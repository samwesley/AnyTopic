import time
import variables
import json
import openai
import find_file_path

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

testPrompts = {
    "classification": "Determine what the topics of this article are, make a list and respond with them. Then provide a binary answer of if any those topics are related to Space or not with 0 representing no and 1 representing yes. Article : ",
    "summarization": "Extract the key points from the following article. Write them in a 2 sentence summary used for an email newsletter. Do not provide any header or title, simply write the summary. Article : ",
    "duplicates": "Are any of these article titles duplicates? If so, which ones? Please respond with only the index of articles that are duplicates (e.g. 0,2,10). Article Titles: ",
    "summarization2": "Extract the key points from the following article. Write them in a 2-5 sentence summary used for an email newsletter. Add a bit of personality to the summary. Do not provide any header or title, simply write the summary. Article : ",
    "learning_news": "I will provide you a list of article titles. I want you to decide which article appears to be the most likely article for a reader of a Space Technology newsletter to learn something new about the topic. Respond with only the index of the article title. Article Titles: ",
    "important_news": "I will provide you a list of article titles. I want you to decide which article is the most important for the topic of Space Technology. Respond with only the index of the article title. Article Titles: ",
    "inspiring_news": "I will provide you a list of article titles. I want you to decide which article is the most inspiring about the topic of Space Technology. Respond with only the index of the article title. Article Titles: ",
    "finding_job": "I will provide you a list of article titles, I am looking to read articles that will help me find and get a job in the Space industry, return the 3 most relevant article titles for this purposes and why you chose them. Article Titles: ",
    "title_summary":"Write a newsletter summary based on these article titles. Article Titles: ",
    "topic_probing":"You are a news curator, I am coming to you asking for news related to Space Technology. I am looking for technical news and general news on the field. Based on this guidance, generate a single score from 0-10 of how relevant the following article is for me. Article: "
}

def curie(prompt):
    response = openai.Completion.create(
        model="curie",
        prompt = prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text
    print(text)
    return text

def davinci2(promptName,block=None):
    intro = testPrompts[promptName]
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
    print(text)
    return text

def davinciRaw(prompt):
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
    print(text)
    return text

def davinci(block):
    intro = testPrompts["summarization2"]
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
    print(text)
    return text

def parseJSON(category):

    file_path = find_file_path.main(category)

    #FOR TESTING
    #path= "/categories/chicagoRiver/2023-01-03/final/"


    with open(file_path + "data.json") as f:
        text = json.load(f)
        counter = 0
        for i in range(20):

            file_name = str(i)
            firstFieldOption = ["date", "category"]
            secondFieldOption = ["link", "title", "html"]
            thirdFieldOptions = ["htmlTag", "block", "prompt", "summary", "blockWordCount"]

            secondField = text["articles"][file_name]
            thirdField = text["articles"][file_name]["article"]

            nonZero = []
            for j in thirdField["blockWordCount"]:

                j = int(j)

                if j > 1000 and j < 4500:
                    print(j)
                    #find the index of s in blockWordCount
                    index = thirdField["blockWordCount"].index(str(j))
                    #find the corresponding block
                    block = thirdField["block"][index]
                    print(block)
                    counter = counter + 1

                    link = secondField["link"]
                    title = secondField["title"]
                    summ = davinci(title)
                    #add new field to summaryDict with link title and summary
                    print("--------------------")
                    print("Title: " + title)
                    print("Summary: " + summ)
                    print("--------------------")
                    time.sleep(5)

def main(category):
    file_path = find_file_path.main(category)
    with open(file_path + "data.json") as f:
        data = json.load(f)
    for i in range(18):
        try:
            path = data['articles'][str(i)]['text']
            print("-------------------------")
            print(data['articles'][str(i)]['title'])
            response = davinci2("topic_probing",path)
            prompt = "Return only the numerator of the score from this text: " + response
            gptScore = davinciRaw(prompt)
            print("Relevancy Score: " + str(data['articles'][str(i)]['relevancy_score']))
            gptScore = gptScore.replace("\n","")
            print("GPT Relevancy Score: " + gptScore)
            gptScore = int(gptScore)

            data['articles'][str(i)]['gpt_score'] = gptScore
            #print("GPT Relevancy Score: " + gptScore)
        except Exception as e:
            print(e)
            pass
    with open(file_path + 'data.json', 'w') as outfile:
        json.dump(data, outfile)
main("sr")