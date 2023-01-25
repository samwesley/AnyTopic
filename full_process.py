import os
import requests
import json
import find_file_path
from newspaper import Article
from bs4 import BeautifulSoup
import datetime
import traceback
import unicode_converter
import openai
from dotenv import load_dotenv
import time
from slack_bolt import App
import json
import slack_block_builder
import boto3
import uuid

load_dotenv()

today = str(datetime.date.today())


texts = []
titles = []
keywords = []
links = []

file_name = ""
category = ""
details = ""
#response = {'category': 'gardening', 'details': 'I am interested in vegetable gardening as an intermediate gardener in a temperate climate with a goal of learning new gardening techniques and interested in both indoor and outdoor content and organic method of gardening. I am interested in in-ground gardening and specifically in vegetable plants and soil management issues.', 'email': 'robbyriley15@gmail.com', 'url': 'https://google.com/alerts/feeds/14677448040511440142/15328111450502535226'}




def getLinksFromXML(url):
    # Fetch the web page containing the article
    response = requests.get(url)
    # Parse the web page into a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'lxml')
    # Find the main content of the article, which is likely to be contained in a
    # div with a specific class name
    '''pull all links from the xml file'''
    for link in soup.find_all('link'):
        tLink = link.get('href')
        try:
            tLink = tLink.split("&url=")[1]
            tLink = tLink.split("&ct=")[0]
            #print("The link is now " + tLink)
            links.append(tLink)
        except Exception as e:
            print(traceback.print_exc())
    print("Link Count..............." + str(len(links)))
    return links

def parseArticle(category,email):
    for i in links:
        article = Article(i)
        try:
            fileName = links.index(i)
            article.download()
            article.parse()
            article.nlp()
            #time.sleep(1)
            text = article.text
            title = article.title
            keyword = article.keywords
            try:
                text = unicode_converter.main(text)
            except Exception as e:
                print(e)
            texts.append(text)
            titles.append(title)
            keywords.append(keyword)
        except Exception as e:
            print(traceback.print_exc())
            texts.append("")
            titles.append("")
            keywords.append("")

    print("Text Count.............." + str(len(texts)))
    print("Title Count............." + str(len(titles)))
    print("Keyword Count..........." + str(len(keywords)))
    create_dict(links, texts, titles, keywords,category,email)


def create_dict(links, texts, titles, keywords, category,email):
    result = {"date": today, "category": category, "email":email, "articles": {}}
    counter = 0
    for link, text, title, keyword in zip(links, texts, titles, keywords):
        result["articles"][counter] = {"link" : link, "title" : title, "keywords" : keyword, "text" : text}
        counter += 1
    return result

def final_pull_articles(file_name,category):
    with open('data_template.json') as f:
        data = json.load(f)
        counter = 0
        for i in links:
            number = links.index(i)
            #add a new field to data with number as a key and text, title, keywords and link as values
            data["articles"][number] = {"text": texts[number], "title": titles[number], "keywords": keywords[number], "link": links[number], "skip": "false"}
            path = data["articles"][number]
            if len(path["text"])< 100:
                print("Marking as Skip due to <100 words" + path["title"])
                data["articles"][number]["skip"] = "true"
                counter += 1
            data["date"] = today
            data["category"] = category
    print("Skip Count............." + str(counter))


    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)
    return data

"""Marking Duplicates Section"""

def main_duplicates(data,file_name):
    keyword_lists = []

    for article in data["articles"].values():
        keyword_lists.append(article["keywords"])

    duplicateLists = find_overlap(keyword_lists)
    counter = 0
    for i in duplicateLists:
        for k in range(2):
            index = i[k]
            print(index)
            #if there is no key duplicates in the json file, create one
            if "duplicates" not in data["articles"][index]:
                data["articles"][index]["duplicates"] = []
            path = data["articles"][index]["duplicates"]
            data["articles"][index]["skip"] = "true"
            print("Marking as Skip due to duplicates " + data["articles"][index]["title"])
            for l in range(2):
                path.append(str(i[l]))
            print("duplicates found: ", i)
            counter +=1
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
    print("Duplicates Count........"+ str(counter))
    choose_main_article(file_name)


def find_overlap(lists):
    overlaps = []
    for i in range(len(lists)):
        for j in range(i+1, len(lists)):
            try:
                overlap = len(set(lists[i]) & set(lists[j])) / len(set(lists[i]) | set(lists[j]))
                if overlap > 0.3:
                    overlaps.append((i, j))
            except ZeroDivisionError:
                pass
    return overlaps


def choose_main_article(file_name):
    with open(file_name) as f:
        data = json.load(f)
    for article in data["articles"].values():
        if "duplicates" in article:
            textCounts = []
            for i in article["duplicates"]:
                textCounts.append(len(data["articles"][i]["text"]))
            maxIndex = textCounts.index(max(textCounts))
            data["articles"][article["duplicates"][maxIndex]]["skip"] = "false"
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

"""GPT Relevancy Scoring Section"""


openai.api_key = os.getenv("OPENAI_API_KEY")

def category_details(category,details):
    #category_details = "I'm not looking for any subtopics in particular, I'm interested in new technology and general news. I'm looking for news that's within the past month. I'm looking for both news and articles from scientific journals and magazines. "
    intro = f"You are a news curator, I am coming to you asking for news related to {category}. {details}. Based on this guidance, generate a single integer score from 0-10 of how relevant the following article is for me. Format the score as x/10. Article: "
    return intro

def davinci(block, category, details):
    intro = category_details(category,details)
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

def main_relevancy():
    skipCount = 0
    with open(file_name) as f:
        data = json.load(f)
    for i in range(len(data["articles"])):
        try:
            path = data['articles'][str(i)]['text']
            response = davinci(path,category,details)
            data['articles'][str(i)]['gpt_score_reason'] = response
            prompt = "Return only the numerator of the score from the following text, if the score is not a fraction just return the number :" + response
            gptScore = davinciRaw(prompt)
            gptScore = gptScore.replace("\n","")
            gptScore = int(gptScore)
            if gptScore < 5:
                data['articles'][str(i)]['skip'] = "true"
                skipCount += 1
            data['articles'][str(i)]['gpt_relevancy_score'] = gptScore
        except Exception as e:
            data['articles'][str(i)]['skip'] = "true"
            data['articles'][str(i)]['gpt_relevancy_score'] = 0
            pass
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)
    print("GPT relevancy skip......" + str(skipCount))


"""Get Summary Section"""


def getSummary(text):
    intro = "Extract the key points from the following article and write them in a 2-4 sentence summary used for an email newsletter. Only respond with the summary as if it were a paragraph in an article, do not uses any header. Article : "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt = intro + text,
            temperature=0.9,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        response = response.choices[0].text
        return response
    except openai.error.InvalidRequestError:
        print("Error: Article text is too long, attempting to shorten")
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt = intro + text,
                temperature=0.9,
                max_tokens=500,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1
            )
            response = response.choices[0].text
            return response
        except openai.error.InvalidRequestError:
            print("Error: Could not shorten article text, skipping. Article Text: ", len(text.split()))
            return ""


def main_summary():
    with open(file_name) as f:
        data = json.load(f)
    counter = 0
    skip_count = 0
    for article in data["articles"].values():
        path = article["skip"]
        if "summary" not in article and path == "false":
            summary = getSummary(article["text"])
            if summary.startswith("Summary: "):
                summary = summary.split("Summary: ", 1)[1]
            if '\n' in summary:
                summary = summary.split("\n",1,)[1]
            article["summary"] = summary
            counter += 1
            time.sleep(1)
        else:
            skip_count += 1
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
    print("Summaries written......."+ str(counter))
    print("Skip Count.............."+ str(skip_count))

    if counter == 0:
        print("Exiting as no summaries were written")
        #exit()
    return os.path.basename(__file__) + " finished"


"""Slack App Section"""

slack_key = os.getenv("SAM_SLACK_KEY")
# Initializes your app with your bot token and socket mode handler

def main_slack(file_name):
    channel = "@samwesley3"
    app = App(token=slack_key)
    block1, block2 = slack_block_builder.main(file_name)
    app.client.chat_postMessage(token=slack_key,channel=channel, blocks=block1["blocks"])
    app.client.chat_postMessage(token=slack_key, channel=channel, blocks=block2["blocks"])
    return "Sent"

def get_user_info(email):
    #Pull all user subscriptions from dynamoDB
    from boto3.dynamodb.conditions import Key
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    response = table.query(KeyConditionExpression=Key('email').eq(email))
    return response

'''Save Data to S3'''
def save_to_s3():
    s3 = boto3.client('s3')
    # specify the bucket name and file name
    bucket_name = 'anytopic-newsletter-data'

    # open the file in binary mode
    with open(file_name, 'rb') as data:
        # upload the file to S3
        response = s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    return response

def save_newsletter_to_dynamo(email):
    file_name = 'test/2023-01-23_Space Robotics_data.json'
    dynamodb = boto3.client('dynamodb')
    url = f"https://anytopic-newsletter-data.s3.amazonaws.com/{file_name}"
    id = str(uuid.uuid4())
    item = {
        'id': {'S': id},
        'url': {'S': url},
        'user': {'S': email},
        'date': {'S': today}
    }
    response = dynamodb.put_item(
        TableName='newsletters',
        Item=item
    )
    return response


def main(email):
    all_subscriptions = get_user_info(email)
    for subscription in all_subscriptions["Items"]:
        print(subscription)
        global category
        global details
        global file_name
        url = subscription['url']
        category = subscription['category']
        details = subscription['details']
        file_name = "test/" + today + "_" + category + "_data.json"
        getLinksFromXML(url)
        parseArticle(file_name,email)
        article_data = final_pull_articles(file_name, category)
        links.clear()
        texts.clear()
        titles.clear()
        keywords.clear()
        main_duplicates(article_data,file_name)
        main_relevancy()
        main_summary()
        save_to_s3()
        save_newsletter_to_dynamo(email)
        main_slack(file_name)
    return os.path.basename(__file__) + " finished"

main('samwesley3@gmail.com')
#print(save_newsletter_to_dynamo())