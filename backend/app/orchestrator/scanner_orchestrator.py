import os
import asyncio
from typing import List, Type, TypeVar
from main import DB_CONNECTION_URL

from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from app.skills.base_scanner_skill import BaseScannerSkill
from app.skills.region_split_skill import RegionSplitSkill 
from app.skills.ingestion_skill import IngestionSkill
from app.skills.classification_skill import ClassificationSkill
from app.skills.scoring_skill import ScoringSkill
from app.skills.expansion_eval_skill import ExpansionEvalSkill
from app.skills.overall_ranking_skill import OverallRankingSkill
from app.skills.rationale_skill import RationaleSkill
from app.skills.storage_skill import StorageSkill
# from app.skills.vectorize_skill import VectorizeSkill

from app.models.company_model import BaseScannerList
from app.models.region_split_model import RegionSplitList
from app.models.scoring_model import MetricRankingList

from app.exceptions.plugin_invocation_exception import PluginInvocationError

# 1. Initialize Semantic Kernel with Azure OpenAI 
kernel = Kernel()

kernel.add_service(
    AzureChatCompletion(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="o4-mini",
    )
) 
scanner_skill = BaseScannerSkill()
region_split_skill = RegionSplitSkill()
ingestion_skill = IngestionSkill()
classification_skill = ClassificationSkill()
scoring_skill = ScoringSkill()
expansion_eval_skill = ExpansionEvalSkill()
overall_ranking_skill = OverallRankingSkill()
rationale_skill = RationaleSkill()
storage_skill = StorageSkill(DB_CONNECTION_URL)
# vectorize_skill = VectorizeSkill()

# 2. Import each agent as a Semantic Kernel skill
scanner_skill = kernel.add_plugin(scanner_skill, "Scanner")
region_split_skill = kernel.add_plugin(region_split_skill, "Region Splitter")
ingsestion_skill = kernel.add_plugin(ingestion_skill, "Ingestion")
classification_skill = kernel.add_plugin(classification_skill, "Classify")
ranking_skill = kernel.add_plugin(scoring_skill, "Scoring")
signal_skill = kernel.add_plugin(expansion_eval_skill, "Signal")
overall_ranking_skill = kernel.add_plugin(overall_ranking_skill, "Overall Ranking")
rationale_skill = kernel.add_plugin(rationale_skill, "Rationale")
storage_skill = kernel.add_plugin(storage_skill, "Storage")
# vectorize_skill = kernel.add_plugin(vectorize_skill, "Vectorize")

def shard_array(arr, size):
    """Split list into chunks of given size"""
    return [arr[i : i + size] for i in range(0, len(arr), size)]

T = TypeVar("T")

async def invoke_kernel_plugin(plugin_name: str, function_name: str, return_type: Type[T], *args: KernelArguments) -> T:
    try:
        # if kernel.invoke itself fails, that exception will be caught below
        res = await kernel.invoke(
            plugin_name=plugin_name,
            function_name=function_name,
            arguments=args[0]
        )
    except Exception as e:
        # wrap any lower-level error in a more descriptive exception
        raise PluginInvocationError(plugin_name, function_name, e.__str__(), e)

    # if we get back None, or there's no .value, treat it as an error
    if res is None or not hasattr(res, "value"):
        raise PluginInvocationError(plugin_name, function_name, "No valid data returned!")

    return res.value # type: ignore

async def process_shard(shard: RegionSplitList) -> MetricRankingList:
    # Enrich
    ingested_ctx = await invoke_kernel_plugin("Ingestion", "ingest_companies",  KernelArguments(company_information_list=shard))

    # Region Split
    region_split_ctx = await invoke_kernel_plugin("Region Splitter", "region_split_companies", KernelArguments(company_information_list=ingested_ctx))

    # Classify
    classified_ctx = await invoke_kernel_plugin("Ingestion", "ingest_companies", KernelArguments(company_information_list=region_split_ctx))

    # Signal detection
    scored_ctx = await invoke_kernel_plugin("Scoring", "score_companies", KernelArguments(company_information_list=classified_ctx))
    
    return scored_ctx


async def run_scan(opts: dict):
    """
    Orchestrates a full scan:
      1. Fetch raw companies
      2. Shard & parallel (Ingest -> Normalize -> Classify -> Signal)
      3. Merge
      4. Rank
      5. Top 500
      6. Generate rationales in batches
      7. Persist
    """
    # 1) Fetch raw list
    raw_ctx: BaseScannerList = await invoke_kernel_plugin("Scanner", "fetch_companies")

    # 2) Shard raw context based on safe(?) batch size
    region_batch_size = 5000
    region_shards = shard_array(raw_ctx, region_batch_size)

    # 3) Get full region split batch list of list, then concat them (due to .gather) 
    region_split_batches_list: List[RegionSplitList] = await asyncio.gather(*[
        invoke_kernel_plugin[RegionSplitList]("Region Split", "region_split_companies", KernelArguments(company_information_list=shard)) 
            for shard in region_shards
    ])

    region_split_batches: RegionSplitList = [
        item for batch in region_split_batches_list for item in batch
    ]

    # 2) Shard based on safe batch size (tune!!)
    batch_size = 1000
    shards = shard_array(region_split_batches, batch_size)

    # 3) Parallel processing of shards
    scored_batches = await asyncio.gather(*[
        process_shard(shard) for shard in shards
    ])

    signaled_all = [c for batch in signaled_batches for c in batch]

    # 4) Ranking
    rank_ctx = await kernel.run_async(
        {"companies": signaled_all},
        ranking_skill.RankingAgent
    )
    ranked = rank_ctx.result

    # 5) Take top 500
    top_500 = ranked[:500]

    # 6) Generate rationales in smaller batches
    rationale_batch_size = 50
    rationale_shards = shard_array(top_500, rationale_batch_size)
    explained = []
    for batch in rationale_shards:
        rat_ctx = await kernel.run_async(
            {"companies": batch},
            rationale_skill.RationaleAgent
        )
        explained.extend(rat_ctx.result)

    # 7) Persist to storage
    await kernel.run_async(
        {"records": explained},
        storage_skill.StorageAgent
    )

    return explained


if __name__ == "__main__":
    # Example invocation
    opts = {"industry": None, "country": None, "region": None}
    results = asyncio.run(run_scan(opts))
    print(f"Persisted {len(results)} company records.")
