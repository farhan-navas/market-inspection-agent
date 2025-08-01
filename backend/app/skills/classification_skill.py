import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from app.models.ingested_models import IngestedList
from app.models.classification_models import ClassifiedMetricsList

class ClassificationSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="classify_companies", description=descriptions.CLASSIFICATION_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: IngestedList) -> ClassifiedMetricsList:
