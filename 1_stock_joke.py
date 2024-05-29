# https://microsoft.github.io/autogen/docs/Getting-Started

import os
from dotenv import load_dotenv
# For 'import autogen' to work, had to 'pip install packaging'
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

llm_config = {
    'model': 'gpt-4o',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}

assistant = AssistantAgent(
    'assistant',
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    'user_proxy',
    code_execution_config=False
)

user_proxy.initiate_chat(
    assistant,
    message='Tell me a joke about NVDA and TESLA stock prices.',
)
