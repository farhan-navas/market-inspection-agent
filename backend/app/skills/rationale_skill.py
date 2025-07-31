import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from backend.app.models.merge_model import MergedCompanyList
from backend.app.models.rationale_model import RationaleList

class RationaleSkill:
    def __init__(self, company_information_list: MergedCompanyList):
        self._company_information_list = company_information_list

    @kernel_function(name="region_split_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
    async def classify_companies(self) -> List[RationaleList]:
        