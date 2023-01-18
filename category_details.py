import json
import variables
import find_file_path
import openai
import unicode_converter
import ast
openai.api_key = variables.openAPIKey
from revChatGPT.ChatGPT import Chatbot

def get_category_details(category,conversation_id=None):

    prompt = f"""Act like you are generating a newsletter for me. I am going to provide you a topic and I want you to ask for information that would better help you decide if any news article is relevant for the topic I'm interested in. The topic is {category}"""
    prompt2 = "Act like you are generating a newsletter for me. I am interested in the chicago river for my non-profit that works on it and I want you to ask for information that would better help you decide if any news article is relevant for the topic I'm interested in."
    chatbot = Chatbot({
        "session_token": "INSERT_SESSION_TOKEN_HERE",
    }, conversation_id, parent_id=None) # You can start a custom conversation

    response = chatbot.ask(prompt, conversation_id, parent_id=None) # You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations are automatically saved)
    print(response)
    print(response["message"])
    return response["message"],response["conversation_id"]



def category_list(category=None):
    for i in variables.categoryNames.values():
        print(i)
        get_category_details(i)
    '''
    categoryName = variables.categoryNames[category]
    message, conv_id = get_category_details(categoryName)
    '''

category_list()