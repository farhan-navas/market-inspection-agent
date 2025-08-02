from typing import List
from pydantic import BaseModel, Field

from app.models.merge_model import MergedCompany

class OverallRankedCompany(MergedCompany):
    total_score: float = Field(..., description="Total score calculated based on various metrics and signals")

# output from overall ranking agent
class OverallRankingList(BaseModel):
    companies: List[OverallRankedCompany] = Field(..., description="A list of ranked companies with their metrics and signals")
