import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from backend.app.models.expansion_eval_model import ExpansionEvalCompanyList
from backend.app.models.overall_ranking_model import OverallRankingList

class OverallRankingSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="rank_companies", description=descriptions.OVERALL_SCORING_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: ExpansionEvalCompanyList) -> OverallRankingList:
        