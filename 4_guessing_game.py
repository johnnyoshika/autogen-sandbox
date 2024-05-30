# https://microsoft.github.io/autogen/docs/tutorial/human-in-the-loop

import os
from dotenv import load_dotenv
# For 'import autogen' to work, had to 'pip install packaging'
from autogen import ConversableAgent

load_dotenv()

# For some reason I need proxyman running and OPENAI_BASE_URL set to http://localhost:10800/v1 for this to work 🤷‍♂️
llm_config = {
    'model': 'gpt-4o',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}

agent_with_number = ConversableAgent(
    "agent_with_number",
    system_message="You are playing a game of guess-my-number. You have the "
    "number 53 in your mind, and I will try to guess it. "
    "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
    llm_config=llm_config,
    # terminate if the number is guessed by the other agent
    is_termination_msg=lambda msg: "53" in msg["content"],
    human_input_mode="NEVER",  # never ask for human input
)

agent_guess_number = ConversableAgent(
    "agent_guess_number",
    system_message="I have a number in my mind, and you will try to guess it. "
    "If I say 'too high', you should guess a lower number. If I say 'too low', "
    "you should guess a higher number. ",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

result = agent_with_number.initiate_chat(
    agent_guess_number,
    message="I have a number between 1 and 100. Guess it!",
)
