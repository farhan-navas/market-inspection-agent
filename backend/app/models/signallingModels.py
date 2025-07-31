from typing import Optional, List
from pydantic import BaseModel, Field
from classificationModels import ClassifiedList
from companyModels import CompanyMetrics

class ExpansionSignal(BaseModel):
    expansion_region: str = Field(..., description="Region where the company is expanding")
    expansion_confidence: float = Field(..., ge=0, le=100,description="Confidence score for company expansion (0-100 scale)")

class SignalledCompany(BaseModel):
    company: CompanyMetrics = Field(..., description="Basic information about the company and its metrics")
    metrics_list: ClassifiedList = Field(..., description="Classified metrics for the company across various categories")
    strong_financial_growth: float = Field(..., description="Financial growth rate indicating strong performance")
    aggressive_workforce_expansion: Optional[float] = Field(...,description="Workforce expansion rate indicating aggressive hiring")
    strategic_real_estate_moves: Optional[float] = Field(...,description="Real estate moves indicating strategic expansion")
    high_value_signal: float = Field(...,description="Overall signal value indicating high potential for expansion")
    expansion_signals: ExpansionSignal = Field(..., description="List of expansion signals indicating regions and confidence levels")

class SignalledList(BaseModel):
    companies: List[SignalledCompany] = Field(..., description="A list of signalled companies with their metrics and signals")

