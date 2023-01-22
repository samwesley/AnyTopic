import boto3

# Connect to DynamoDB
dynamodb = boto3.client('dynamodb')

# Define the item to be added
item = {
    'email': {'S': 'samwesley3@gmail.com'},
    'category_key': {'S': 'sr'},
    'category_name': {'S': 'Space Robotics'},
    'category_url': {'S': 'https://www.google.com/alerts/feeds/04179049431026736918/16094280887727195819'},
    'category_details': {'S': "I'm not looking for any subtopics in particular, I'm interested in new technology and general news. I'm looking for news that's within the past month. I'm looking for both news and articles from scientific journals and magazines."}
}


item2 = {
    "email": {"S": "samwesley3@gmail.com"},
    "category_key": {"S": "st"},
    "category_name":{"S":"Space Technology"},
    "category_url":{"S":"https://www.google.com/alerts/feeds/04179049431026736918/10352800335472653504"},
    "category_details":{"S":"I'm not looking for any subtopics in particular, I'm interested in new technology and general news. I'm looking for news that's within the past month. I'm looking for both news and articles from scientific journals and magazines."}
}



# Add the item to the table
response = dynamodb.put_item(
    TableName='users',
    Item=item2
)

print(response)