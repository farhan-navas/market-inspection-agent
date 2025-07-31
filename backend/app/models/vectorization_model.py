from typing import Optional, List
from pydantic import BaseModel, Field
from rationale_model import Rationale

class VectorEmbeddedCompany(Rationale):
    vector_embedding: str = Field(
        ..., description="Vector embedding of the rationale for the classification and ranking decisions made"
    )

# output from rationale agent
class VectorEmbeddedCompanyList(BaseModel):
    companies: List[VectorEmbeddedCompany] = Field(..., description="A list of rationales for the classification and ranking decisions made for various companies")
