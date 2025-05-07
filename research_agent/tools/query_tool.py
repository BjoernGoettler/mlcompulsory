from autogen import AssistantAgent
from research_agent.config import LLM_CONFIG
from research_agent.tools import semanticscholar

def query_scholar(text: str) -> str:
    agent = AssistantAgent(
        name="Feedback Categorization Agent",
        system_message="You are a helpful AI assistant. "
                      "You can analyze the response from an API "
                      "Given a text, you can use the response tool to comment on the results. "
                      #"You will provide categorization result in the following format: '[theme]'. "
                      #"Example result: 'product'. "
                      #"Example of invalid result: 'theme is product'."
                      #"Theme can be 'product', 'service', or 'other'. "
                      "Don't include any other text in your response.",
                      #"Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    search_results = semanticscholar.get_semantic_search(text)

    reply = agent.generate_reply(
        messages=[
            {"role": "user", "content": f'Sort the search results: {search_results}'}
        ],
    )

    if not reply:
        raise ValueError("No reply found")

    reply_value = ""
    if isinstance(reply, dict):
        reply_content = reply["content"]
        if reply_content:
            reply_value = reply_content
        else:
            raise ValueError("No content found in the reply")
    else:
        reply_value = reply

    reply_values = reply_value.splitlines()
    if len(reply_values) != 1:
        reply_value = reply_values[0]

    reply_value = reply_value.replace("[", "").replace("]", "").replace(" ", "").strip()

    return reply_value