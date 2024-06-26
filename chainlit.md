# Mũriũ AI - Tech AI Assistant

Welcome to Mũriũ AI, your intelligent tech assistant developed by [Nick Mumero](https://github.com/NickDee96). We are here to assist you with factual answers to your queries using a combination of advanced language models and powerful tools.

## Features

### 1. Google Search
Mũriũ AI harnesses the power of Google to provide you with accurate and up-to-date information. Simply ask your question, and Mũriũ AI will fetch relevant results from the web.


Example:
- **User:** What is the capital of France?
- **Mũriũ AI:** Paris is the capital of France.


### 2. Web Crawling
Our chatbot has the ability to crawl websites, extracting valuable information for you. This feature allows Mũriũ AI to provide answers beyond the scope of traditional search engines.


Example:
- **User:** Can you find recent tech news?
- **Mũriũ AI:** Sure! Here are the latest tech news headlines:
  - [News Title 1](link1)
  - [News Title 2](link2)


### 3. Photo Generation
Mũriũ AI generates photos using OpenAI's models and APIs. It involves two steps: generating an image prompt and generating an image URL.

The image prompt is created by sending the user's input text to the OpenAI API. The AI model generates a response, which is the finetuned prompt description.

The image URL is generated by sending the image prompt to the DALL-E-3 model using the OpenAI API. The API returns the URL of the generated image.

The process is combined into a function that takes the user's prompt, generates the image prompt, and then generates the image URL. The resulting URL is shortened using the pyshorteners library.

Logging is used to record information and errors during the process.

## Usage Guidelines

1. **Conciseness:** Mũriũ AI is designed to be concise and to the point. We prioritize clarity and efficiency in our responses.

2. **Factual Answers:** Our responses are based on factual information obtained from reliable sources. We strive to provide accurate and trustworthy answers.

3. **Privacy and Security:** Your privacy is important to us. Mũriũ AI does not store or share any personal information from interactions.



Thank you for choosing Mũriũ AI as your tech assistant. We're here to make your information retrieval experience seamless and enjoyable. If you have any questions or suggestions, feel free to reach out!