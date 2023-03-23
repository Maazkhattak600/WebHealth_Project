import os 
import boto3
import json
import constants as constants

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

#https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-retrieve
table_name = os.environ['URLTable']
table = dynamodb.Table(table_name)

# Getting All Table Data
URL = []
# response = table.scan()
# data = response["Items"]
# for url in data:
#    urls.append(url['URL'])

def lambda_handler(event,context):
    httpmethod=event["httpMethod"]
    # Get the url
    url=event["body"]

    # Perform CRUD operation if method matches
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html?highlight=dynamodb
    if httpmethod=="POST":
        response = table.put_item(
                            Item={ 
                                "URL":url
                            }
                        )
        # Return these lines to be shown in API when doing CRUD operation
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Added Successfully'
        }
        
    
    if httpmethod=="GET":
        response = table.scan()
        data=response["Items"]
        for urls in data:
            URL.append(urls['URL'])
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(URL)
        }

    
    if httpmethod=="PATCH":
        response=table.update_item(
                            Key={
                                "URL":url
                            },
                            UpdateExpression='SET URL = :URL1',
                            ExpressionAttributeValues={
                                                    ':URL1': url
                                                    }
                            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Updated Successfully'
        }
    
    if httpmethod=="DELETE":
        response=table.delete_item(
                                Key={
                                    "URL":url
                                    }
                            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Deleted Successfully'
        }
    
    