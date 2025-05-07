import logging
from copy import deepcopy
from typing import Final
from autogen import ConversableAgent
from research_agent.tools.query_tool import query_scholar
from research_agent.config import LLM_CONFIG
from research_agent.logging_configuration import setup_logging

setup_logging(log_file="research_agent.log")

logger = logging.getLogger(__name__)



MANDATORY_QUERY: Final[str] = "Find a research paper on [topic] that was published [in/before/after] [year] and has [number of citations] citations."

PROMPT_RESEARCH_QUERY = f"""
Please help find research papers based on specific criteria.
You will:
1. Ask for a research topic
2. Ask for a year preference (in/before/after)
3. Ask for minimum number of citations
4. Use the query_scholar tool to search
5. Present the results


Format: "{MANDATORY_QUERY}"
"""


def create_research_agent() -> ConversableAgent:
    # define the agent
    logger.debug("Creating research agent")
    config = deepcopy(LLM_CONFIG)
    if "functions" not in config:
        config["functions"] = []

    config["functions"].append({
        "name": "query_scholar",
        "description": "A new tool added at runtime",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "Research topic"},
                "param2": {"type": "integer", "description": "research year"},
                "param3": {"type": "integer", "description": "minimum number of citations"},
            },
            "required": ["param1", "param2", "param3"],
        }
    })
    logger.debug(f"config: {config}")

    agent = ConversableAgent(
        name="Research Agent",
        system_message=f"""You are a research assistant that helps find academic papers.
                    You will guide users through a search process following this format: {MANDATORY_QUERY}
                    Ask for each piece of information separately:
                    1. Research topic
                    2. Year preference (in/before/after)
                    3. Minimum citations
                    Use the query_scholar tool only after collecting all information.
                    Return 'TERMINATE' after providing search results.""",

        llm_config=config,
        human_input_mode="NEVER",
        function_map={"query_scholar": query_scholar},
    )

    # add the tools to the agent
    agent.register_for_llm(name="query_scholar", description="Search for academic papers")(query_scholar)
    logger.info("Research agent created")

    return agent


def create_user_proxy():
    logger.debug("Creating user proxy")
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="ALWAYS",
    )
    #user_proxy.register_for_execution(name="query_scholar")(query_scholar)
    logger.info("User proxy created")
    return user_proxy


def main():
    logger.info("Starting research agent")
    prompt = PROMPT_RESEARCH_QUERY
    research_agent = create_research_agent()
    user_proxy = create_user_proxy()

    logger.info("Starting chat")
    user_proxy.initiate_chat(
         research_agent,
         message=prompt
         )


if __name__ == "__main__":
    logger.info("Going off!")
    main()
