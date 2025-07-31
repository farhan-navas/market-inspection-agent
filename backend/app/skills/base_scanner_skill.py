import asyncio

from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
import models

class BaseScannerSkill:    
    @kernel_function(name="fetch_companies", description=descriptions.BASE_SCANNER_SKILL_DESCRIPTION)
    async def fetch_companies(self) -> List[models.CompanyInformationList]:

        return [{}]
                                                