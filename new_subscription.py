import json
import variables
import random
import string


def newSubscription(userEmail, categories, category_details):
    with open("users/subscriptions.json") as f:
        data = json.load(f)
        #look through all user id's and add a new id for this user that's one larger than the largest id
        ids = []
        for user in data["users"]:
            ids.append(user["id"])
        newId = max(ids) + 1

        for i in categories:
            generate_code(i)

        data["users"].append({"id" : newId, "email": userEmail, "categoryKeys": code_list, "categories": categories, "category_details": category_details})
        print("New user added! Email: " + userEmail + " Categories: " + str(categories))
        with open("users/subscriptions.json", "w") as f:
            json.dump(data, f, indent=4)

code_list = []

def generate_code(input):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(1,3)))
    if code not in code_list:
        code_list.append(code)
        return code
    else:
        return generate_code(input)


newSubscription("test",["category"],["category_details"])