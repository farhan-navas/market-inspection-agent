# import asyncio
# from semantic_kernel.functions import kernel_function
# from typing import List
# import app.descriptions as descriptions
# from main import project

# from app.models.rationale_model import RationaleList
# from app.models.vectorization_model import VectorEmbeddedCompanyList

# class VectorizeSkill:
#     def __init__(self):
#         self.project = project


#     @kernel_function(name="region_split_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
#     async def classify_companies(self, company_information_tool: RationaleList) -> VectorEmbeddedCompanyList:
#         res: VectorEmbeddedCompanyList = [{}] 

#         return res