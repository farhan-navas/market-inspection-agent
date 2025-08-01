from typing import Optional, List
from pydantic import BaseModel, Field
from overall_ranking_model import OverallRankedCompany

class Rationale(OverallRankedCompany):
    rationale: Optional[str] = Field(None, description="Rationale for the classification and ranking decisions made")

# output from rationale agent
class RationaleList(BaseModel):
    companies: List[Rationale | OverallRankedCompany] = Field(
        ..., description="A list of rationales for the classification and ranking decisions made for various companies"
    )
