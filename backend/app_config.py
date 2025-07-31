# app_config.py
import logging
import os
from typing import Optional

from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient
from dotenv import load_dotenv
from semantic_kernel.kernel import Kernel

# Load environment variables from .env file
load_dotenv()


class AppConfig:
    """Application configuration class that loads settings from environment variables."""

    def __init__(self):
        """Initialize the application configuration with environment variables."""
        # Azure authentication settings
        self.AZURE_TENANT_ID = self._get_optional("AZURE_TENANT_ID")
        self.AZURE_CLIENT_ID = self._get_optional("AZURE_CLIENT_ID")
        self.AZURE_CLIENT_SECRET = self._get_optional("AZURE_CLIENT_SECRET")

        # CosmosDB settings
        self.COSMOSDB_ENDPOINT = self._get_optional("COSMOSDB_ENDPOINT")
        self.COSMOSDB_DATABASE = self._get_optional("COSMOSDB_DATABASE")
        self.COSMOSDB_CONTAINER = self._get_optional("COSMOSDB_CONTAINER")

        # Azure OpenAI settings
        self.AZURE_OPENAI_DEPLOYMENT_NAME = self._get_required(
            "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"
        )
        self.AZURE_OPENAI_API_VERSION = self._get_required(
            "AZURE_OPENAI_API_VERSION", "2024-11-20"
        )
        self.AZURE_OPENAI_ENDPOINT = self._get_required("AZURE_OPENAI_ENDPOINT")
        self.AZURE_OPENAI_SCOPES = [
            f"{self._get_optional('AZURE_OPENAI_SCOPE', 'https://cognitiveservices.azure.com/.default')}"
        ]

        # Frontend settings
        self.FRONTEND_SITE_NAME = self._get_optional(
            "FRONTEND_SITE_NAME", "http://127.0.0.1:3000"
        )

        # Azure AI settings
        self.AZURE_AI_SUBSCRIPTION_ID = self._get_required("AZURE_AI_SUBSCRIPTION_ID")
        self.AZURE_AI_RESOURCE_GROUP = self._get_required("AZURE_AI_RESOURCE_GROUP")
        self.AZURE_AI_PROJECT_NAME = self._get_required("AZURE_AI_PROJECT_NAME")
        self.AZURE_AI_AGENT_ENDPOINT = self._get_required("AZURE_AI_AGENT_ENDPOINT")

        # Cached clients and resources
        self._azure_credentials = None
        self._cosmos_client = None
        self._cosmos_database = None
        self._ai_project_client = None

    def _get_required(self, name: str, default: Optional[str] = None) -> str:
        if name in os.environ:
            return os.environ[name]
        if default is not None:
            logging.warning(
                "Environment variable %s not found, using default value", name
            )
            return default
        raise ValueError(
            f"Environment variable {name} not found and no default provided"
        )

    def _get_optional(self, name: str, default: str = "") -> str:
        if name in os.environ:
            return os.environ[name]
        return default

    def _get_bool(self, name: str) -> bool:
        return name in os.environ and os.environ[name].lower() in ["true", "1"]

    # def get_cosmos_database_client(self):
    #     try:
    #         if self._cosmos_client is None:
    #             self._cosmos_client = CosmosClient(
    #                 self.COSMOSDB_ENDPOINT, credential=get_azure_credential()
    #             )

    #         if self._cosmos_database is None:
    #             self._cosmos_database = self._cosmos_client.get_database_client(
    #                 self.COSMOSDB_DATABASE
    #             )

    #         return self._cosmos_database
    #     except Exception as exc:
    #         logging.error(
    #             "Failed to create CosmosDB client: %s. CosmosDB is required for this application.",
    #             exc,
    #         )
    #         raise

    def create_kernel(self):
        # Create a new kernel instance without manually configuring OpenAI services
        # The agents will be created using Azure AI Agent Project pattern instead
        kernel = Kernel()
        return kernel

    def get_ai_project_client(self):
        if self._ai_project_client is not None:
            return self._ai_project_client

        try:
            credential = DefaultAzureCredential()
            endpoint = self.AZURE_AI_AGENT_ENDPOINT
            self._ai_project_client = AIProjectClient(endpoint=endpoint, credential=credential)

            return self._ai_project_client
        except Exception as exc:
            logging.error("Failed to create AIProjectClient: %s", exc)
            raise

    def get_user_local_browser_language(self) -> str:
        return self._get_optional("USER_LOCAL_BROWSER_LANGUAGE", "en-US")

    def set_user_local_browser_language(self, language: str):
        os.environ["USER_LOCAL_BROWSER_LANGUAGE"] = language


config = AppConfig()