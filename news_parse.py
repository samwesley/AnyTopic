import os
import requests
import json
import variables
import find_file_path
from newspaper import Article
from bs4 import BeautifulSoup
import datetime
import traceback
import unicode_converter

today = str(datetime.date.today())


texts = []
titles = []
keywords = []
links = []

def getLinksFromXML(category):
    file_path = find_file_path.main(category)
    url = variables.urls[category]

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

def parseArticle(category):
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
    create_dict(links, texts, titles, keywords,category)


def create_dict(links, texts, titles, keywords, category):
    result = {"date": today, "category": category, "articles": {}}
    counter = 0
    for link, text, title, keyword in zip(links, texts, titles, keywords):
        result["articles"][counter] = {"link" : link, "title" : title, "keywords" : keyword, "text" : text}
        counter += 1
    return result


def final(category):
    file_path = find_file_path.main(category)
    with open(file_path + 'data.json') as f:
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


    with open(file_path + 'data.json', 'w') as f:
        json.dump(data, f, indent=4)



def main(category):
    getLinksFromXML(category)
    parseArticle(category)
    final(category)
    links.clear()
    texts.clear()
    titles.clear()
    keywords.clear()
    return os.path.basename(__file__) + " finished"

