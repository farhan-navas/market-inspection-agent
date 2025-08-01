import json
from semantic_kernel.functions import kernel_function
from typing import List
from main import project, model

import backend.app.descriptions as descriptions
import backend.app.prompts as prompts

from app.models.scoring_model import MetricRankingList
from backend.app.models.expansion_eval_model import ExpansionEvalCompanyList

from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, MessageRole, BingGroundingTool

class ExpansionEvalSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="evaluate_expansion_companies", description=descriptions.EXPANSION_EVALUATION_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: MetricRankingList) -> ExpansionEvalCompanyList:
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
        return ExpansionEvalCompanyList.model_validate(assistant_output)
     