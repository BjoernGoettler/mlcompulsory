from dotenv import load_dotenv, find_dotenv
from os import getenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

API_KEY = getenv("API_KEY")

LLM_CONFIG = {
    "config_list": [
        {
            "model": "open-mistral-nemo",
            "api_key": API_KEY,
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "repeat_penalty": 1.1,
            "temperature": 0.0,
            "seed": 42,
            "stream": False,
            "native_tool_calls": False,
            "cache_seed": None,
        }
    ]
}
