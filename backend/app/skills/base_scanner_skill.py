from semantic_kernel.functions import kernel_function
from typing import Optional
from main import project, model

import backend.app.descriptions as descriptions
import backend.app.prompts as prompts

from app.models.company_models import CompanyInformation, BaseScannerList
from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, MessageRole

class BaseScannerSkill:    
    def __init__(self):
        self.project = project
        self.agents_client = self.project.agents

    @kernel_function(
            name="fetch_companies", 
            description=descriptions.BASE_SCANNER_SKILL_DESCRIPTION
    )
    async def agent_function(self, industry: str, region: Optional[str], country: Optional[str]) -> BaseScannerList:
        agent_id = "fetch_companies"

        thread_run = self.agents_client.create_thread_and_process_run(
            agent_id=agent_id,
            model=model,
            instructions=prompts.BASE_SCANNER_SKILL_PROMPT,
            thread=AgentThreadCreationOptions(
                messages=[
                        ThreadMessageOptions(
                        role="user",
                        content=(
                            f"Please list all companies in industry={industry}, "
                        )
                    )
                ]
            )
        )

        last_text = self.agents_client.messages.get_last_message_text_by_role(
            thread_id=thread_run.thread_id,
            role=MessageRole("assistant")
        )
        # last_text is a MessageTextContent
        assistant_output = last_text.text.value if last_text else ""

        # 5) Parse the concatenated JSON into your Pydantic model
        return BaseScannerList.model_validate(assistant_output)



        


                                                