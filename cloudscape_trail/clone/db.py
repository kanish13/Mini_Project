# from pynamodb.aws_auth import AWS_Credentials
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
)
from dotenv import load_dotenv
import boto3
import os
import uuid
import json


load_dotenv('.env')

class Query_details(Model):
    class Meta:
        table_name = "Queries"
        region = os.getenv('REGION_NAME')
        key_schema = [
            {
                "AttributeName": "_id", 
                "KeyType": "HASH",
            }
        ]
    @classmethod
    def json_serialize(cls, model_instance):
        return {
            "_id": model_instance._id,
            "query": model_instance.query,
            "pdf_url": model_instance.pdf_url,
            "answer": model_instance.answer,
        }
    _id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    query = UnicodeAttribute(null=False)
    pdf_url = UnicodeAttribute(null=False)
    answer = UnicodeAttribute(null=False)


def write_query(query,answer,pdf_url):
    if not Query_details.exists():
        Query_details.create_table(read_capacity_units=1, write_capacity_units=1,wait=True)
    print("entered here now")
    past_query = Query_details(query=query, answer=answer, pdf_url=pdf_url)
    past_query.save()
    print("history created")

def get_queries():
    if not Query_details.exists():
        Query_details.create_table(read_capacity_units=1, write_capacity_units=1,wait=True)
    return json.dumps([Query_details.json_serialize(query) for query in Query_details.scan()])
