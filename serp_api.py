import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_payload(query: str, location: str) -> str:
    """
    Create a payload for the search request.

    Args:
        query (str): The search query.
        location (str): The location for the search.

    Returns:
        str: The created payload in JSON format.
    """
    # Create a dictionary with the query and location
    payload = json.dumps({
        "q": query,
        "gl": location
    })
    return payload

def send_request(url: str, headers: dict, payload: str) -> requests.Response:
    """
    Send a POST request to the specified URL with the provided headers and payload.

    Args:
        url (str): The URL to send the request to.
        headers (dict): The headers for the request.
        payload (str): The payload for the request.

    Returns:
        requests.Response: The response from the server.
    """
    # Send a POST request to the server
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def search(query: str) -> dict:
    """
    Perform a Google search using the specified query.

    Args:
        query (str): The search query.

    Returns:
        dict: The search results.
    """
    # Define the URL and headers for the request
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': '21009d36e9d78792b627f923437715078b7522b1',
        'Content-Type': 'application/json'
    }
    # Create the payload for the request
    payload = create_payload(query, "ke")
    # Send the request and get the response
    response = send_request(url, headers, payload)
    # Log the response status code
    logging.info(f"Response status code: {response.status_code}")
    # Return the JSON content of the response
    return response.json()

if __name__ == "__main__":
    # Define the search query
    query = "Latest news on William Ruto"
    # Perform the search and print the results
    logging.info(f"Performing search for query: {query}")
    results = search(query)
    logging.info(f"Search results: {results}")
