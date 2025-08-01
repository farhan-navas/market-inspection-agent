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

    # def __init__(self, company_information_list: IngestedList):
    #     self._company_information_list = company_information_list

    @kernel_function(name="region_split_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
    async def classify_companies(self) -> List[ClassifiedMetricsList]: