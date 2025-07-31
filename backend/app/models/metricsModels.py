from typing import Optional, List
from pydantic import BaseModel, Field

class FinancialMetrics(BaseModel):
    annual_revenue: float = Field(..., description="Annual revenue of the company")
    net_profit_margin: float = Field(..., description="Net profit margin of the company as a percentage")
    annual_growth_CAGR: float = Field(..., description="Compound annual growth rate (CAGR) of the company's revenue")
    mA_count: Optional[int] = Field(None, description="Number of mergers and acquisitions the company has been involved in the last 12 months")
    ipo_filings_count: Optional[int] = Field(None, description="Number of IPO filings the company has made")
    divestments_count: Optional[int] = Field(None, description="Number of divestments the company has made")

class EmployeeMetrics(BaseModel):
    employee_count: Optional[int] = Field(None, description="Total number of employees in the company")
    employee_growth_rate: Optional[float] = Field(None, description="Employee growth rate over the last year as a percentage")

class RealEstateMetrics(BaseModel):
    space_footprint: Optional[int] = Field(None, description="Total square footage of the company's real estate holdings")
    lease_expiry_count: Optional[int] = Field(None, description="Number of lease expiries in the next 12 months")
    expansion_news_count: Optional[int] = Field(None, description="Number of news articles related to real estate expansion in the last 6 months")
    consolidation_count: Optional[int] = Field(None, description="Number of consolidation activities")
    relocation_news_count: Optional[int] = Field(None, description="Number of news articles related to real estate relocation in the last 6 months")
