import logging
from research_agent.tools import semanticscholar

logger = logging.getLogger(__name__)

def query_scholar(search_string: str, year: str, minCitationCount: str) -> str:
    logger.debug(f"Searching for {search_string} in {year} with minCitationCount {minCitationCount}")
    search_results = semanticscholar.get_semantic_search(search_string, year, minCitationCount)
    return search_results
