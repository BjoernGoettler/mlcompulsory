import requests

def get_semantic_search(search_string: str):
    url = f"https://api.semanticscholar.org/graph/v1/paper/autocomplete?query={search_string}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching Semantic Scholar data: {response.status_code}")
    return response.json()