import os
import learn,db
import json
import boto3
from dotenv import load_dotenv


load_dotenv('.env')



def handler(event, context):
    request_method = event.get('httpMethod')
    path = event.get('path')
    

    #Handle /
    if path=='/':
        return  {
        "statusCode": 200,
        "body": json.dumps({"message": "Finally it runs"}),
        "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*"
        }
        }


    #Handle /geturl
    if request_method == 'POST' and path == '/geturl':
        body = json.loads(event.get('body'))
        s3_client = boto3.client('s3')
        try:
            presigned_url = s3_client.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': os.getenv('BUCKET_NAME'),
                    'Key': body['filename'],
                },
                ExpiresIn=15 * 60  
            )
            return  {
            "statusCode": 200,
            "body": json.dumps({"message": "URL generated","presigned_url": presigned_url}),
            "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*"
            }
            }

        except Exception as e:
            print(f'Error uploading PDF: {e}')
            return   {
            "statusCode": 500,
            "body": json.dumps({"message": "URL generation failed","error": e}),
            "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*"
            }
            }
        


    #Handle /query
    if request_method == 'POST' and path == '/query':
        body = json.loads(event.get('body'))
        ans = learn.query(body['pdf_url'],body['system_prompt'],body['query'])
        db.write_query(body['query'],ans,body['pdf_url'])
        return  {
        "statusCode": 200 ,
        "body": json.dumps({"message": "Query answered","answer": ans}),
        "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*"
        }
    }

    #Handle /history
    if request_method == 'GET' and path == '/history':
        history=db.get_queries()
        return  {
        "statusCode": 200 ,
        "body": json.dumps({"message": "History fetched","history": history}),
        "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*"
        }
    }

   


