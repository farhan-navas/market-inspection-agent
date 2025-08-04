import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

load_dotenv()

class AppConfig:

    def __init__(self):
        self.MODEL: str = "o4-mini"

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL environment variable is required.")
        self.DATABASE_URL: str = db_url

        bing_id = os.getenv("BING_CONNECTION_ID")
        if not bing_id:
            raise ValueError("BING_CONNECTION_ID environment variable is required.")
        self.BING_CONNECTION_ID: str = bing_id

        agent_endpoint = os.getenv("AZURE_AI_AGENT_ENDPOINT")
        if not agent_endpoint:
            raise ValueError("AZURE_AI_AGENT_ENDPOINT environment variable is required.")
        self.AZURE_AI_AGENT_ENDPOINT = agent_endpoint

        openai_key = os.getenv("AZURE_OPENAI_KEY")
        if not openai_key:
            raise ValueError("AZURE_OPENAI_KEY environment variable is required.")
        self.AZURE_OPENAI_KEY = openai_key

        openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if not openai_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required.")
        self.AZURE_OPENAI_ENDPOINT = openai_endpoint

        self.project = self.create_azure_project_client()

    def create_azure_project_client(self):
        project = AIProjectClient(
            endpoint=self.AZURE_AI_AGENT_ENDPOINT,
            credential=DefaultAzureCredential()
        )

        return project
    
    def initialize_kernel(self):
        # initialize semantic kernel with azure openAI 
        kernel = Kernel()

        kernel.add_service(
            AzureChatCompletion(
                api_key=self.AZURE_OPENAI_KEY,
                endpoint=self.AZURE_OPENAI_ENDPOINT,
                deployment_name=self.MODEL,
            )
        )

        return kernel

    def create_kernel(self):
        """Create a new kernel instance"""
        return self.initialize_kernel()

    def get_ai_project_client(self):
        """Get the AI project client"""
        return self.project

config = AppConfig()