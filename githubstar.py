import os
from openai import OpenAI
from composio_openai import ComposioToolSet, App, Action
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
composio_api_key = os.getenv("COMPOSIO_API_KEY")

# Debugging print statements to verify environment variables are loaded correctly
print(f"OpenAI API Key: {openai_api_key}")
print(f"Composio API Key: {composio_api_key}")

if not openai_api_key or not composio_api_key:
    raise ValueError("API key(s) not found. Ensure they are set in the .env file.")

openai_client = OpenAI(api_key=openai_api_key)

# Initialise the Composio Tool Set
composio_toolset = ComposioToolSet(api_key=composio_api_key)

# Get GitHub tools that are pre-configured
actions = composio_toolset.get_actions(actions=[Action.GITHUB_ACTIVITY_STAR_REPO_FOR_AUTHENTICATED_USER])

my_task = "Star a repo ComposioHQ/composio on GitHub"

# Setup openai assistant
assistant_instruction = "You are a super intelligent personal assistant"

assistant = openai_client.beta.assistants.create(
    name="composio",
    instructions=assistant_instruction,
    model="gpt-3.5-turbo-16k",
    tools=actions,  # type: ignore
)

# Create a thread
thread = openai_client.beta.threads.create()
message = openai_client.beta.threads.messages.create(thread_id=thread.id, role="user", content=my_task)

# Execute Agent with integrations
run = openai_client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

# Execute Function calls
response_after_tool_calls = composio_toolset.wait_and_handle_assistant_tool_calls(
    client=openai_client,
    run=run,
    thread=thread,
)

print(response_after_tool_calls)
