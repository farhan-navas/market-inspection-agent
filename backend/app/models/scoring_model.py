from typing import List, Union
from pydantic import BaseModel, Field
from classification_models import FinancialClassifiedCompany, EmployeeClassifiedCompany, RealEstateClassifiedCompany

class CompanyMetricRanking(BaseModel):
    company: Union[
        FinancialClassifiedCompany,
        EmployeeClassifiedCompany,
        RealEstateClassifiedCompany,
    ] = Field(
        ...,
        discriminator="type",
        description="Exactly one of the classified-company models"
    )
    indiv_class_score: float = Field(..., description="Total score calculated based on various metrics and signals")

# output from scoring agent
class MetricRankingList(BaseModel):
    companies: List[CompanyMetricRanking] = Field(..., description="A list of ranked companies with their metrics and signals")
