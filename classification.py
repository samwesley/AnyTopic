import requests
import json
import find_file_path

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
apiToken = "INSERT_TOKEN_HERE"
headers = {"Authorization": f"Bearer {apiToken}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def classify(category):
    file_path = find_file_path.main(category)
    with open(file_path + "data.json") as f:
        data = json.load(f)
        titles = []
        articles = []
        outputs = []
        finalTitles = []
        blockNums = []
        for i in range(len(data["articles"])):
            i = str(i)
            title = data["articles"][i]["title"]
            article = data["articles"][i]["article"]["block"]
            if title != "No Title":
                titles.append(title)
                articles.append(article)
        for i in articles:
            index = articles.index(i)
            for j in i:

                output = query({
                    "inputs": j,
                    "parameters": {"candidate_labels": ["Space Technology", "Space Robotics","Real Estate", "Video Games", "Pop Culture"]}
                })
                title = titles[index]
                bNum = j
                outputs.append(output)
                finalTitles.append(title)

        with open(file_path + "classification.json", "w") as f:
            json.dump({"titles": finalTitles, "outputs": outputs}, f)

