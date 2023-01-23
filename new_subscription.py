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

new_subscription("samwesley3@gmail.com","startup competition","I'm looking for news about startup competitions to apply for. I'm looking for opportunities in the US and that have cash prizes.")