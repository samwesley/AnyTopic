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

new_subscription("samwesley3@gmail.com","Space Technology","Use the following rubric: 20% of score based on: must be new technology going into space or helping for space ecosystem. 20% for funding or creation of new space companies. 10% for current news <30 days old. 50% for the news specifically being related to something off earth, in space.")