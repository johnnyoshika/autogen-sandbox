# https://microsoft.github.io/autogen/docs/tutorial/code-executors/

import os
from dotenv import load_dotenv
import tempfile
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


# Create a temporary directory to store the code files.
# On macOS, the temporary directory gets created here and is automatically deleted when this script finishes.
# /private/var/folders/pz/{random_string}/T/tmp{random_string}
temp_dir = tempfile.TemporaryDirectory()

# Create a Docker command line code executor.
executor = DockerCommandLineCodeExecutor(
    # Execute code using the given docker image name.
    image="python:3.12-slim",
    timeout=10,  # Timeout for each code execution in seconds.
    # Use the temporary directory to store the code files.
    work_dir=temp_dir.name,
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

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message="Write Python code to calculate the 14th Fibonacci number.",
)

# Creates a file called calculate_fibonacci.py:
# ----------------------------------------------------
# ➜  tmpmzcowkow ls -al
# total 8
# drwx------    3 johnny  staff     96 31 May 08:07 .
# drwx------@ 402 johnny  staff  12864 31 May 08:07 ..
# -rw-r--r--    1 johnny  staff    240 31 May 08:07 calculate_fibonacci.py
# ➜  tmpmzcowkow cat calculate_fibonacci.py
# # filename: calculate_fibonacci.py

# def fibonacci(n):
#     a, b = 0, 1
#     for _ in range(n):
#         a, b = b, a + b
#     return a

# # Calculate the 14th Fibonacci number
# fib_14 = fibonacci(14)
# print(f"The 14th Fibonacci number is: {fib_14}")%
# ----------------------------------------------------


# When the code executor is no longer used, stop it to release the resources.
# executor.stop()
