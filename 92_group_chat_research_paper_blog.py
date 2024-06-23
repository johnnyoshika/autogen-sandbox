import os
from dotenv import load_dotenv
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, register_function
from autogen.coding import DockerCommandLineCodeExecutor
from tools.search_arxiv import search_arxiv

load_dotenv()

# For some reason I need proxyman running and OPENAI_BASE_URL set to http://localhost:10800/v1 for this to work 🤷‍♂️
llm_config = {
    'model': 'gpt-4o',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': os.getenv('OPENAI_BASE_URL') if os.getenv('OPENAI_BASE_URL') else None,
}

directory = '/Users/johnny/Downloads/instructor-help'

product_manager_agent = ConversableAgent(
    "product_manager_agent",
    description="product_manager_agent is an AI agent designed to give directives.",
    llm_config=False,
    human_input_mode="NEVER",
)


code_writer_agent = AssistantAgent(
    "code_writer_agent",
    llm_config=llm_config,
)

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

paper_extractor_agent = ConversableAgent(
    "paper_extractor_agent",
    description="paper_extractor is an AI agent designed to read academic papers and extract the main key takeaways in a detailed and comprehensive manner. "
    "The extracted information serves as a solid foundation for creating insightful and well-informed blog posts, ensuring that complex research findings are accessible and understandable.",
    system_message="You are paper_extractor, an AI agent dedicated to reading academic papers and pulling out the main key takeaways. "
    "Your task is to provide thorough and detailed summaries that encapsulate the core findings, methodologies, and implications of the research. "
    "These summaries should be clear and comprehensive, serving as a strong foundation for blog posts that communicate complex scientific concepts to a broader audience.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

blog_creator_agent = ConversableAgent(
    "blog_creator_agent",
    description="blog_creator_agent is an AI agent designed to transform detailed summaries of academic papers into engaging, professional, and thought-provoking "
    "blog posts. It ensures that complex research findings are communicated in an accessible and captivating manner, suitable for a broad audience.",
    system_message="You are blog_creator_agent, an AI agent tasked with converting detailed summaries of academic papers into engaging and professional blog posts. "
    "Your goal is to create content that is not only informative but also captivating and thought-provoking. Use clear and compelling language to ensure "
    "the blog posts are accessible to a wide audience while maintaining a high standard of professionalism and engagement.",
    llm_config=llm_config,
)

blog_critic_agent = ConversableAgent(
    "blog_critic_agent",
    description="blog_critic is an AI agent specialized in evaluating the quality of written blog posts to determine if they meet high publication standards. "
    "If the blog post is deemed to be of insufficient quality, the agent provides constructive feedback to help improve the content. "
    "If the blog post meets the high standards, the agent confirms its readiness for publication.",
    system_message="You are blog_critic, an AI agent responsible for critiquing written blog posts to ensure they meet high publication standards. "
    "Your task is to thoroughly evaluate the quality of the content, including its clarity, engagement, professionalism, and thoughtfulness. "
    "If a blog post does not meet the necessary standards, provide constructive feedback to guide the writer in improving it. "
    "If the blog post is of high quality, confirm its readiness for publication.",
    llm_config=llm_config,
)

blog_publish_agent = ConversableAgent(
    "blog_publish_agent",
    description="blog_publisher is an AI agent responsible for taking the approved blog post and preparing it for publication. It ensures that the final content is ready for distribution and returns it for posting.",
    system_message="You are blog_publisher, an AI agent tasked with taking the approved blog post and preparing it for publication. Your role is to ensure the final content is polished and ready for distribution. Once confirmed, return the blog post for posting.",
    llm_config=llm_config,
)

register_function(
    search_arxiv,
    # code_writer_agent can suggest calls to the search_arxiv tool.
    caller=code_writer_agent,
    # code_executor_agent can execute search_arxiv calls.
    executor=code_executor_agent,
    description="Search arXiv for the given query using the arXiv API, then return the search results.",
)

allowed_transitions = {
    product_manager_agent: [code_writer_agent],
    code_executor_agent: [code_writer_agent, paper_extractor_agent],
    code_writer_agent: [code_executor_agent],
    paper_extractor_agent: [blog_creator_agent],
    blog_creator_agent: [blog_critic_agent],
    blog_critic_agent: [blog_creator_agent, blog_publish_agent],
}

group_chat = GroupChat(
    description="A comprehensive workflow that integrates multiple specialized AI agents to transform academic research into high-quality, engaging blog posts. "
    "The process begins with product_manager_agent, who instructs code_writer_agent to write Python code to search for and find relevant research articles on arXiv. "
    "code_executor_agent then executes this code to retrieve the search results. Human intervenes and picks the most interesting article. "
    "code_writer_agent writes Python code to download the selected research paper, and code_executor_agent is called to execute this code. "
    "Anytime code_executor_agent executes code, the results are sent back to code_writer_agent to determine if the task was successful. "
    "If the execution is not successful, code_writer_agent amends its code and passes them back to code_executor_agent for another attempt. "
    "Once the code is executed successfully, the next agent is called upon.  Once the research paper is successfully downloaded, paper_extractor_agent "
    "reads it and extracts detailed key takeaways. Using these key takeaways, blog_creator_agent crafts a professional, engaging, and thought-provoking blog post. "
    "blog_critic_agent then evaluates the blog post to ensure it meets high publication standards. If the blog post does not meet the necessary standards, "
    "blog_critic_agent provides constructive feedback to blog_creator_agent to make improvements. This iterative process continues between "
    "blog_critic_agent and blog_creator_agent until blog_critic_agent approves the blog post for publication. Finally, blog_publish_agent takes the approved blog post "
    "and prepares it for distribution, ensuring the final content is ready for posting.",
    agents=[product_manager_agent, code_writer_agent, code_executor_agent, paper_extractor_agent, blog_creator_agent, blog_critic_agent,
            blog_publish_agent],
    messages=[],
    max_round=20,
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
)

group_chat_manager = GroupChatManager(
    description="group_chat_manager is an AI agent responsible for coordinating and managing the workflow of multiple specialized AI agents within the Academic to "
    "Blog Pipeline. It ensures smooth communication, task delegation, and monitors the progress of each task. group_chat_manager facilitates the seamless transition of "
    "tasks from one agent to another, verifying the successful completion of each step before moving forward. This includes managing the iterative process between "
    "code_writer_agent and code_executor_agent for code execution and adjustments, as well as the iterative feedback loop between blog_creator_agent and blog_critic_agent "
    "for refining blog posts. The agent oversees the entire process, from the initial search for relevant research articles to the final preparation of blog posts for "
    "publication, ensuring efficiency, accuracy, and high-quality output.",
    groupchat=group_chat,
    llm_config=llm_config,
)

chat_result = product_manager_agent.initiate_chat(
    group_chat_manager,
    message='Find academic research reports related to "Optimization of Battery Management Systems for Enhanced Performance and Longevity in Electric Vehicles." '
    'Pick the most relevant ones and create an engaging and thought-provoking blog post. Ensure the blog post is critiqued and reviewed before publishing it.',
    summary_method="reflection_with_llm",
)

print(chat_result.summary)
