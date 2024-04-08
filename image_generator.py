import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
import pyshorteners
type_tiny = pyshorteners.Shortener()

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI()

def generate_image_prompt(text: str) -> str:
    """
    Generate an image prompt based on the input text.

    Args:
        text (str): The input text to generate an image prompt.

    Returns:
        str: The generated image prompt.
    """
    try:
        # Create a chat completion with the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced image prompt generator. You always return a finetuned prompt description of what the user wants."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Extract the content of the first choice
        chat_response = response.choices[0].message.content

        logger.info(f"Generated image prompt for input text: {text} with output text:\n {chat_response}")
        return chat_response
    except Exception as e:
        logger.error(f"Error generating image prompt for input text: {text}. Error: {e}")
        raise

def generate_image_url(prompt: str) -> str:
    """
    Generate an image URL based on the input prompt.

    Args:
        prompt (str): The input prompt to generate an image URL.

    Returns:
        str: The generated image URL.
    """
    try:
        # Generate an image with the OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        # Extract the URL of the first data
        image_url = response.data[0].url

        logger.info(f"Generated image URL for prompt: {prompt}")
        return image_url
    except Exception as e:
        logger.error(f"Error generating image URL for prompt: {prompt}. Error: {e}")
        raise






def generate_image(user_prompt: str) -> str:
    """
    Generate an image URL based on the user prompt.

    Args:
        user_prompt (str): The user prompt to generate an image URL.

    Returns:
        str: The generated image URL.
    """
    try:
        # Generate an image prompt based on the user prompt
        image_prompt = generate_image_prompt(user_prompt)
        # Generate an image URL based on the image prompt
        image_url = generate_image_url(image_prompt)
        short_image_url = type_tiny.tinyurl.short(image_url)

        logger.info(f"Generated image URL for user prompt: {user_prompt}")
        return short_image_url
    except Exception as e:
        logger.error(f"Error generating image for user prompt: {user_prompt}. Error: {e}")
        raise
