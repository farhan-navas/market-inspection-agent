import asyncio
from semantic_kernel.functions import kernel_function
from typing import Optional
import backend.app.descriptions as descriptions
from main import project

from app.models.company_models import CompanyInformation, BaseScannerList

class BaseScannerSkill:    
    def __init__(self):
        self.project = project

    @kernel_function(
            name="fetch_companies", 
            description=descriptions.BASE_SCANNER_SKILL_DESCRIPTION
    )
    async def fetch_companies(self, industry: str, region: Optional[str], country: Optional[str]) -> BaseScannerList:

        # Fetch companies based on industry, region, and country
        filters = {}
        if industry:
            filters["industry"] = industry
        if region:
            filters["region"] = region
        if country:
            filters["country"] = country

        try:
            entities = self.project.entities.list(
                entity_type="company",
                filters=filters
            )

            company_list = [
                CompanyInformation(
                    id=entity.id,
                    name=entity.name,
                    industry=entity.industry,
                    region=entity.region,
                    country=entity.country
                ) for entity in entities
            ]

            scanner_list = BaseScanner(
                companies=company_list
            )

            return scanner_list.dict()
        except Exception as e:
            print(f"Error fetching companies: {e}")
            return BaseScanner(companies=[]).dict()
        
        


                                                