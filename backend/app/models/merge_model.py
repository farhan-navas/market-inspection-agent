from typing import List
from pydantic import BaseModel, Field

from app.models.expansion_eval_model import ExpansionEvalCompany
from app.models.ingested_model import FinancialMetrics, EmployeeMetrics, RealEstateMetrics

class MergedCompany(ExpansionEvalCompany):
    finance_metrics: FinancialMetrics = Field(
        ..., description="Classified financial metrics of the company"
    )
    employee: EmployeeMetrics = Field(
        ..., description="Classified employee-related metrics of the company"
    )
    real_estate: RealEstateMetrics = Field(
        ..., description="Classified real estate-related metrics of the company"
    )

# output of merge agent
class MergedCompanyList(BaseModel):
    companies: List[MergedCompany] = Field(..., description="A list of merged companies with all possible metrics and signals")
