# https://microsoft.github.io/autogen/docs/tutorial/introduction

import os
from dotenv import load_dotenv
# For 'import autogen' to work, had to 'pip install packaging'
from autogen import ConversableAgent

load_dotenv()

cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={"config_list": [
        {
            "model": "gpt-4",
            "temperature": 0.9,
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL")
        }]},
    human_input_mode="NEVER",  # Never ask for human input.
)

joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={"config_list": [
        {
            "model": "gpt-4",
            "temperature": 0.7,
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL")
        }]},
    human_input_mode="NEVER",  # Never ask for human input.
)

# Set the max_turns to 3 to keep the conversation short
result = joe.initiate_chat(
    cathy, message="Cathy, tell me a joke.", max_turns=3)

print('result', result)
