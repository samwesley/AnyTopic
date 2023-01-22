import os
import datetime
import json
import variables
today = str(datetime.date.today())

def createFolder(today):
    #check if the folder exists
    categories = []
    with open("users/subscriptions.json") as f:
        data = json.load(f)
        for user in data["users"]:
            for category in user["categories"]:
                if category not in categories:
                    category = category.replace(" ", "_")
                    categories.append(category)


    folderName = str(today)
    for i in categories:
        if not os.path.exists("categories/" + i):
            os.makedirs("categories/" + i)
            print("Created Directory: " + i)
        if not os.path.exists("categories/" + i + "/" + folderName):
            os.mkdir("categories/" + i + "/" + folderName)
            os.mkdir("categories/" + i + "/" + folderName + "/final")
            print("Folder created for " + i + " on " + today)

        #make file data.json from the template
        if not os.path.exists("categories/" + i + "/" + folderName + "/final/data.json"):
            with open("data_template.json", "r") as f:
                text = f.read()
                with open("categories/" + i + "/" + folderName + "/final/data.json", "w") as f:
                    f.write(text)




createFolder(today)