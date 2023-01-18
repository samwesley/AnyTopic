import json
import variables
import find_file_path
import os


def relevantListSearch(category):
    skipCount = 0
    file_path = find_file_path.main(category)
    with open("categories/categoryKeywords.json", "r") as j:
        categoryKeywords = json.load(j)
        relevantKeywords = categoryKeywords[category]
        for u in relevantKeywords:
            u = u.lower()
        j.close()

    with open(file_path + 'data.json') as f:
        data = json.load(f)
        f.close()

        for i in data["articles"]:
            kList = []
            counter = 0

            path = data["articles"][str(i)]
            keywords = path["keywords"]
            print(keywords)
            for k in keywords:
                if k.lower() in relevantKeywords:
                    kList.append(k)
                    print(k)
                    counter = counter + 1

            path["relevancy_score"] = counter
            if counter < 2:
                print("Marking as Skip due to relevancy_score", path["title"])
                print("relevancy_score was: ", counter)
                path["skip"] = "true"
                skipCount += 1

    with open(file_path + 'data.json', 'w') as f:
        json.dump(data, f)
        f.close()
    print("Nonrelevant Articles....", skipCount)
    print("Relevant Articles....", len(data["articles"]) - skipCount)
    return os.path.basename(__file__) + " finished"

