BASE_SCANNER_SKILL_DESCRIPTION = """
Take a list of company names and query public APIs to fetch each firm’s region code, ticker (if public), and official website link.
It then outputs a clean, standardized JSON mapping of company names to these structured data fields.
"""

REGION_SPLIT_SKILL_DESCRIPTION = """
Takes in a flat JSON of company profiles (each with a region code) and groups them into separate JSON buckets keyed by region.
It outputs a nested JSON where each region maps to its companies (with the region field removed).
"""

INGESTION_SKILL_DESCRIPTION = """
Takes a region-filtered JSON of company profiles and enriches each entry by fetching financial, employee, and real estate metrics from public APIs and news sources.
It outputs a validated JSON where every company object is augmented with the specified metrics (or null if unavailable) for downstream scoring and analysis.
"""
CLASSIFICATION_SKILL_DESCRIPTION = """
Validate each company’s profile for completeness and then segregate its metrics into 3 arrays: financialMetrics, 
employeeMetrics, and realEstateMetrics.
"""

SIGNAL_AGENT_CLASSIFICATION = """
Analyze each company’s enriched metrics to calculate an “expansionConfidence” score and then recommend a new “expansionRegion” field based on peer expansion signals.
It outputs the original profiles augmented with these two fields for prioritized expansion targeting.
"""