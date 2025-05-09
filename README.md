# Machine Learning Compulsary 2

Start by installing the requirements:

```bash
pip install -r requirements.txt
```

Set yor API key in a file called .env

```
API_KEY="This is where you put your key"
```

Have a chat with the agent, and get to know more about research topics of your own choice
```bash
python -m research_agent.agent.research_response_agent
```

You can evaluate the agent by using it's critic-agent
```bash
python -m research_agent.evaluation.research_agent_evaluation
```
