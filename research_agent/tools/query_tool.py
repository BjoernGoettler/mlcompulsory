from research_agent.tools import semanticscholar

def query_scholar(search_string: str, year: str, minCitationCount: str) -> str:
    search_results = semanticscholar.get_semantic_search(search_string, year, minCitationCount)
    return search_results
