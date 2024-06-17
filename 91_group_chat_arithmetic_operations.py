import os
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager

load_dotenv()

# For some reason I need proxyman running and OPENAI_BASE_URL set to http://localhost:10800/v1 for this to work 🤷‍♂️
llm_config = {
    'model': 'gpt-4',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}


# The Number Agent always returns the same numbers.
number_agent = ConversableAgent(
    name="Number_Agent",
    # GroupChatManager uses description to select the next agent when selection strategy is 'auto' (the default)
    description="Return the numbers given.",
    system_message="You return me the numbers I give you, one number each line.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Adder Agent adds 1 to each number it receives.
adder_agent = ConversableAgent(
    name="Adder_Agent",
    # GroupChatManager uses description to select the next agent when selection strategy is 'auto' (the default)
    description="Add 1 to each input number.",
    system_message="You add 1 to each number I give you and return me the new numbers, one number each line.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Multiplier Agent multiplies each number it receives by 2.
multiplier_agent = ConversableAgent(
    name="Multiplier_Agent",
    # GroupChatManager uses description to select the next agent when selection strategy is 'auto' (the default)
    description="Multiply each input number by 2.",
    system_message="You multiply each number I give you by 2 and return me the new numbers, one number each line.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Subtracter Agent subtracts 1 from each number it receives.
subtracter_agent = ConversableAgent(
    name="Subtracter_Agent",
    # GroupChatManager uses description to select the next agent when selection strategy is 'auto' (the default)
    description="Subtract 1 from each input number.",
    system_message="You subtract 1 from each number I give you and return me the new numbers, one number each line.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Divider Agent divides each number it receives by 2.
divider_agent = ConversableAgent(
    name="Divider_Agent",
    # GroupChatManager uses description to select the next agent when selection strategy is 'auto' (the default)
    description="Divide each input number by 2.",
    system_message="You divide each number I give you by 2 and return me the new numbers, one number each line.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

group_chat = GroupChat(
    agents=[adder_agent, multiplier_agent,
            subtracter_agent, divider_agent, number_agent],
    messages=[],
    max_round=6,
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
)

chat_result = number_agent.initiate_chat(
    group_chat_manager,
    message="My number is 3, I want to turn it into 13.",
    summary_method="reflection_with_llm",
)

print(chat_result.summary)
