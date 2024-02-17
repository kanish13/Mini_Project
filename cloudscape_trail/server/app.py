import os
from werkzeug.utils import secure_filename
import boto3
import learn,db
import json
from dotenv import load_dotenv


load_dotenv('.env')



def lambda_handler(event, context):
    request_method = event.get('httpMethod')
    path = event.get('path')
    body = event.get('body')
    print(event)

    #Handle /query
    if request_method == 'POST' and path == '/query':
        ans = learn.query(body['pdf_url'],body['system_prompt'],body['query'])
        db.write_query(body['query'],ans,body['pdf_url'])
        return  {
        "statusCode": 200 ,
        "body": json.dumps({"message": "Query answered","answer": ans}),
        "headers": {
                "Content-Type": "application/json"
        }
    }

    #Handle /history
    if request_method == 'GET' and path == '/history':
        ans = learn.query(body['pdf_url'],body['system_prompt'],body['query'])
        db.write_query(body['query'],ans,body['pdf_url'])
        return  {
        "statusCode": 200 ,
        "body": json.dumps({"message": "Query answered","answer": ans}),
        "headers": {
                "Content-Type": "application/json"
        }
    }

   





