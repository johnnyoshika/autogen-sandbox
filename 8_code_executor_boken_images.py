# This is a continuation of 7_code_executor_links.py

import os
from dotenv import load_dotenv
# For 'import autogen' to work, had to 'pip install packaging'
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

load_dotenv()

# For some reason I need proxyman running and OPENAI_BASE_URL set to http://localhost:10800/v1 for this to work 🤷‍♂️
llm_config = {
    'model': 'gpt-4o',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}


directory = '/Users/johnny/Downloads/instructor-help'

# Create a Docker command line code executor.
executor = DockerCommandLineCodeExecutor(
    # Execute code using the given docker image name.
    image="python:3.12-slim",
    timeout=100,  # Timeout for each code execution in seconds.
    # Use the temporary directory to store the code files.
    work_dir=directory,
)

code_executor_agent = UserProxyAgent(
    "code_executor_agent",
    # Use the docker command line code executor.
    code_execution_config={"executor": executor},
)

code_writer_agent = AssistantAgent(
    "code_writer_agent",
    llm_config=llm_config,
)

website = 'https://instructor-help.examind.io/'

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message="Write Python code to read links.json in the directory, "
    "scrape each link in the links.json file, and find all img src attribute values. "
    f"Keep track of all src values that aren't either absolute {website} paths or relative paths. "
    "Continue this process for every link in the links.json file. "
    "Save all tracked src along with the page URL where it's located to a file named images.json in JSON format."
)

# When the code executor is no longer used, stop it to release the resources.
# executor.stop()
