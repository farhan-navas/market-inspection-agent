from typing import Optional, List
from pydantic import BaseModel, Field
from companyModels import CompanyMetrics
from classificationModels import ClassifiedList
from signallingModels import SignalledCompany, SignalledList
from backend.app.models.metricRankingModel import CompanyMetricRanking, MetricRankingList
from overallRankingModel import OverallCompanyRanking, OverallRankingList

class Rationale(BaseModel):
    signalled_company: SignalledCompany = Field(..., description="Signalled company with metrics and signals")
    signalled_list: SignalledList = Field(..., description="List of signalled companies with their metrics and signals")
    company_ranking: CompanyMetricRanking = Field(..., description="Ranking of the company based on its metrics and signals")
    ranking_list: MetricRankingList = Field(..., description="List of ranked companies with their metrics and signals")
    overall_company_ranking: OverallCompanyRanking = Field(..., description="Overall company ranking with metrics and signals")
    overall_ranking_list: OverallRankingList = Field(..., description="Overall ranking list of companies with their metrics and signals")
    rationale: str = Field(..., description="Rationale for the classification and ranking decisions made")

class RationaleList(BaseModel):
    rationales: List[Rationale] = Field(..., description="A list of rationales for the classification and ranking decisions made for various companies")


