import json

from semantic_kernel.functions import kernel_function
from app.app_config import config
import app.descriptions as DESCRIPTIONS
import app.prompts as PROMPTS

from app.orchestrator.scanner_orchestrator import project

from app.models.ingested_model import IngestedList
from app.models.classification_model import ClassifiedMetricsList

from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, MessageRole, BingGroundingTool

class ClassificationSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="classify_companies", description=DESCRIPTIONS.CLASSIFICATION_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: IngestedList) -> ClassifiedMetricsList:
        agent_id = "classify_companies"
        bing_connection_id = config.BING_CONNECTION_ID

        bing = BingGroundingTool(connection_id=bing_connection_id)

        agent = self.project.agents.create_agent(
            model=config.MODEL,
            name="BaseScannerAgent",
            instructions=PROMPTS.BASE_SCANNER_SKILL_PROMPT,
            tools=bing.definitions,
        )

        print(f"agent has been successfully created with id: {agent.id}")

        thread_run = self.project.agents.create_thread_and_process_run(
            agent_id=agent_id,
            thread=AgentThreadCreationOptions(
                messages=[
                        ThreadMessageOptions(
                        role="user",
                        content=json.dumps(company_information_list.model_dump())
                    )
                ]
            ),
            tool_choice="bing_grounding",
        )

        last_text = self.project.agents.messages.get_last_message_text_by_role(
            thread_id=thread_run.thread_id,
            role=MessageRole("assistant")
        )
        # last_text is a MessageTextContent
        assistant_output = last_text.text.value if last_text else ""

        self.project.agents.delete_agent(agent.id)

        # 5) Parse the concatenated JSON into your Pydantic model
        return ClassifiedMetricsList.model_validate(assistant_output)
