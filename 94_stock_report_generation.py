# DeepLearning.AI
# Course: AI Agentic Design Patterns with AutoGen
# https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/7/planning-and-stock-report-generation

import os
from dotenv import load_dotenv
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, register_function
from autogen.coding import DockerCommandLineCodeExecutor
import datetime

load_dotenv()

llm_config = {
    'model': 'gpt-4o',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}

task = "Write a blogpost about the stock price performance of Nvidia in the past month. "
f"Today's date is {datetime.date.today().strftime('%Y-%m-%d')}."


user_proxy = ConversableAgent(
    name="Admin",
    system_message="Give the task, and send "
    "instructions to writer to refine the blog post.",
    code_execution_config=False,
    llm_config=llm_config,
    human_input_mode="ALWAYS",
)

# From https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/7/planning-and-stock-report-generation
planner = ConversableAgent(
    name="Planner",
    system_message="Given a task, please determine "
    "what information is needed to complete the task. "
    "Please note that the information will all be retrieved using"
    " Python code. Please only suggest information that can be "
    "retrieved using Python code. "
    "After each step is done by others, check the progress and "
    "instruct the remaining steps. If a step fails, try to "
    "workaround",
    description="Given a task, determine what "
    "information is needed to complete the task. "
    "After each step is done by others, check the progress and "
    "instruct the remaining steps",
    llm_config=llm_config,
)

# AssistantAgent is a subclass of ConversableAgent with human_input_mode=NEVER and code_execution_config=False.
# It also comes with default system_message and description fields. This class is a convenient short-cut for creating
# an agent that is intended to be used as a code writer and does not execute code.
# https://microsoft.github.io/autogen/docs/tutorial/code-executors#note-on-user-proxy-agent-and-assistant-agent
engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    description="Write code based on the plan "
    "provided by the planner.",
)

directory = '/Users/johnny/Downloads/instructor-help'

# Create a Docker command line code executor.
docker_executor = DockerCommandLineCodeExecutor(
    # Execute code using the given docker image name.
    image="python:3.12-slim",
    timeout=100,  # Timeout for each code execution in seconds.
    # Directory to store the code files.
    work_dir=directory,
)

# The course uses ConversableAgent but could have used UserProxyAgent instead if we wanted human_input_mode to be ALWAYS.
# UserProxyAgent is a subclass of ConversableAgent with human_input_mode=ALWAYS and llm_config=False.
# It also comes with default description field for each of the human_input_mode setting. This class is a convenient
# short-cut for creating an agent that is intended to be used as a code executor.
# https://microsoft.github.io/autogen/docs/tutorial/code-executors#note-on-user-proxy-agent-and-assistant-agent
executor = ConversableAgent(
    name="Executor",
    system_message="Execute the code written by the "
    "engineer and report the result.",
    description="Execute the code written by the "
    "engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "executor": docker_executor,  # In the course we didn't use Docker but we will here
        "last_n_messages": 3,
    },
)

writer = ConversableAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="Writer. "
    "Please write blogs in markdown format (with relevant titles)"
    " and put the content in pseudo ```md``` code block. "
    "You take feedback from the admin and refine your blog.",
    description="After all the info is available, "
    "write blogs based on the code execution results and take "
    "feedback from the admin to refine the blog. ",
)

groupchat = GroupChat(
    agents=[user_proxy, engineer, writer, executor, planner],
    messages=[],
    max_round=20,
    allowed_or_disallowed_speaker_transitions={
        user_proxy: [engineer, writer, executor, planner],
        engineer: [user_proxy, executor],
        writer: [user_proxy, planner],
        executor: [user_proxy, engineer, planner],
        planner: [user_proxy, engineer, writer],
    },
    speaker_transitions_type="allowed",
)

manager = GroupChatManager(
    groupchat=groupchat, llm_config=llm_config
)

groupchat_result = user_proxy.initiate_chat(
    manager,
    message=task,
)
