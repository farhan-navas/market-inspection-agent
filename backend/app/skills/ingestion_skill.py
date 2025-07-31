import asyncio

from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
import models

class IngestionSkill:
    def __init__(self, company_information_list: models...):
        self._company_information_list = company_information_list

    @kernel_function(name="ingest_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
    async def ingest_companies(self) -> List[models...]:

        return [{}]
                                                