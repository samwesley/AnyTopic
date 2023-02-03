import os
import requests
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
from sendgrid.helpers.mail import *
import sendgrid

load_dotenv()

today = str(datetime.date.today())


texts = []
titles = []
keywords = []
links = []
list_order = []

file_name = ""
category = ""
details = ""


total_cost = 0
tldr_cost = 0
relevancy_cost = 0
relevancy_2_cost = 0
summary_cost = 0
total_count = 0

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
    intro = f"You are a news curator, I am coming to you asking for news related to {category}. {details}. Based on this guidance, generate a single integer score from 0-10 of how relevant the following article is for me. Format the score as x/10. Article title: "
    return intro

def title_relevancy_scoring(title, category, details):
    intro = f"You are a news curator, I am coming to you asking for news related to {category}. {details}. Based on this guidance, return json with the following fields. A single integer score from 0-10 of how relevant the following article is for me (0 meaning do not ever read, 10 meaning drop everythiing and read right now). Title this fiield relevancy_score and format the score as only the numerator out of 10. If this score is higher than 4, do the following. Extract the key points from the following article and write a short 2 sentence summary of the article to be used for an email newsletter. Only respond with 2 sentences and tile this field two_summary. Lastly, return a python readable list of classifications for this article and title this field classifications. Article :"
    #intro = category_details(category, details)
    prompt = intro + title
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0,
        max_tokens=500,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text
    print(text)
    est = response.usage.total_tokens * 0.00002
    print("{} estimated cost: {}".format("relevancy",est))
    global total_cost
    total_cost += est
    global relevancy_cost
    relevancy_cost += est
    global total_count
    total_count += 1
    return text

def relevancy_scoring(block, category, details):
    intro = category_details(category,details)
    prompt = intro + block
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text
    est = response.usage.total_tokens * 0.00002
    print("{} estimated cost: {}".format("relevancy",est))
    global total_cost
    total_cost += est
    global relevancy_cost
    relevancy_cost += est
    return text

def fraction_fixing(block):
    prompt = block
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0,
        max_tokens=50,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text

    est = response.usage.total_tokens * 0.00002
    print ("{} estimated cost: {}".format("raw",est))
    global total_cost
    total_cost += est
    global relevancy_2_cost
    relevancy_2_cost += est
    return text


def main_relevancy():
    skipCount = 0
    with open(file_name) as f:
        data = json.load(f)
    for i in range(len(data["articles"])):
        try:
            path = data['articles'][str(i)]['text']
            if path != "":
                #response = title_relevancy_scoring(data['articles'][str(i)]['text'],category,details)
                response = relevancy_scoring(data['articles'][str(i)]['text'],category,details)
                data['articles'][str(i)]['test_combined'] = response
                #data['articles'][str(i)]['gpt_score_reason'] = response
                prompt = "Return only the numerator of the score from the following text, if the score is not a fraction just return the number :" + response
                gptScore = fraction_fixing(prompt)
                gptScore = gptScore.replace("\n","")
                gptScore = int(gptScore)
                if gptScore < 5:
                    data['articles'][str(i)]['skip'] = "true"
                    skipCount += 1
                if gptScore > 10 or gptScore < 0:
                    gptScore = 0
                    data['articles'][str(i)]['skip'] = "true"
                    skipCount += 1
                data['articles'][str(i)]['gpt_relevancy_score'] = gptScore
            else:
                data['articles'][str(i)]['skip'] = "true"
                data['articles'][str(i)]['gpt_relevancy_score'] = gptScore
                skipCount += 1
        except Exception as e:
            data['articles'][str(i)]['skip'] = "true"
            data['articles'][str(i)]['gpt_relevancy_score'] = 0
            print(e)
            pass
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)
    print("GPT relevancy skip......" + str(skipCount))


"""Get Summary Section"""


def getSummary(text):
    intro = "Extract the key points from the following article and write them in a short 2 sentence summary used for an email newsletter. Only respond with the summary as if it were a paragraph in an article, do not uses any header. Article : "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt = intro + text,
            temperature=0.4,
            max_tokens=300,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        text = response.choices[0].text
        est = response.usage.total_tokens * 0.00002
        print("{} estimated cost: {}".format("art 1",est))
        global total_cost
        total_cost += est
        global summary_cost
        summary_cost += est
        return text
    except openai.error.InvalidRequestError:
        print("Error: Article text is too long, attempting to shorten")
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt = intro + text,
                temperature=0.9,
                max_tokens=300,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1
            )
            text = response.choices[0].text
            est = response.usage.total_tokens * 0.00002
            print ("{} estimated cost: {}".format(intro,est))
            total_cost += est
            summary_cost += est
            return text
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
            #summary = getSummary(article["text"])
            summary = getSummary(article["text"])
            if summary.startswith("Summary:"):
                summary = summary.split("Summary:", 1)[1]
            if '\n' in summary:
                summary = summary.replace("\n","")
            article["summary"] = summary
            counter += 1
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
    #file_name = 'test/2023-01-23_Space Robotics_data.json'
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

def get_section_1():
    group_of_summaries = []
    with open(file_name) as data:
        data = json.load(data)
        for i in data["articles"]:
            if data["articles"][i]["skip"] == "false":
                group_of_summaries.append(data["articles"][i]["summary"])
        numbered_list = "\n".join(f"{index+1}. {item}" for index, item in enumerate(group_of_summaries))

    intro = "Generate a 3-5 sentence overview of the key points from the following summaries to be used for an email newsletter. Only respond with the summary as if it were a paragraph in an article, do not uses any header. List of summaries : "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt = intro + numbered_list,
            temperature=0.2,
            max_tokens=300,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        text = response.choices[0].text
        est = response.usage.total_tokens * 0.00002
        print("{} estimated cost: {}".format("tldr",est))
        global total_cost
        total_cost += est
        global tldr_cost
        tldr_cost += est
        tldr = text
        data["tldr"] = tldr
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)
        return tldr
    except openai.error.InvalidRequestError:
        print("Error: summaries text is too long")

def send_grid_start(email):
    full_dict = {}
    with open(file_name) as f:
        data = json.load(f)
    category = data["category"]
    full_dict["category"] = category
    links = []
    titles = []
    summary = []
    relevancy = []
    full_dict["tldr"] = data["tldr"]
    for i in data["articles"]:
        path = data["articles"][str(i)]
        if "summary" in path and path["skip"] != "true":
            links.append(path["link"])
            titles.append(path["title"])
            summary.append(path["summary"])
            relevancy.append(path["gpt_relevancy_score"])
    try:
        for i in range(len(relevancy)):
            list_order.append(i)
        list_order.sort(key=lambda x: relevancy[x], reverse=True)

    except Exception as e:
        print(e)
        pass
    summaryCount = 5
    if len(summary) < summaryCount:
        summaryCount = len(summary)
    if len(list_order) < summaryCount:
        summaryCount = len(list_order)
    print(links)
    print(titles)
    for i in range(summaryCount):
        print(list_order[i])
        print(titles[list_order[i]])
        full_dict["summary_link_{}".format(i+1)] = links[list_order[i]]
        full_dict["summary_title_{}".format(i+1)] = titles[list_order[i]]
        full_dict["summary_{}_text".format(i+1)] = summary[list_order[i]]
        full_dict["relevancy_score_{}".format(i+1)] = relevancy[list_order[i]]


    links = []
    titles = []
    score = []
    for i in data["articles"]:
        if i not in list_order[:5] and data["articles"][str(i)]["skip"] != "true":
            path = data["articles"][str(i)]
            links.append(path["link"])
            titles.append(path["title"])
            score.append(path["gpt_relevancy_score"])
        additionalCount = 9
    if len(titles) < additionalCount:
        additionalCount = len(titles)
    for i in range(additionalCount):
        full_dict["additional_link_{}".format(i+1)] = links[i]
        full_dict["additional_title_{}".format(i+1)] = titles[i]
        full_dict["additional_relevancy_score_{}".format(i+1)] = "Article score: {} / 10".format(score[i])

    send_email(full_dict,email)
    return full_dict

def send_email(full_dict,email):

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    from_email = "sam@anytopic.io"
    to_email = email
    template_id = "d-bfcdffb03aea4f0a98831da3d54f146b"


    mail = Mail()
    mail.from_email = from_email
    mail.template_id = template_id

    personalization = Personalization()

    for key, value in full_dict.items():
        personalization.add_substitution(Substitution('-{}-'.format(key), value))

    # Add the recipient to the mail
    mail.add_to(to_email)
    mail.dynamic_template_data = full_dict

    mail_json = mail.get()

    # Send the email
    response = sg.client.mail.send.post(request_body=mail_json)

def abandon_decision():
    summaries = []
    with open(file_name) as f:
        data = json.load(f)
    for i in data["articles"]:
        try:
            path = data["articles"][str(i)]
            if path["skip"] != "true":
                i = str(i)
                summaries.append(path["summary"])
                if len(summaries) < 1:
                    print("Abandoning due to lack of summaries!!!!!")
                    exit()
        except Exception as e:
            print(e)





def main(email):
    global total_cost
    global tldr_cost
    global relevancy_2_cost
    global relevancy_cost
    global summary_cost
    all_subscriptions = get_user_info(email)
    for subscription in all_subscriptions["Items"]:
        last_cost = total_cost
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
        abandon_decision()
        #main_slack(file_name)
        get_section_1()
        total_cost = total_cost - last_cost
        print("Total cost of {}: ${}".format(category,total_cost))
        print("Total Relevant Cost: ${}, Total Relevancy 2 Cost ${}, Total Summary Cost ${}, Total TLDR Cost ${}".format(relevancy_cost,relevancy_2_cost,summary_cost,tldr_cost))
        send_grid_start(email)
        print("Sent email to {} about {}".format(email,category))

    print("Total cost of all categories: ${}".format(total_cost))
    print("Total Scoring count: "+ total_count)

    return os.path.basename(__file__) + " finished"

main('samwesley3@gmail.com')


def test(email):
    send_grid_start(email)

#test('samwesley3@gmail.com')
