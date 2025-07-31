import asyncio

from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from app.models.region_split_model import RegionSplitList
from app.models.ingested_models import IngestedList

class IngestionSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="ingest_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
    async def ingest_companies(self, company_information_list: RegionSplitList) -> IngestedList:

        return [{}]
                                                