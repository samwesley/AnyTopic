import json
import variables


def newSubscription(userEmail, slackUsername, categories):
    with open("users/subscriptions.json") as f:
        data = json.load(f)
        #look through all user id's and add a new id for this user that's one larger than the largest id
        ids = []
        for user in data["users"]:
            ids.append(user["id"])
        newId = max(ids) + 1

        data["users"].append({"id" : newId, "email": userEmail, "categories": categories, "slack": {"username": slackUsername}})
        print("New user added! Email: " + userEmail + " Categories: " + categories)
