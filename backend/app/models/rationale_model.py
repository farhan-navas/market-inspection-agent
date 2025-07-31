from typing import Optional, List
from pydantic import BaseModel, Field
from overall_ranking_model import OverallRankedCompany

class Rationale(OverallRankedCompany):
    rationale: str = Field(..., description="Rationale for the classification and ranking decisions made")

# output from rationale agent
class RationaleList(BaseModel):
    rationales: List[Rationale] = Field(..., description="A list of rationales for the classification and ranking decisions made for various companies")


