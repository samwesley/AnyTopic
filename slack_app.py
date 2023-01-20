from slack_bolt import App
import json
import slack_block_builder
import os
from dotenv import load_dotenv

load_dotenv()
slack_key = os.getenv("SAM_SLACK_KEY")
# Initializes your app with your bot token and socket mode handler



def findUserDetails(userEmail):
    with open("users/subscriptions.json") as f:
        data = json.load(f)

        for user in data["users"]:
            if user["email"] == userEmail:
                channel = user["slack"]["channel"]
                return channel



def sendMessages(category, userEmail):
    channel = findUserDetails(userEmail)
    app = App(token=slack_key)
    block1, block2 = slack_block_builder.main(category)
    app.client.chat_postMessage(token=slack_key,channel=channel, blocks=block1["blocks"])
    app.client.chat_postMessage(token=slack_key, channel=channel, blocks=block2["blocks"])
    return "Sent"
