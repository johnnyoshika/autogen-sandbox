# See ./travel_agent/README.md for diagram of the workflow.
# Source: https://www.youtube.com/watch?v=bEld-pRTsO8
# Repo: https://github.com/john-adeojo/autogen_flights_tutorial

# Note: while this demonstrates how agents can be connected to form a workflow,
# it doesn't execute flawlessly because thew mocked function calls don't return
# relevant data. We end up with this message from senior_analyst:
#

import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

from travel_agent.function_calls import get_flight_data, run_sql
from travel_agent.messages import system_message_analyst, system_message_data_retriever, system_message_travel_agent, system_message_chat_manager, system_message_user_proxy, system_message_senior_analyst
from travel_agent.function_definitions import all_functions, get_flight_data_functions, run_sql_functions

load_dotenv()

# For some reason I need proxyman running and OPENAI_BASE_URL set to http://localhost:10800/v1 for this to work 🤷‍♂️
config_list = [{
    'model': 'gpt-4o',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}]

directory = '/Users/johnny/Downloads/instructor-help'

llm_config_user_proxy = {
    "functions": all_functions,
    "config_list": config_list,
    "seed": 100,
    "temperature": 0.7
}

llm_config_data_retriever = {
    "functions": get_flight_data_functions,
    "config_list": config_list,
    "seed": 100,
    "temperature": 0.7
}

llm_config_analyst = {
    "functions": run_sql_functions,
    "config_list": config_list,
    "seed": 100,
    "temperature": 0.7
}

llm_config_no_tools = {
    "config_list": config_list,
    "seed": 100,
    "temperature": 0.7
}

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    llm_config=llm_config_user_proxy,
    is_termination_msg=lambda x: x.get("content", "") and x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10,
    code_execution_config=False,
    system_message=system_message_user_proxy,
)

data_retriever = AssistantAgent(
    name="data_retriever",
    system_message=system_message_data_retriever,
    llm_config=llm_config_data_retriever
)

analyst = AssistantAgent(
    name="analyst",
    system_message=system_message_analyst,
    llm_config=llm_config_analyst,

)

travel_agent = AssistantAgent(
    name="travel_agent",
    system_message=system_message_travel_agent,
    llm_config=llm_config_no_tools,

)

senior_analyst = AssistantAgent(
    name="senior_analyst",
    system_message=system_message_senior_analyst,
    llm_config=llm_config_no_tools,

)

user_proxy.register_function(
    function_map={
        "get_flight_data": get_flight_data,
        "run_sql": run_sql,
    }
)

groupchat = GroupChat(
    agents=[user_proxy, data_retriever, analyst, travel_agent, senior_analyst],
    messages=[],
    max_round=30
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config_no_tools,
    is_termination_msg=lambda x: x.get("content", "") and x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    system_message=system_message_chat_manager
)

manager.initiate_chat(
    manager,
    message="Show me the cheapest flights from Sydney to Bangkok, leaving on the "
    "16th of December 2023 and returning on the 20th of May 2024."
)
