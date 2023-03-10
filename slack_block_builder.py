import json
import find_file_path
import variables

divider = {
    "type": "divider"
}

def pullData(file_name):
    with open(file_name) as f:
        data = json.load(f)
    for i in range(len(data["articles"])):
        try:
            path = data["articles"][str(i)]
            if path["skip"] == "true":
                data["articles"].pop(str(i))
        except KeyError:
            pass
    return data

list_order = []

def generateMainBlock(file_name):
    data = pullData(file_name)
    category = data["category"]
    links = []
    titles = []
    summary = []
    relevancy = []

    for i in data["articles"]:
        path = data["articles"][str(i)]
        if "summary" in path:
            links.append(path["link"])
            titles.append(path["title"])
            summary.append(path["summary"])
            relevancy.append(path["gpt_relevancy_score"])

    blocks = []
    #write a list of the indexes of relevancy scores in descending order
    # Added try to handle the case where articles are not scored on relevenacy
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
    for i in range(summaryCount):
        blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*<" + links[i] + "|" + titles[i] +">*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": summary[i]
                }
            },
            {
                "type": "divider"
            }
        ])

    blocks.insert(0, {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": ":newspaper: Newsy :newspaper:"
        }
    })
    blocks.insert(1, {
        "type": "divider"
    })
    blocks.insert(2, {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": " :loud_sound: "+ category + " :loud_sound:"
        }
    })
    blocks.insert(3, {
        "type": "divider"
    })
    return { "blocks": blocks }

def generateSecondBlock(file_name):
    blocks = []
    data = pullData(file_name)
    links = []
    titles = []
    for i in data["articles"]:
        if i not in list_order[:5]:
            path = data["articles"][str(i)]
            links.append(path["link"])
            titles.append(path["title"])

    additionalCount = 9
    if len(titles) < additionalCount:
        additionalCount = len(titles)
    for i in range(additionalCount):
        blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<" + links[i] + "|" + titles[i] + ">"
                }
            }
        ])
    blocks.insert(0, {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": ":newspaper: Additional News :newspaper:"
        }
    })
    return { "blocks": blocks }


def main(file_name):
    block1 = generateMainBlock(file_name)
    block2 = generateSecondBlock(file_name)
    return block1, block2

