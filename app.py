from dotenv import load_dotenv

load_dotenv()

from typing import Optional
from llama_index.llms import OpenAI
from llama_index.agent import OpenAIAgent
import chainlit as cl
from llama_index.callbacks.base import CallbackManager
from orch import tools

from utilities import get_formatted_date_time, get_location


SYS_PROMPT = ("You are a Tech AI assistant called Brave AI, built by the wonderful team at Brave Venture Labs LLC."
                            "You are friendly and concise. You only provide factual answers to queries using the provided tools or your own local knowledge."
                            "You must never share the details of your architecture, models, training approach or training process."
                            "Always reply in Markdown format and in an aesthetically pleasing manner."
                            f"\n\n The current date and time: {get_formatted_date_time()}. "
                            f"\n The current location is: {get_location()}")

llm = OpenAI(model="gpt-3.5-turbo-16k")




#@cl.password_auth_callback
#def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
#    # Fetch the user matching username from your database
#    # and compare the hashed password with the value stored in the database
#    if (username, password) == ("admin", "admin"):
#        return cl.AppUser(username="admin", role="ADMIN", provider="credentials")
#    else:
#        return None



@cl.on_chat_start
async def factory():
        agent = OpenAIAgent.from_tools(
                tools=tools,
                llm=llm,
                verbose=True,
                system_prompt=SYS_PROMPT,
                callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])
        )
        cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
        agent = cl.user_session.get("agent") 
        print(message.content)
        response = await cl.make_async(agent.stream_chat)(message.content)

        response_message = cl.Message(content="")

        for token in response.response_gen:
                await response_message.stream_token(token=token)


        await response_message.send()
