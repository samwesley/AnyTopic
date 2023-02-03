import os
import json

def add_annotated_relevancy(title, category,gpt_relevancy_score):
    annotated_relevancy = int(input(title+" . Please enter the annotated relevancy score (an integer between 0 and 10): "))
    if annotated_relevancy > 10:
        annotated_relevancy = 10
    if annotated_relevancy < 0:
        annotated_relevancy = 0
    print("Title: ", title)
    print("Category: ", category)
    print("Annotated Relevancy: ", annotated_relevancy)
    print("gpt_relevancy_score: ", gpt_relevancy_score)
    return annotated_relevancy

def read_json_files(folder):
    text_list = []
    gpt_relevancy_score_list = []
    title_list = []
    category_list = []
    annotations_list = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            file_path = os.path.join(folder, file)
            print(file_path)
            with open(file_path, "r") as f:
                data = json.load(f)
                date = data["date"]
                category = data["category"]
                articles = data["articles"]
                for article in articles.values():
                    #text_list.append(article["text"])
                    gpt_relevancy_score_list.append(article["gpt_relevancy_score"])
                    title_list.append(article["title"])
                    category_list.append(category)
                    annotations_list.append("")
    for i in range(len(title_list)):
        if category_list[i] == "Space Robotics":
            annotation = add_annotated_relevancy(title_list[i], category_list[i], gpt_relevancy_score_list[i])
            if annotation == "e":
                break
            annotations_list[i] = annotation

    return text_list, gpt_relevancy_score_list, title_list, category_list, annotations_list
text = read_json_files("test")

with open("test.json", "w") as f:
    json.dump(text, f)

