import argparse
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
                    Don't include any other text in your response.""",
        llm_config=LLM_CONFIG,
    )

    # add the tools to the agent
    agent.register_for_llm(name="query_scholar", description="Read customer feedback")(query_scholar)

    return agent

def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    user_proxy.register_for_execution(name="feedback_reader")(query_feedback)
    user_proxy.register_for_execution(name="sentiment_analysis")(analyze_sentiment)
    user_proxy.register_for_execution(name="categorization")(categorize_feedback)
    user_proxy.register_for_execution(name="keyword_extraction")(extract_keywords)
    return user_proxy


    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("--mode", choices=["sentiment_analysis", "keyword_extraction", "categorization", "categorize_and_extract_keywords"], required=True, default="sentiment_analysis")
        args = parser.parse_args()

        prompt = None
        if args.mode == "sentiment_analysis":
            prompt = PROMPT_SENTIMENT_ANALYSIS
        elif args.mode == "keyword_extraction":
            prompt = PROMPT_KEYWORD_EXTRACTION
        elif args.mode == "categorization":
            prompt = PROMPT_CATEGORIZATION
        elif args.mode == "categorize_and_extract_keywords":
            prompt = PROMPT_CATEGORIZE_AND_EXTRACT_KEYWORDS

        user_proxy = create_user_proxy()
        feedback_analysis_agent = create_feedback_analysis_agent()
        user_proxy.initiate_chat(
            feedback_analysis_agent,
            message=prompt
        )

    if __name__ == "__main__":
        main()
