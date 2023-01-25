from sendgrid.helpers.mail import *
import sendgrid
import dotenv
import os
import json

dotenv.load_dotenv()

full_template = {}
links = []
summaries = []
titles = []
gpt_relevancy_score = []

summ_links = []
summ_titles = []

list_order = []

def testing():
    full_dict = {}
    with open("test/2023-01-24_Space Technology_data.json") as f:
        data = json.load(f)
    category = data["category"]
    full_dict["category"] = category
    links = []
    titles = []
    summary = []
    relevancy = []

    for i in data["articles"]:
        path = data["articles"][str(i)]
        if "summary" in path:
            links.append(path["link"])
            titles.append(path["title"])
            summary.append(path["summary"])
            relevancy.append(path["gpt_relevancy_score"])
    try:
        for i in range(len(relevancy)):
            list_order.append(i)
        list_order.sort(key=lambda x: relevancy[x], reverse=True)
    except Exception as e:
        print(e)
        pass
    summaryCount = 5
    if len(summary) < summaryCount:
        summaryCount = len(summary)
    for i in range(summaryCount):
        full_dict["summary_link_{}".format(i+1)] = links[list_order[i]]
        full_dict["summary_title_{}".format(i+1)] = titles[list_order[i]]
        full_dict["summary_{}".format(i+1)] = summary[list_order[i]]

    links = []
    titles = []
    for i in data["articles"]:
        if i not in list_order[:5]:
            path = data["articles"][str(i)]
            links.append(path["link"])
            titles.append(path["title"])
        additionalCount = 9
    if len(titles) < additionalCount:
        additionalCount = len(titles)
    for i in range(additionalCount):
        full_dict["additional_link_{}".format(i+1)] = links[i]
        full_dict["additional_title_{}".format(i+1)] = titles[i]
    send_email(full_dict)
    return full_dict

def send_email(full_dict):

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    from_email = "sam@anytopic.io"
    to_email = "sam@anytopic.io"
    template_id = "d-bfcdffb03aea4f0a98831da3d54f146b"


    mail = Mail()
    mail.from_email = from_email
    mail.template_id = template_id

    personalization = Personalization()

    for key, value in full_dict.items():
        personalization.add_substitution(Substitution('-{}-'.format(key), value))




    # Add the recipient to the mail
    mail.add_to(to_email)
    mail.dynamic_template_data = full_dict

    mail_json = mail.get()

    print(mail_json)

    # Send the email
    response = sg.client.mail.send.post(request_body=mail_json)

    # Print the response
    print(response.status_code)
    print(response.body)
    print(response.headers)

testing()