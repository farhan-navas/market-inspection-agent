import json 
from semantic_kernel.functions import kernel_function
from typing import List
from main import project, model

import backend.app.descriptions as descriptions
import backend.app.prompts as prompts

from app.models.company_models import BaseScannerList
from app.models.region_split_model import RegionSplitList
from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, MessageRole

class RegionSplitSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="region_split_companies", description=descriptions.INGESTION_SKILL_DESCRIPTION)
    async def region_split_companies(self, company_information_list: BaseScannerList) -> RegionSplitList:
        agent_id = "region_split_companies"

        agent = self.project.agents.create_agent(
            model=model,
            name="BaseScannerAgent",
            instructions=prompts.BASE_SCANNER_SKILL_PROMPT,
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
            )
        )

        last_text = self.project.agents.messages.get_last_message_text_by_role(
            thread_id=thread_run.thread_id,
            role=MessageRole("assistant")
        )

        # last_text is a MessageTextContent
        assistant_output = last_text.text.value if last_text else ""

        # delete agent
        self.project.agents.delete_agent(agent.id)

        # 5) Parse the concatenated JSON into your Pydantic model
        return RegionSplitList.model_validate(assistant_output)
                                                