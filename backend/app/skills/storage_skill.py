import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from backend.app.models.rationale_model import RationaleList

class StorageSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="storage_companies", description=descriptions.STORAGE_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: RationaleList) -> str:
        