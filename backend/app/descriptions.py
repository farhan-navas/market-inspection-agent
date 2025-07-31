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