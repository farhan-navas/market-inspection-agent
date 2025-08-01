import asyncio

from semantic_kernel.functions import kernel_function
from typing import List
import backend.app.descriptions as descriptions
from main import project

from app.models.region_split_model import RegionSplitList
from app.models.ingested_models import IngestedList

class IngestionSkill:
    def __init__(self):
        self.project = project

    @kernel_function(
            name="ingest_companies", 
            description=descriptions.INGESTION_SKILL_DESCRIPTION
    )

    async def ingest_companies(self, company_information_list: RegionSplitList) -> IngestedList:       
        try:
            # Create a list to hold the ingested companies
            ingested_companies = []

            # Iterate through each company in the provided list
            for company in company_information_list.companies:
                # Create an entity for each company
                entity = self.project.entities.create(
                    entity_type="company",
                    data={
                        "name": company.name,
                        "region": company.region,
                        "ticker": company.ticker,
                        "link": company.link
                    }
                )
                ingested_companies.append(entity)

            # Return the list of ingested companies
            return IngestedList(companies=ingested_companies).model_dump()
        except Exception as e:
            print(f"Error ingesting companies: {e}")
            return IngestedList(companies=[]).model_dump()                                         