import json

import pwd
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=pwd.ACCESS_ID,
    aws_secret_access_key=pwd.ACCESS_KEY,
    region_name=pwd.REGION_NAME
)

TABLE_NAME = "ExtenalPlans"
table = dynamodb.Table(TABLE_NAME)

for item in json.load(open('./outputs/plans.json','r',encoding='utf-8')):
    item['viewed']=False
    print(item)
    table.put_item(Item=item)

# print(table.creation_date_time)

