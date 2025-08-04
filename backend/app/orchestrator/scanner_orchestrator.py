import os
import asyncio
from typing import List, Type, TypeVar, cast
from pydantic import BaseModel
from app.app_config import config

from semantic_kernel.functions.kernel_arguments import KernelArguments

# Initialize kernel and project from config
kernel = config.create_kernel()
project = config.get_ai_project_client()

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
from app.models.ingested_model import IngestedList
from app.models.classification_model import ClassifiedMetricsList 
from app.models.scoring_model import MetricRankingList
from app.models.expansion_eval_model import ExpansionEvalCompanyList 
from app.models.overall_ranking_model import OverallRankingList
from app.models.rationale_model import RationaleList

from app.exceptions.plugin_invocation_exception import PluginInvocationError

# Initialize skills
scanner_skill = BaseScannerSkill()
region_split_skill = RegionSplitSkill()
ingestion_skill = IngestionSkill()
classification_skill = ClassificationSkill()
scoring_skill = ScoringSkill()
expansion_eval_skill = ExpansionEvalSkill()
overall_ranking_skill = OverallRankingSkill()
rationale_skill = RationaleSkill()
storage_skill = StorageSkill(config.DATABASE_URL)

# Register each agent as a Semantic Kernel skill
scanner_skill = kernel.add_plugin(scanner_skill, "Scanner")
region_split_skill = kernel.add_plugin(region_split_skill, "Region Splitter")
ingestion_skill = kernel.add_plugin(ingestion_skill, "Ingestion")
classification_skill = kernel.add_plugin(classification_skill, "Classify")
scoring_skill = kernel.add_plugin(scoring_skill, "Scoring")
expansion_eval_skill = kernel.add_plugin(expansion_eval_skill, "Expansion Evaluation")
overall_ranking_skill = kernel.add_plugin(overall_ranking_skill, "Overall Ranking")
rationale_skill = kernel.add_plugin(rationale_skill, "Rationale")
storage_skill = kernel.add_plugin(storage_skill, "Storage")
# vectorize_skill = kernel.add_plugin(vectorize_skill, "Vectorize")

def shard_array(arr, size):
    # Split list into chunks of given size
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

    raw_return_value = res.value

    # if the return type is a Pydantic model, validate it
    if issubclass(return_type, BaseModel):
        try:
            return return_type.model_validate(raw_return_value)
        except Exception as e:
            raise PluginInvocationError(
                plugin_name,
                function_name,
                f"Returned value does not match expected model {return_type.__name__}: {e}"
            )

    # if it's not a Pydantic model (rare case), just trust the type hint
    return cast(T, raw_return_value)

async def process_shard(shard: RegionSplitList) -> ExpansionEvalCompanyList:
    # enrich
    ingested_ctx = await invoke_kernel_plugin("Ingestion", "ingest_companies", IngestedList, KernelArguments(company_information_list=shard))

    # classify
    classified_ctx = await invoke_kernel_plugin("Classify", "classify_companies", ClassifiedMetricsList, KernelArguments(company_information_list=ingested_ctx))

    # score
    scored_ctx = await invoke_kernel_plugin("Scoring", "score_companies", MetricRankingList, KernelArguments(company_information_list=classified_ctx))

    # evaluate expansion
    expansion_eval_ctx = await invoke_kernel_plugin("Expansion Evaluation", "evaluation_expansion_companies", ExpansionEvalCompanyList, KernelArguments(company_information_list=scored_ctx))
    
    return expansion_eval_ctx


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
    raw_ctx: BaseScannerList = await invoke_kernel_plugin("Scanner", "fetch_companies", BaseScannerList, KernelArguments(opts))

    # 2) Shard raw context based on safe(?) batch size
    region_batch_size = 5000
    region_shards = shard_array(raw_ctx, region_batch_size)

    # 3) Get full region split batch list of list, then concat them (due to .gather) 
    region_split_batches_list = await asyncio.gather(*[
        invoke_kernel_plugin("Region Split", "region_split_companies", RegionSplitList ,KernelArguments(company_information_list=shard)) 
            for shard in region_shards
    ])

    region_split_batches = RegionSplitList(
        companies=[
            company
            for batch in region_split_batches_list
            for company in batch.companies
        ]
    )

    # 4) Shard based on safe batch size (tune!!)
    batch_size = 1000
    shards: List[RegionSplitList] = shard_array(region_split_batches, batch_size)

    # 5) Parallel processing of shards
    scored_batches_list = await asyncio.gather(*[
        process_shard(shard) for shard in shards
    ])

    scored_batches = ExpansionEvalCompanyList(
        companies=[
            company
            for batch in scored_batches_list
            for company in batch.companies
        ]
    ) 

    # 6) Ranking
    rank_ctx = await invoke_kernel_plugin("Overall Ranking", "rank companies", OverallRankingList, KernelArguments(company_information_list=scored_batches))

    # 7) Take top 500
    top_500 = OverallRankingList(companies=rank_ctx.companies[:500])

    # 8) Generate rationales in smaller batches
    rationale_batch_size = 50
    rationale_shards = shard_array(top_500, rationale_batch_size)

    explained_companies_list = await asyncio.gather(*[
        invoke_kernel_plugin("Rationale", "rationale_companies", RationaleList, KernelArguments(company_information_list=shard))
            for shard in rationale_shards
    ])

    explained_companies = RationaleList(
        companies=[
            company
            for batch in explained_companies_list
            for company in batch.companies
        ]
    )

    # 9) Persist to storage
    await invoke_kernel_plugin("Storage", "store_companies", dict, KernelArguments(company_information_list=explained_companies))

    # 10) Return explained companies to backend for validation
    return explained_companies
