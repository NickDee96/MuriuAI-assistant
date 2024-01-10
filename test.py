import pandas as pd
# This code is for v1 of the openai package: pypi.org/project/openai
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()
from tqdm import tqdm

df = pd.read_csv("data/q4 Leads - L1.csv")

prompt_template = '''
My name is Nick the CEO and Cofounder of Continuum Ads.

Write a LinkedIn cold message to {firstName} using the context and bio below to create a personalized message. Do not add a subject. Just the message. Do not include the bio or summary verbatim.
THE MESSAGE SHOULD BE LESS THAN 700 CHARACTERS.


{fullName} is the {title} at {companyName} with the following bio:
{summary}

Below is a description of what {companyName} is all about:
{titleDescription}

About the Continuum Ads no commitment-free beta:
We've made significant enhancements to our platform, incorporating valuable insights from thought leaders like you and feedback from potential users. I believe these updates could bring substantial benefits to {companyName}, and I'd love to give you an exclusive look.

Additionally, we're launching a commitment-free beta test, and I see a great opportunity for a partnership. If you're interested, let's set up a time to dive into what's new and explore how we might collaborate for mutual success.


The cold message should have all of the following properties:

 - Personalized: The message should be tailored to the recipient. Use their name, reference their work, or mention a common connection.
 - Brief and Concise: Keep your message short and to the point. Respect the recipient's time.
 - Clear Purpose: State the purpose of your message in the beginning. Why are you reaching out? What do you want from them?
 - Value Proposition: Explain what's in it for them. How can they benefit from responding to your message?
 - Professional Tone: Maintain a professional and respectful tone throughout the message.
 - Call to Action: End the message with a clear call to action. What should they do next?
 - Error-Free: Make sure your message is free of spelling and grammar mistakes.
 - Follow-Up Plan: If you don't hear back, have a plan for a polite and non-intrusive follow-up.


'''

df.fillna('', inplace=True)
responses = []

for i in tqdm(range(len(df))):
    prompt = prompt_template.format(
        firstName = df.iloc[i]['firstName'].capitalize(),
        fullName = df.iloc[i]['fullName'].capitalize(),
        title = df.iloc[i]['title'].capitalize(),
        companyName = df.iloc[i]['companyName'].capitalize(),
        summary = df.iloc[i]['summary'],
        titleDescription = df.iloc[i]['titleDescription']

    )

    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are an experience Sales Lead generator on LinkedIn."
        },
        {
        "role": "user",
        "content": prompt
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    chat_response = response.choices[0].message.content
    responses.append(chat_response)

df["messages"] = responses

df.to_csv("data/q4 Leads - L1_with_messages.csv", index=False)