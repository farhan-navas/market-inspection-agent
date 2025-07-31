from typing import List, Literal
from pydantic import BaseModel, Field
from ingested_models import FinancialMetrics, EmployeeMetrics, RealEstateMetrics
from company_models import CompanyInformation

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
    real_estate: RealEstateMetrics = Field(..., description="Classified real estate-related metrics of the company")

# output from the classification agent
class ClassifiedMetricsList(BaseModel):
    type: Literal["real_estate"] = Field(
        "real_estate", description="Discriminator for real-estate models"
    )
    companies: List[FinancialClassifiedCompany | EmployeeClassifiedCompany | RealEstateClassifiedCompany] = Field(
        ...,
        description="A list of classified real companies with financial, employee, or realestate metrics"
    )