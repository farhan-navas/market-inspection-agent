from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.orchestrator.scanner_orchestrator import run_scan

app = FastAPI()

origins = [
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatPayloadType(BaseModel):
    content: str

class FormPayloadType(BaseModel):
    industry: str
    region: str
    country: str

class CompanyPayloadType(BaseModel):
    company_name: str

@app.get("/")
def get_root_data():
    return { 'message': 'Welcome to Market Scanner Backend!' }

@app.get("/trial")
async def fetch_data():
    opts = {"industry": "Healthcare", "country": None, "region": None} # hardcoded trial

    res = await run_scan(opts)
    return { 
        "message": 'Welcome to Market Scanner Backend!', 
        "companies": res.companies if hasattr(res, 'companies') else [], 
        "res": f"Persisted {len(res.companies) if hasattr(res, 'companies') else 0} company records." 
    }

@app.get('/api/scanner-chat')
def post_chat_data(chat_payload: ChatPayloadType):
    content = chat_payload.content
    # TODO: Implement chat functionality
    return {"message": "Chat received", "content": content}

@app.get("/api/scanner-form")
def post_form_data(form_payload: FormPayloadType):
    industry, region, country = form_payload.industry, form_payload.region, form_payload.country

@app.get("/api/dashboard/company-name")
def post_company_data(company_payload: CompanyPayloadType):
    company_name = company_payload.company_name
    # TODO: Implement company data retrieval
    return {"message": f"Company data requested for {company_name}"}
    
