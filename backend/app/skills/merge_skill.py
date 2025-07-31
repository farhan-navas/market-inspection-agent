import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from backend.app.models.overall_ranking_model import OverallRankingList
from backend.app.models.merge_model import MergedCompanyList

class OverallRankingSkill:
    def __init__(self):
        self.project = project

    # def __init__(self, company_information_list: OverallRankingList):
    #     self._company_information_list = company_information_list

    @kernel_function(name="region_split_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
    async def classify_companies(self) -> List[MergedCompanyList]:
     