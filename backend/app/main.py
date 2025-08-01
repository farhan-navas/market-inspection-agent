import os
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()


origins = [
    "http://localhost:5173", 
]

DB_CONNECTION_URL = os.getenv("DATABASE_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model="o4-mini"

project = AIProjectClient(
    endpoint="https://hackathon-group4-resource.services.ai.azure.com/api/projects/hackathon-group4",
    credential=DefaultAzureCredential()
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
    return { 'Welcome to Market Scanner Backend!' }

@app.get('/api/scanner-chat')
def post_chat_data(chat_payload: ChatPayloadType):
    content = chat_payload.content

@app.get("/api/scanner-form")
def post_form_data(form_payload: FormPayloadType):
    industry, region, country = form_payload.industry, form_payload.region, form_payload.country

@app.get("/api/dashboard/company-name")
def post_company_data(company_payload: CompanyPayloadType):
    company_name = company_payload.company_name
    
