from typing import Optional, List
from pydantic import BaseModel, Field
from companyModels import CompanyMetrics
from classificationModels import ClassifiedList
from signallingModels import SignalledCompany, SignalledList

class CompanyMetricRanking(BaseModel):
    signalled_company: SignalledCompany = Field(..., description="Signalled company with metrics and signals")
    signalled_list: SignalledList = Field(..., description="List of signalled companies with their metrics and signals")
    total_score: float = Field(..., description="Total score calculated based on various metrics and signals")

class MetricRankingList(BaseModel):
    companies: List[CompanyMetricRanking] = Field(..., description="A list of ranked companies with their metrics and signals")
