import variables
import datetime
import json

#Usage: copy the following line
# file_path = find_file_path.main(category)
today = str(datetime.date.today())

folderName = str(today)


def main(category):
    path = "categories/gardening/2023-01-21/final/"
    '''
    with open("users/subscriptions.json") as f:
        data = json.load(f)
        for user in data["users"]:
            for i in user["category_map"]:
                if i == category:
                    cat_name = user["category_map"][i]
                    cat_name = cat_name.replace(" ", "_")

    path = "categories/" + cat_name + "/" + folderName + "/final/"
    
    '''
    return path

