from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

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

@app.get("/")
def get_root_data():
    return { 'Welcome to Market Scanner Backend!' }

@app.post('/api/scanner-chat')
def post_chat_data(chat_payload: ChatPayloadType):
    content = chat_payload.content

@app.post("/api/scanner-form")
def post_form_data(form_payload: FormPayloadType):
    industry, region, country = form_payload.industry, form_payload.region, form_payload.country

