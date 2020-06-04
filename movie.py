from decimal import Decimal
import json
import boto3


def load_movies(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('blog')
    
    response = table.put_item(
       Item={
            'blogid': "2",
            'title': "title",
            'info': {
                'plot': "Nothing happens at all.",
                'rating': '0'
            }
        }
    )
    print(response)

if __name__ == '__main__':
    load_movies()
