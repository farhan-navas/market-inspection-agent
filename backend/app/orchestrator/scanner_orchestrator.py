import os
import asyncio
from main import DB_CONNECTION_URL

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.services.ai_service_client_base import AIServiceClientBase

from backend.app.skills.base_scanner_skill import BaseScannerSkill
from backend.app.skills.region_split_skill import RegionSplitSkill 
from backend.app.skills.ingestion_skill import IngestionSkill
from backend.app.skills.classification_skill import ClassificationSkill
from backend.app.skills.scoring_skill import ScoringSkill
from backend.app.skills.expansion_eval_skill import ExpansionEvalSkill
from backend.app.skills.overall_ranking_skill import OverallRankingSkill
from backend.app.skills.rationale_skill import RationaleSkill
from backend.app.skills.storage_skill import StorageSkill
from backend.app.skills.vectorize_skill import VectorizeSkill

from backend.app.models.company_models import BaseScannerList

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


async def process_shard(shard: BaseScannerList):
    # Enrich
    enriched_ctx = await kernel.invoke(
        ingestion_skill.agent_function,
        shard,
    )
    enriched = enriched_ctx.result

    # Normalize
    clean_ctx = await kernel.run_async(
        {"companies": enriched},
        normalize_skill.NormalizeAgent
    )
    cleaned = clean_ctx.result

    # Classify
    classified_ctx = await kernel.run_async(
        {"companies": cleaned},
        classification_skill.ClassifyAgent
    )
    classified = classified_ctx.result

    # Signal detection
    signal_ctx = await kernel.run_async(
        {"companies": classified},
        signal_skill.SignalAgent
    )
    return signal_ctx.result


async def run_scan(opts: dict):
    """
    Orchestrates a full scan:
      1. Fetch raw companies
      2. Shard & parallel (Ingest → Normalize → Classify → Signal)
      3. Merge
      4. Rank
      5. Top 500
      6. Generate rationales in batches
      7. Persist
    """
    # 1) Fetch raw list
    raw_ctx = await kernel.run_async(
        opts,
        scanner_skill.agent_function
    )
    raw_companies = raw_ctx.result

    # 2) Shard based on safe batch size (tune as needed)
    batch_size = 1000
    shards = shard_array(raw_companies, batch_size)

    # 3) Parallel processing of shards
    signaled_batches = await asyncio.gather(*[
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
