import json
import boto3
from flask_lambda import FlaskLambda
from flask import request
import simplejson as json

app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('blog')


@app.route('/hello')
def index():
    return json_response({"message": "Hello, world!"})

@app.route('/blog', methods=['GET', 'POST'])
def put_list_blog():
    if request.method == 'GET':
        blog = table.scan()['Items']
        return json_response(blog)
    elif request.method == 'POST':
        key = request.get_json(force=True)
        table.put_item(Item=key)
        return json_response({"message": "blog entry created"})


@app.route('/blog/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_blog(id):
    key = {"blogid": id}
    if request.method == 'GET':
        blog = table.get_item(Key=key).get('Item')
        if blog:
            return json_response(blog)
        else:
            return json_response({"message": "blog not found"}, 404)
    elif request.method == 'PATCH':
        key1 = request.get_json(force=True)
        table.update_item(Key = key,UpdateExpression="set content.author=:a, content.image_url=:i, content.content=:d",
        ExpressionAttributeValues={
            ':a':key1['content']['author'],
            ':i':key1['content']['image_url'],
            ':d':key1['content']['content']
        },
        ReturnValues="UPDATED_NEW"
        )
        return json_response({"message": "blog entry updated"})
    else:
        table.delete_item(Key=key)
        return json_response({"message": "blog entry deleted"})

def json_response(data, response_code=200):
    
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}

