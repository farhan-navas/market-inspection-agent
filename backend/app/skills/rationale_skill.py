import asyncio
from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from backend.app.models.merge_model import MergedCompanyList
from backend.app.models.rationale_model import RationaleList

class RationaleSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="rationale_companies", description=descriptions.RATIONALE_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: MergedCompanyList) -> RationaleList:
        