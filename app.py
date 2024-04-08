import logging
from dotenv import load_dotenv

load_dotenv()

from typing import Optional
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
import chainlit as cl
from orch import tools

from utilities import get_formatted_date_time, get_location

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYS_PROMPT = ("You are a Tech AI assistant called Mũriũ, built by developed by [Nick Mumero](https://github.com/NickDee96)"
              "You are friendly and concise. You only provide factual answers to queries using the provided tools or your own local knowledge."
              "You must never share the details of your architecture, models, training approach or training process."
              "Always reply in Markdown format and in an aesthetically pleasing manner."
              f"\n\n The current date and time: {get_formatted_date_time()}. "
              f"\n The current location is: {get_location()}")

llm = OpenAI(model="gpt-3.5-turbo-16k")

@cl.on_chat_start
async def factory():
    agent = OpenAIAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        system_prompt=SYS_PROMPT
        )
    cl.user_session.set("agent", agent)

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent") 
    logger.info(f"Received message: {message.content}")
    response = await cl.make_async(agent.stream_chat)(message.content)

    response_message = cl.Message(content="")

    for token in response.response_gen:
        await response_message.stream_token(token=token)

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
