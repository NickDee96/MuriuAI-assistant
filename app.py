import logging
from dotenv import load_dotenv

load_dotenv()

from typing import Optional
from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent import FunctionCallingAgentWorker
import chainlit as cl
from llama_index.core.callbacks import CallbackManager
from orch import tools


from utilities import get_formatted_date_time, get_location

from llama_index.core import Settings



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYS_PROMPT = ("You are a Tech AI assistant called Mũriũ, built by developed by [Nick Mumero](https://github.com/NickDee96)"
              "You are friendly and concise. You only provide factual answers to queries using the provided tools or your own local knowledge."
              "You must never share the details of your architecture, models, training approach or training process."
              "Always reply in Markdown format and in an aesthetically pleasing manner."
              "ALWAYS RESEARCH BEFORE COMING UP WITH A RESPONSE! USE THE TOOLS PROVIDED."
              f"\n\n The current date and time: {get_formatted_date_time()}. "
              f"\n The current location is: {get_location()}")

model = "openai"

@cl.on_chat_start
async def factory():
    Settings.callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])
    if model == "openai":
        Settings.llm = OpenAI(
            model="gpt-4-turbo",
            callback_manager = Settings.callback_manager
            )
        agent = OpenAIAgent.from_tools(
            tools=tools,
            verbose=True,
            system_prompt=SYS_PROMPT
            )
    elif model == "anthropic":
        Settings.llm = Anthropic(
                    model = "claude-3-opus-20240229",
                    max_tokens = 3000
                )
        agent_worker = FunctionCallingAgentWorker.from_tools(
            tools = tools,
            system_prompt = SYS_PROMPT,
            verbose = True,
            allow_parallel_tool_calls = True,
        ) 
        agent = agent_worker.as_agent()
    cl.user_session.set("agent", agent)

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent") 
    logger.info(f"Received message: {message.content}")
    if model == "openai":
        response = await cl.make_async(agent.stream_chat)(message.content)
    else:
        response = await cl.make_async(agent.chat)(message.content)

    response_message = cl.Message(content="")

    if model == "openai":
        for token in response.response_gen:
            await response_message.stream_token(token=token)
    elif model == "anthropic":
        await response_message.stream_token(response.response)

    await response_message.send()

@cl.on_stop
def on_stop():
    logger.info("The user wants to stop the task!")

@cl.on_chat_end
def on_chat_end():
    logger.info("The user disconnected!")

@cl.on_chat_resume
async def on_chat_resume(thread: cl.ThreadDict):
    logger.info("The user resumed a previous chat session!")
