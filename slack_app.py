from slack_bolt import App
import json
import slack_block_builder
# Initializes your app with your bot token and socket mode handler



def findUserDetails(userEmail):
    with open("users/subscriptions.json") as f:
        data = json.load(f)

        for user in data["users"]:
            if user["email"] == userEmail:
                channel = user["slack"]["channel"]
                slackKey = user["slack"]["key"]
                return channel, slackKey



def sendMessages(category, userEmail):
    channel, slackKey = findUserDetails(userEmail)
    app = App(token=slackKey)
    block1, block2 = slack_block_builder.main(category)
    app.client.chat_postMessage(token=slackKey,channel=channel, blocks=block1["blocks"])
    app.client.chat_postMessage(token=slackKey, channel=channel, blocks=block2["blocks"])
    return "Sent"
