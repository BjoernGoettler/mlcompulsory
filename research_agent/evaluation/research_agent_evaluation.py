import autogen
from research_agent.config import LLM_CONFIG
import rich
from rich.markdown import Markdown
from rich.console import Console

evaluation_prompts = [
    "Find a research paper on databases that was published before 2020  and has a minimum of 10 citations.",
    "Find a research paper on covid-19 that was published after 2019 and has a minimum of 10 citations.",
    "Find a research paper on something interesting that was published after the president was born and has a lot of citations."
    "Find a research paper on databases that has not been published yet and has a minimum of 10 citations."
    "Find a research paper on databases that was published before 2020  and has a negative amount of citations."
]

critic_agent = autogen.AssistantAgent(
    name="critic_agent",
    llm_config=LLM_CONFIG,
)

def evaluate_agent(agent, prompts: list[str]):
    console = Console()
    for prompt in prompts:
        agent_response = agent.generate_reply([{"role": "user", "content": prompt}])
        critic_prompt = f"""
        You are evaluating an AI product recommendation agent.
        
        Evaluate the response based on these criteria:
        - Completeness (1-5): addresses every part of the request.
        - Quality (1-5): accurate, clear, and effectively structured.
        - Robustness (1-5): handles ambiguities, errors, or nonsensical input well.
        - Consistency (1-5): maintains consistent reasoning with specified user needs.
        - Specificity (1-5): provides detailed and relevant recommendations with clear justifications.
        
        Additionally:
        - Check if the agent response provided clear context and justifications.
        - Determine if the agent accurately interpreted ambiguous prompts.
        - Assess realism, practicality, and feasibility of recommendations.
        
        User Prompt: {prompt}
        Agent Response: {agent_response}
        
        Provide your evaluation as raw JSON object with fields:
        - completeness
        - quality
        - robustness
        - consistency
        - specificity
        - feedback (a brief descriptive explanation including specific examples from the response)"""

        critic_evaluation = critic_agent.generate_reply([{"role": "user", "content": critic_prompt}])

        md = Markdown(critic_evaluation.get("content", ""))
        print(f"Evaluation of: {prompt}")

        console.print(md)

if __name__ == "__main__":
    evaluate_agent(critic_agent, evaluation_prompts)