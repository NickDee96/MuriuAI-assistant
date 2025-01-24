"""
Chainlit-based AI Assistant application with OpenAI and Anthropic model support.
"""

import logging
import os
from typing import Optional

from dotenv import load_dotenv
import chainlit as cl
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic
from llama_index.agent.openai import OpenAIAgent
from chainlit.types import ThreadDict

from utilities import get_formatted_date_time, get_location
from orch import get_tools
from prompts import SYSTEM_PROMPT

# Initialize environment variables
load_dotenv(dotenv_path=".env", verbose=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



CHAT_PROFILES = [
    cl.ChatProfile(
        name="GPT-4o",
        markdown_description="The underlying LLM model is **GPT-4o**.",
        icon="https://zapier-images.imgix.net/storage/developer_cli/a86f51fcd659c4b311c82ba31a176e4a.png",
    ),
    cl.ChatProfile(
        name="Claude Sonnet",
        markdown_description="The underlying LLM model is **Claude Sonnet**.",
        icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRU7-NtcV60lEKC0XpS04K3ys9UJE-xpOI2GA&s",
    ),
]

def get_agent(model: str = os.getenv("MODEL_TYPE", "anthropic")) -> OpenAIAgent | FunctionCallingAgentWorker:
    """
    Initialize and return an AI agent based on the specified model type.
    
    Args:
        model (str): The model type to use ('openai' or 'anthropic')
        
    Returns:
        An instance of either OpenAIAgent or FunctionCallingAgentWorker
    """
    callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])
    
    if model == "openai":
        logger.info("Initializing OpenAI agent")
        Settings.llm = OpenAI(model="gpt-4o")
        return OpenAIAgent.from_tools(
            tools=get_tools(),
            verbose=True,
            system_prompt=SYSTEM_PROMPT,
            callback_manager=callback_manager
        )
    
    if model == "anthropic":
        logger.info("Initializing Anthropic agent")
        Settings.llm = Anthropic(model="claude-3-5-sonnet-latest")
        agent_worker = FunctionCallingAgentWorker.from_tools(
            tools=get_tools(),
            system_prompt=SYSTEM_PROMPT,
            verbose=True,
            allow_parallel_tool_calls=True,
            callback_manager=callback_manager
        )
        return agent_worker.as_agent()
    
    raise ValueError(f"Unsupported model type: {model}")

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """Authenticate users with username and password."""
    if (username, password) == ("admin", "admin"):
        return cl.User(identifier="admin", metadata={"role": "ADMIN"})
    return None

@cl.set_chat_profiles
async def chat_profile() -> list[cl.ChatProfile]:
    """Return available chat profiles."""
    return CHAT_PROFILES

@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialize chat session with selected profile."""
    chat_profile = cl.user_session.get("chat_profile")
    
    try:
        if chat_profile == "GPT-4o":
            agent = get_agent("openai")
        elif chat_profile == "Claude Sonnet":
            agent = get_agent("anthropic")
        else:
            raise ValueError(f"Invalid chat profile: {chat_profile}")
        
        agent.tools = get_tools
        cl.user_session.set("agent", agent)
        
        await cl.Message(
            content=f"Starting chat using the {chat_profile} chat profile"
        ).send()
        
    except Exception as e:
        logger.error(f"Error during chat initialization: {str(e)}")
        await cl.Message(content="Failed to initialize chat. Please try again.").send()

@cl.on_message
async def main(message: cl.Message) -> None:
    """Handle incoming chat messages."""
    agent = cl.user_session.get("agent")
    chat_profile = cl.user_session.get("chat_profile")
    
    try:
        logger.info(f"Received message: {message.content}")
        response_message = cl.Message(content="")
        
        if chat_profile == "GPT-4o":
            response = await cl.make_async(agent.stream_chat)(message.content)
            for token in response.response_gen:
                await response_message.stream_token(token=token)
        else:
            response = await cl.make_async(agent.chat)(message.content)
            await response_message.stream_token(response.response)
            
        await response_message.send()
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        await cl.Message(content="An error occurred while processing your message.").send()

@cl.on_stop
def on_stop() -> None:
    """Handle chat stop event."""
    logger.info("The user wants to stop the task!")

@cl.on_chat_end
def on_chat_end() -> None:
    """Handle chat end event."""
    logger.info("The user disconnected!")

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict) -> None:
    """Handle chat resume event."""
    logger.info("The user resumed a previous chat session!")
