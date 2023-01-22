import json



def get_category_keys(email):
    with open("users/subscriptions.json") as f:
        data = json.load(f)
        for user in data["users"]:
            if user["email"] == email:
                print(user["category_keys"])
                return user["category_keys"]

