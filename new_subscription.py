import create_google_alerts
import boto3
import openai
import time
import ast

# Connect to DynamoDB
dynamodb = boto3.client('dynamodb')

def create_category_list(category, category_details):
    category_list = []
    prompt = f"Return a python usable list of 4 similar search terms for {category}, based on these details: {category_details}. The list should be in the format of ['term1', 'term2', 'term3']"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text
    print(text)
    text = ast.literal_eval(text)
    return text

def new_subscription(email, category, category_details):
    category_url = create_google_alerts.create_alerts(category)
    item = {
        'email': {'S': email},
        'category': {'S': category},
        'url': {'S': category_url},
        'details': {'S': category_details}
    }
    response = dynamodb.put_item(
        TableName='users',
        Item=item
    )
    print(email +" subscribed to: " + category)


def new_subscription_list(email, category, category_details):
    categories = create_category_list(category, category_details)
    category_list = []
    category_url_list = []
    for i in categories:
        new_url = create_google_alerts.create_alerts(i)
        if new_url != None:
            category_list.append(i)
            category_url_list.append(new_url)
            print(new_url)
    category_url = create_google_alerts.create_alerts(category)
    print(category_url_list)
    print(category_list)
    print(category_url)
    print(category)
    print(email)
    print(category_details)
    item = {
        'email': {'S': email},
        'category': {'S': category},
        #'url': {'S': category_url},
        'details': {'S': category_details},
        'sub_catergories': {'L': [{'S': item} for item in category_list]},
        'sub_category_url' : {'L': [{'S': item} for item in category_url_list]}
    }
    response = dynamodb.put_item(
        TableName='users',
        Item=item
    )
    print(email +" subscribed to: " + category)
new_subscription_list("samwesley3@gmail.com","Space robotics","I'm not looking for any subtopics in particular, I'm interested in new technology and general news. I'm looking for news that's within the past month. I'm looking for both news and articles from scientific journals and magazines. Be sure that this news is related to space, not just robotics.")
