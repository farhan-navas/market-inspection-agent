from semantic_kernel.functions import kernel_function
from typing import Optional
from main import project, model

import backend.app.descriptions as descriptions
import backend.app.prompts as prompts

from app.models.company_models import CompanyInformation, BaseScannerList

from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, MessageRole, BingGroundingTool

class BaseScannerSkill:    
    def __init__(self):
        self.project = project

    @kernel_function(
            name="fetch_companies", 
            description=descriptions.BASE_SCANNER_SKILL_DESCRIPTION
    )
    async def agent_function(self, industry: str) -> BaseScannerList:
        agent_id = "fetch_companies"
        bing_connection_id = "ba8921d52eda4f1181179f811192358b"

        bing = BingGroundingTool(connection_id=bing_connection_id)

        agent = self.project.agents.create_agent(
            model=model,
            name="BaseScannerAgent",
            instructions=prompts.BASE_SCANNER_SKILL_PROMPT,
            tools=bing.definitions,
        )

        print(f"agent has been successfully created with id: {agent.id}")

        thread_run = self.project.agents.create_thread_and_process_run(
            agent_id=agent_id,
            thread=AgentThreadCreationOptions(
                messages=[
                        ThreadMessageOptions(
                        role="user",
                        content=(
                            f"Please list all companies in industry={industry} in one reponse"
                        )
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
        return BaseScannerList.model_validate(assistant_output)
                                          