import create_google_alerts
import boto3

# Connect to DynamoDB
dynamodb = boto3.client('dynamodb')

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

#new_subscription("samwesley3@gmail.com","chicago bears","I'm looking for news on the chicago bears football team and current players.")