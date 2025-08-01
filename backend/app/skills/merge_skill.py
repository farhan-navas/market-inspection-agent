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

    @kernel_function(name="merge_companies", description=descriptions.MERGE_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: OverallRankingList) -> MergedCompanyList:
     