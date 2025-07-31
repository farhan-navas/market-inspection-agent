import asyncio

from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from app.models.company_models import CompanyInformation, BaseScannerList
from app.models.region_split_model import AustraliaRegionSplit, USRegionSplit, EMEARegionSplit, AsiaRegionSplit, RegionSplitList

class RegionSplitSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="region_split_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
    async def region_split_companies(self, company_information_list: BaseScannerList) -> List[RegionSplitList]:

        return [{}]
                                                