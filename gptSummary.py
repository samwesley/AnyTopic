import openai
import json

def davinci(block,category=None):
    if category != None:
        intro = "You are writing a weekly newsletter about " + category + ". Summarize the following article in 2-5 sentences for a section in your newsletter. Article: "
    else:
        intro = "Extract the key points from the following article. Write a 2-5 sentence summary on the article that will be used for an email newsletter. Article : "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = intro + block,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text
    print("wrote this summary: " + text)
    print(text)
    return text