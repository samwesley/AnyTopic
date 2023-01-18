import find_file_path
import openai
import json
import variables
import os
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def category_details(category):
    category_name = variables.categoryNames[category]
    #category_details = ""
    category_details = "I'm not looking for any subtopics in particular, I'm interested in new technology and general news. I'm looking for news that's within the past month. I'm looking for both news and articles from scientific journals and magazines. "
    intro = f"You are a news curator, I am coming to you asking for news related to {category_name}. {category_details}. Based on this guidance, generate a single integer score from 0-10 of how relevant the following article is for me. Format the score as x/10. Article: "
    return intro

def davinci(block,category):
    intro = category_details(category)
    prompt = intro + block
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text

    return text

def davinciRaw(block):
    prompt = block
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text
    return text

def main(category):
    file_path = find_file_path.main(category)
    skipCount = 0
    with open(file_path + "data.json") as f:
        data = json.load(f)
    for i in range(len(data["articles"])):
        try:
            path = data['articles'][str(i)]['text']

            response = davinci(path,category)
            data['articles'][str(i)]['gpt_score_reason'] = response
            prompt = "Return only the numerator of the score from the following text, if the score is not a fraction just return the number :" + response
            gptScore = davinciRaw(prompt)
            gptScore = gptScore.replace("\n","")
            gptScore = int(gptScore)
            if gptScore < 5:
                data['articles'][str(i)]['skip'] = "true"
                skipCount += 1
            data['articles'][str(i)]['gpt_relevancy_score'] = gptScore
            #print("GPT Relevancy Score: " + gptScore)
        except Exception as e:
            data['articles'][str(i)]['skip'] = "true"
            data['articles'][str(i)]['gpt_relevancy_score'] = 0
            pass
    with open(file_path + 'data.json', 'w') as outfile:
        json.dump(data, outfile)
    print("GPT relevancy skip......" + str(skipCount))
    return os.path.basename(__file__) + " finished"

