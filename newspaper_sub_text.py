import newspaper


#pull all json from test folder, and run the script on each one
import glob
import json
import os

all_urls = []

def get_all_json():
    path1 = "test/*.json"
    files = glob.glob(path1)
    try:
        for file in files:
            with open(file) as f:
                data = json.load(f)
                for i in data['articles']:
                    path = data['articles'][i]
                    if path['gpt_relevancy_score'] > 5 and len(path['link'])<100:
                        new_url = path['link']
                        all_urls.append(new_url)
                        print("``````````````````")
                        print("link: " + path['link'])
                        print(file)



    except Exception as e:
        print(e)
    #print(all_urls)
    with open('all_urls.json', 'w') as j:
        json.dump(all_urls, j)
    return all_urls

def get_text(url):

    print("getting " + url)
    paper = newspaper.build(url)
    try:
        test = paper.articles
        print(test)
        for article in paper.articles:
            #print(article.url)
            article.download()
            article.parse()
            print(article.title)
            article.nlp()
            print(article.keywords)
            print("---------------------")
    except Exception as e:
        print(e)

get_all_json()
with open('all_urls.json', 'r') as j:
    all_urls = json.load(j)

    for i in all_urls:
        get_text(i)