import boto3

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('users')

def get_user_data(email,category):
    response = table.get_item(
        Key={
            'email': email,
            'category': category
        }
    )
    item = response['Item']
    print(item)
    return item
get_user_data('robbyriley15@gmail.com','gardening')