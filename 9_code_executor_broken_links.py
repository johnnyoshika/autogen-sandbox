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

# Note: when running this, I had to steer it a few times with the following feedback, but the end result was perfect:
# "Oh, we also need to know where these broken links are linked from"
# "can you also produce a csv file?"
# "Could we also get the text that's hyperlinked to the broken link?"

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=f"Write Python code to scrape the webpage at {website}, "
    f"find all absolute links that start with {website} or relative links, "
    "and convert relative links to absolute fully qualified links. "
    f"Follow these links and find more links that are either absolute {website} links or relative links. "
    "Continue this process recursively until no more relevant links are found. "
    "Do not follow links that have already been crawled. "
    "Keep track of all broken links (i.e. a link that results in a 404 error when requested), "
    "and save those broken links to a file named broken_links.json in JSON format. "
)

# When the code executor is no longer used, stop it to release the resources.
# executor.stop()
