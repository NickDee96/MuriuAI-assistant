# Mũriũ AI Assistant

Mũriũ AI Assistant is an intelligent tech assistant developed by Nick Mumero. It provides factual answers to queries using advanced language models and powerful tools. This readme document explains the logic of how everything works and provides instructions for setting up the project.

## File Structure

```
MuriuAI-assistant
├── .chainlit/
│   └── config.toml
├── .files/
├── .env
├── .gitignore
├── app.py
├── chainlit.md
├── Dockerfile
├── image_generator.py
├── orch.py
├── requirements.txt
├── serp_api.py
├── test.py
└── utilities.py
```

## Logic and Functionality

The Mũriũ AI Assistant project consists of several files and modules that work together to provide the desired functionality. Here's an overview of how everything works:

1. `app.py`: This is the main file of the project. It initializes the OpenAI language model, sets up the system prompt, and handles incoming messages from the user. It uses the `llama_index` library to create an OpenAIAgent and process the user's queries.

2. `chainlit.md`: This file contains the documentation for the Mũriũ AI Assistant. It explains the features of the assistant, such as Google Search, Web Crawling, and Photo Generation.

3. `Dockerfile`: This file is used to build a Docker image for the Mũriũ AI Assistant. It sets up the Python environment, installs the required dependencies from `requirements.txt`, and specifies the command to run the `app.py` file.

4. `image_generator.py`: This file contains the logic for generating images using OpenAI's models and APIs. It defines functions to generate image prompts and image URLs based on user prompts. It also includes logging to record information and errors during the process.

5. `orch.py`: This file contains utility functions for performing web crawling, converting HTML to Markdown, and searching using the SERP API. It uses the `BeautifulSoup` and `html2text` libraries for HTML parsing and conversion.

6. `serp_api.py`: This file provides a function to perform a Google search using the SERP API. It sends a POST request to the API endpoint with the search query and location, and returns the search results in JSON format.

7. `utilities.py`: This file contains utility functions for getting the current date and time in a formatted string, and getting the current location using the `geocoder` library.

## Setup Process

To set up the Mũriũ AI Assistant project, follow these steps:

1. Clone the project repository to your local machine.

2. Make sure you have Docker installed on your machine.

3. Open a terminal or command prompt and navigate to the project directory.

4. Build the Docker image using the following command:
   ```
   docker build -t muriu-ai-assistant .
   ```

5. Run the Docker container using the following command:
   ```
   docker run -p 8000:8000 muriu-ai-assistant
   ```

6. The Mũriũ AI Assistant will now be running on `http://localhost:8000`. You can access it using a web browser or send requests programmatically.

7. Interact with the Mũriũ AI Assistant by sending messages or queries. The assistant will provide factual answers using the provided tools and local knowledge.

That's it! You have successfully set up and run the Mũriũ AI Assistant project using Docker.

## Usage Guidelines

1. Conciseness: The Mũriũ AI Assistant is designed to be concise and to the point. It prioritizes clarity and efficiency in its responses.

2. Factual Answers: The assistant's responses are based on factual information obtained from reliable sources. It strives to provide accurate and trustworthy answers.

3. Privacy and Security: Your privacy is important. The Mũriũ AI Assistant does not store or share any personal information from interactions.

## Conclusion

Thank you for choosing Mũriũ AI as your tech assistant. It aims to make your information retrieval experience seamless and enjoyable. If you have any questions or suggestions, feel free to reach out!