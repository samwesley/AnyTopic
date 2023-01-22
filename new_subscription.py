import json
import variables
import random
import string
import create_google_alerts


def new_subscription(userEmail, categories, category_details):
    with open("users/subscriptions.json") as f:
        data = json.load(f)
        #look through all user id's and add a new id for this user that's one larger than the largest id
        ids = []
        for user in data["users"]:
            ids.append(user["id"])
        newId = max(ids) + 1

        #create a new user with the new id
        for i in categories:
            generate_code(i)
        print(len(categories))
        category_urls = {category_keys[i]: create_google_alerts.create_alerts(categories[i]) for i in range(len(categories))}
        data["users"].append({"id" : newId, "email": userEmail, "category_keys": category_keys, "categories": categories, "category_details": category_details, "category_urls": category_urls})
        print("New user added! Email: " + userEmail + " Categories: " + str(categories))
        with open("users/subscriptions.json", "w") as f:
            json.dump(data, f, indent=4)

category_keys = []

def generate_code(input):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(1,3)))
    if code not in category_keys:
        category_keys.append(code)
        return code
    else:
        return generate_code(input)

newTopicList = ["chicago river", "AI startup accelerator accepting applications"]

new_subscription("allTest3@gmail.com", newTopicList, ["", ""])
