from typing import Optional, List, Literal
from pydantic import BaseModel, Field

class CompanyInformation(BaseModel):
    name: str = Field(..., description="The name of the company")
    region: Literal["aus", "us", "asia", "emea"] = Field(..., description="The region where the company operates")
    ticker: Optional[str] = Field(None, description="The stock ticker symbol of the company")
    link: Optional[str] = Field(None, description="A link to the company's website or profile")

# output type from BaseScannerAgent
class BaseScannerList(BaseModel):
    companies: List[CompanyInformation] = Field(..., description="A list of company information objects")
