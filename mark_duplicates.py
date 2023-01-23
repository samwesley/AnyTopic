import json
import find_file_path
import os
from collections import Counter


def main(category):
    file_path = find_file_path.main(category)
    with open(file_path + "data.json") as f:
        data = json.load(f)
    keyword_lists = []

    for article in data["articles"].values():
        keyword_lists.append(article["keywords"])

    duplicateLists = find_overlap(keyword_lists)
    counter = 0
    for i in duplicateLists:
        for k in range(2):
            index = str(i[k])
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
    with open(file_path + "data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Duplicates Count........"+ str(counter))
    choose_main_article(category)
    return os.path.basename(__file__) + " finished"



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



def choose_main_article(category):
    file_path = find_file_path.main(category)
    with open(file_path + "data.json") as f:
        data = json.load(f)
    for article in data["articles"].values():
        if "duplicates" in article:
            textCounts = []
            for i in article["duplicates"]:
                textCounts.append(len(data["articles"][i]["text"]))
            maxIndex = textCounts.index(max(textCounts))
            data["articles"][article["duplicates"][maxIndex]]["skip"] = "false"
    with open(file_path + "data.json", "w") as f:
        json.dump(data, f, indent=4)

