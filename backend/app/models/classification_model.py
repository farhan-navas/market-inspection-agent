from typing import List, Literal
from pydantic import BaseModel, Field

from app.models.ingested_model import FinancialMetrics, EmployeeMetrics, RealEstateMetrics
from app.models.company_model import CompanyInformation

class FinancialClassifiedCompany(CompanyInformation):
    type: Literal["financial"] = Field(
        "financial", description="Discriminator for financial models"
    )
    finance_metrics: FinancialMetrics = Field(..., description="Classified financial metrics of the company")

class EmployeeClassifiedCompany(CompanyInformation):
    type: Literal["employee"] = Field(
        "employee", description="Discriminator for employee models"
    )
    employee: EmployeeMetrics = Field(..., description="Classified employee-related metrics of the company")

class RealEstateClassifiedCompany(CompanyInformation):
    type: Literal["real_estate"] = Field(
        "real_estate", description="Discriminator for real estate models"
    )
    real_estate: RealEstateMetrics = Field(..., description="Classified real estate-related metrics of the company")

# output from the classification agent
class ClassifiedMetricsList(BaseModel):
    companies: List[FinancialClassifiedCompany | EmployeeClassifiedCompany | RealEstateClassifiedCompany] = Field(
        ...,
        description="A list of classified real companies with financial, employee, or realestate metrics"
    )