import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from app.models.classification_models import ClassifiedMetricsList
from app.models.scoring_model import MetricRankingList

class ScoringSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="scoring_companies", description=descriptions.SCORING_SKILL_DESCRIPITION)
    async def agent_function(self, company_information_list: ClassifiedMetricsList) -> MetricRankingList:
     