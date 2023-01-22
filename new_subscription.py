import json
import time

import variables
import random
import string
import create_google_alerts
import boto3

# Connect to DynamoDB
dynamodb = boto3.client('dynamodb')

def new_subscription(email, category, category_details):

    category_url = create_google_alerts.create_alerts(category)
    time.sleep(1)
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
    print(response)

new_subscription('robbyriley15@gmail.com', 'gardening', 'I am interested in vegetable gardening as an intermediate gardener in a temperate climate with a goal of learning new gardening techniques and interested in both indoor and outdoor content and organic method of gardening. I am interested in in-ground gardening and specifically in vegetable plants and soil management issues.')