import time

import openai
import json
import os
import find_file_path
import variables

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def getSummary(text):
    intro = "Extract the key points from the following article and write them in a 2-4 sentence summary used for an email newsletter. Only respond with the summary. Do not uses any header, only write the summary. Article : "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt = intro + text,
            temperature=0.9,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        response = response.choices[0].text
        return response
    except openai.error.InvalidRequestError:
        print("Error: Article text is too long, attempting to shorten")
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt = intro + text,
                temperature=0.9,
                max_tokens=500,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1
            )
            response = response.choices[0].text
            return response
        except openai.error.InvalidRequestError:
            print("Error: Could not shorten article text, skipping. Article Text: ", len(text.split()))
            return ""


def main(category):
    file_path = find_file_path.main(category)
    with open(file_path + "data.json") as f:
        data = json.load(f)
    counter = 0
    skip_count = 0
    for article in data["articles"].values():
        path = article["skip"]
        if "summary" not in article and path == "false":
            article["summary"] = getSummary(article["text"])
            counter += 1
            time.sleep(1)
        else:
            skip_count += 1
    with open(file_path + "data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Summaries written......."+ str(counter))
    print("Skip Count.............."+ str(skip_count))

    if counter == 0:
        print("Exiting as no summaries were written")
        #exit()
    return os.path.basename(__file__) + " finished"
