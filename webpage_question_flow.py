import openai
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def category_request(category):
    gpt_query = f"Act like you are generating a newsletter for me. I am going to provide you a topic and I want you to return a list of 5 related subtopics. Return these as a python usable list. The topic is {category}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=gpt_query,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
    )
    return response.choices[0].text

category_request("gardening")