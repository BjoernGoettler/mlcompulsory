from typing import Final
from autogen import ConversableAgent
from research_agent.tools.query_tool import query_scholar
from research_agent.config import LLM_CONFIG

MANDATORY_QUERY: Final[str] = "Find a research paper on [topic] that was published [in/before/after] [year] and has [number of citations] citations."

PROMPT_RESEARCH_QUERY = f"""
Read the following query and return a research paper that follows this example: "{MANDATORY_QUERY}"
The square brackets are placeholders for the actual topic, year, number of citations, etc.
You will ask the user to provide a topic, year, and number of citations.
You will ask the user if the year should be before, after or the exact year of publication
You can query the Semantic Scholar API using the query_scholar tool.
You can read the API response and return it
Don't include any other text in your response.
"""


def create_research_agent() -> ConversableAgent:
    # define the agent
    agent = ConversableAgent(
        name="Research Agent",
        system_message=f"""You are a helpful AI assistant.
                    You can help the user coin a search That follows this example: "{MANDATORY_QUERY}
                    The square brackets are placeholders for the actual topic, year, number of citations, etc.
                    You will ask the user to provide a topic, year, and number of citations.
                    You will ask the user if the year should be before, after or the exact year of publication
                    You can query the Semantic Scholar API using the query_scholar tool.
                    You can read the API response and return it
                    Don't include any other text in your response.
                    Return 'TERMINATE' when the task is done.""",
        llm_config=LLM_CONFIG,
    )

    # add the tools to the agent
    agent.register_for_llm(name="query_scholar", description="Read query response")(query_scholar)

    return agent

def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="ALWAYS",
    )
    user_proxy.register_for_execution(name="query_scholar")(query_scholar)
    return user_proxy


def main():
    prompt = PROMPT_RESEARCH_QUERY
    research_agent = create_research_agent()
    user_proxy = create_user_proxy()

    user_proxy.initiate_chat(
        research_agent,
        message=prompt
        )

    if __name__ == "__main__":
        main()
