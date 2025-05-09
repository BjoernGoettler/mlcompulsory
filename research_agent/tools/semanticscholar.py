import requests

def get_semantic_search(search_string: str, year: str, minCitationCount: str):
    query_params = {
        "query": f'"{search_string}"',
        "fields": "title,url,publicationTypes,publicationDate,openAccessPdf",
        "year": f"-{year}",
        "minCitationCount": minCitationCount

    }
    url = f"https://api.semanticscholar.org/graph/v1/paper/autocomplete?query={search_string}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching Semantic Scholar data: {response.status_code}")
    return response.json()