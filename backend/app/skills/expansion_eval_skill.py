import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from app.models.scoring_model import MetricRankingList
from backend.app.models.expansion_eval_model import ExpansionEvalCompanyList

class ExpansionEvalSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="evaluate_expansion_companies", description=descriptions.EXPANSION_EVALUATION_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: MetricRankingList) -> ExpansionEvalCompanyList:
     