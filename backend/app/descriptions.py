BASE_SCANNER_SKILL_DESCRIPTION = """
Take a list of company names and query public APIs to fetch each firm’s region code, ticker (if public), and official website link.
It then outputs a clean, standardized JSON mapping of company names to these structured data fields.
"""

REGION_SPLIT_SKILL_DESCRIPTION = """
Take in a flat JSON of company profiles (each with a region code) and groups them into separate JSON buckets keyed by region.
It outputs a nested JSON where each region maps to its companies (with the region field removed).
"""

INGESTION_SKILL_DESCRIPTION = """
Take in a region-filtered JSON of company profiles and enriches each entry by fetching financial, employee, and real estate metrics from public APIs and news sources.
It outputs a validated JSON where every company object is augmented with the specified metrics (or null if unavailable) for downstream scoring and analysis.
"""
CLASSIFICATION_SKILL_DESCRIPTION = """
Validate each company’s profile for completeness and then segregate its metrics into 3 arrays: financialMetrics, 
employeeMetrics, and realEstateMetrics.
"""

SCORING_SKILL_PROMPT = """
Take in all companies in a region, normalizes each metric against that cohort’s 5th and 95th percentiles, and then aggregates them into three 0–100 scores — 
financialScore, employeeScore, and realEstateScore—for easy comparison and prioritization
"""

EXPANSION_EVALUATION_SKILL_DESCRIPTION = """
Analyze each company’s enriched metrics to calculate an “expansionConfidence” score and then recommend a new “expansionRegion” field based on peer expansion signals.
It outputs the original profiles augmented with these two fields for prioritized expansion targeting.
"""

MERGE_SKILL_DESCRIPTION = """
Consolidate multiple region-specific company score buckets into one unified dataset, tagging each company with its region and preserving all category scores.
"""

OVERALL_SCORING_SKILL_DESCRIPTION = """
Combine each company’s financial, employee, and real estate scores using the provided metricScoringWeightage to compute a single overallScore (0–100). Then outputs 
a clean JSON dictionary mapping each company name to its rounded overallScore for final prioritization
"""

RATIONALE_SKILL_DESCRIPTION = """
Filter for the top 500 companies by overallScore and then generates a structured, multi-section narrative for each—starting with an overall summary, 
followed by category-level analyses, and concluding with metric-by-metric explanations—to provide clear, in-depth insights
"""

STORAGE_SKILL_DESCRIPTION = """
Persist each company’s complete profile into a SQL database via upsert statements and simultaneously indexes their key textual content (e.g., rationale and top metrics) into a vector database for fast semantic retrieval
"""

# retrieval agents
RETRIEVAL_CHAT_SKILL_DESCRIPTION = """
Listen to a user’s natural-language request, translates it into structured filter criteria, invokes the Retrieval Form Agent, and presents the matching companies back in conversational form
"""

RETRIVAL_FORM_SKILL_DESCRIPTION = """
Receive a JSON payload of filter parameters, queries the persisted company dataset for all matching records, and returns the full profiles as a JSON array
"""