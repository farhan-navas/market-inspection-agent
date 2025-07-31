from typing import Optional, List
from pydantic import BaseModel, Field
from metricsModels import FinancialMetrics, EmployeeMetrics, RealEstateMetrics
from companyModels import CompanyInformation

class FinancialClassifiedMetrics(BaseModel):
    company: CompanyInformation = Field(..., description="Basic information about the company")
    finance_metrics: FinancialMetrics = Field(..., description="Classified financial metrics of the company")

class EmployeeClassifiedMetrics(BaseModel):
    company: CompanyInformation = Field(..., description="Basic information about the company")
    employee: EmployeeMetrics = Field(..., description="Classified employee-related metrics of the company")

class RealEstateClassifiedMetrics(BaseModel):
    company: CompanyInformation = Field(..., description="Basic information about the company")
    real_estate: RealEstateMetrics = Field(..., description="Classified real estate-related metrics of the company")

class ClassifiedList(BaseModel):
    financial_metrics: List[FinancialClassifiedMetrics] = Field(..., description="A list of classified financial metrics for companies")
    employee_metrics: List[EmployeeClassifiedMetrics] = Field(..., description="A list of classified employee-related metrics for companies")
    real_estate_metrics: List[RealEstateClassifiedMetrics] = Field(..., description="A list of classified real estate-related metrics for companies")
