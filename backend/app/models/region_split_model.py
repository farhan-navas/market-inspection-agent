from typing import List, Literal
from pydantic import BaseModel, Field

from company_models import CompanyInformation

class AustraliaRegionSplit(CompanyInformation):
    region: Literal["aus"] = Field(
        "aus",
        description="This subclass only covers the Australian region"
    )


class USRegionSplit(CompanyInformation):
    region: Literal["us"] = Field(
        "us",
        description="This subclass only covers the US region"
    )


class AsiaRegionSplit(CompanyInformation):
    region: Literal["asia"] = Field(
        "asia",
        description="This subclass only covers the Asia region"
    )


class EMEARegionSplit(CompanyInformation):
    region: Literal["emea"] = Field(
        "emea",
        description="This subclass only covers the EMEA region"
    )

# outputs from the region split model
class RegionSplitList(BaseModel):
    companies: List[AustraliaRegionSplit | USRegionSplit | AsiaRegionSplit | EMEARegionSplit] = Field(
        ..., description="All companies in the Australia region"
    )
