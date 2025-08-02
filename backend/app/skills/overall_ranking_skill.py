import json
from semantic_kernel.functions import kernel_function
from main import project, model

import app.descriptions as descriptions
import app.prompts as prompts

from app.models.expansion_eval_model import ExpansionEvalCompanyList
from app.models.overall_ranking_model import OverallRankingList

from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, MessageRole

class OverallRankingSkill:
    def __init__(self):
        self.project = project

    @kernel_function(name="rank_companies", description=descriptions.OVERALL_SCORING_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: ExpansionEvalCompanyList) -> OverallRankingList:
        agent_id = "rank_companies"

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
        return OverallRankingList.model_validate(assistant_output)