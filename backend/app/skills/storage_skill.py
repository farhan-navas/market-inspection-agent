import json
import asyncpg
from semantic_kernel.functions import kernel_function
from typing import List, Optional
from main import project, model, DB_CONNECTION_URL

import app.descriptions as descriptions
import app.prompts as prompts

from app.models.rationale_model import RationaleList

SQL_CREATE_TABLE = """
CREATE TABLE company_rankings (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  ticker TEXT,
  industry TEXT,
  region TEXT,
  total_score DOUBLE PRECISION,
  signals JSONB,
  rationale TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

class StorageSkill:
    def __init__(self, DB_CONNECTION_URL):
        self.project = project
        self.DB_CONNECTION_URL = DB_CONNECTION_URL

    @kernel_function(name="storage_companies", description=descriptions.STORAGE_SKILL_DESCRIPTION)
    async def agent_function(self, company_information_list: RationaleList) -> str:
        conn = await asyncpg.connect(self.DB_CONNECTION_URL)
        try:
            # 2) Use a transaction for safety & speed
            async with conn.transaction():
                for item in company_information_list.companies:
                    # Unpack your model (fields may vary)
                    name      = item.company.name
                    ticker    = item.company.ticker
                    industry = "HealthCare"
                    region    = Optional[item.company.region]
                    total_score = item.total_score
                    signals = {}
                    if isinstance(item.finance_metrics, dict):
                        signals.update(item.finance_metrics)
                    if isinstance(item.employee, dict):
                        signals.update(item.employee)
                    if isinstance(item.real_estate, dict):
                        signals.update(item.real_estate)

                    rationale = item.rationale if (item is not None or not hasattr(item, "rationale")) else ''

                    # 3) Upsert: insert or update on conflict (e.g. same ticker+region)
                    await conn.execute(
                        SQL_CREATE_TABLE,
                        name, ticker, industry, region, total_score, signals, rationale
                    )

            # 4) Finished!
            return f"✅ Stored {len(company_information_list.companies)} companies"
        finally:
            await conn.close()