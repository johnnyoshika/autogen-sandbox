# https://github.com/microsoft/autogen/blob/main/test/twoagent.py

import os
from dotenv import load_dotenv
# For 'import autogen' to work, had to 'pip install packaging'
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

# For some reason I need proxyman running and OPENAI_BASE_URL set to http://localhost:10800/v1 for this to work 🤷‍♂️
llm_config = {
    'model': 'gpt-4o',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}

assistant = AssistantAgent("assistant", llm_config=llm_config)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": True}
)

user_proxy.initiate_chat(
    assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
