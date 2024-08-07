from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import html2text
from llama_index.core.tools import FunctionTool
#from serp_api import search
from image_generator import generate_image
from llama_index.tools.code_interpreter import CodeInterpreterToolSpec
from llama_index.tools.arxiv import ArxivToolSpec
from llama_index.core.tools.ondemand_loader_tool import OnDemandLoaderTool
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.agent.openai import OpenAIAgent
from llama_index.tools.exa import ExaToolSpec
from copy import copy
import os


exa_tool = ExaToolSpec(
    api_key = os.getenv("EXA_API_KEY"),
)

code_spec = CodeInterpreterToolSpec()

# Initialize DuckDuckGo Search
ddgs = DDGS()

reader = WikipediaReader()

def html_to_markdown(html_content: str) -> str:
    """
    Convert HTML content to Markdown.

    Args:
        html_content (str): HTML content to convert.

    Returns:
        str: Converted Markdown text.
    """
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove JavaScript code
    for script in soup(['script', 'style']):
        script.extract()

    # Get cleaned HTML content
    cleaned_html = str(soup)

    # Convert HTML to Markdown using html2text
    markdown_text = html2text.html2text(cleaned_html)

    return markdown_text


def search(query: str) -> list:
    """
    Perform a search engine query and return the results.

    Args:
        query (str): Search query.

    Returns:
        list: List of search results.
    """
    results = list(ddgs.text(query, max_results=10))
    return results

def crawl_site(link: str) -> str:
    """
    Crawl a website, retrieve its HTML content, and convert it to Markdown.

    Args:
        link (str): URL of the website to crawl.

    Returns:
        str: Converted Markdown text.
    """
    # Make a GET request to the website
    response = requests.get(link)

    # Convert HTML content to Markdown
    markdown_text = html_to_markdown(response.text)
    return markdown_text






def get_tools():
    tools = [
        #FunctionTool.from_defaults(fn = search),
        FunctionTool.from_defaults(fn = crawl_site),
        FunctionTool.from_defaults(fn = generate_image),
        OnDemandLoaderTool.from_defaults(
            reader,
            name="WikipediaTool",
            description="A tool for loading and querying articles from Wikipedia",
        )

    ]

    arxiv_codespec = ArxivToolSpec()

    #tools += code_spec.to_tool_list()
    tools += arxiv_codespec.to_tool_list()
    tools += exa_tool.to_tool_list()
    return copy(tools)