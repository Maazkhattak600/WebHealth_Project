import boto3
import os

"""Class to put data into the dynamodb"""
class Dynamodb:
    def __init__(self):
        """ Retrieve Table name from Environement variables"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        # https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-retrieve
        self.table_name = os.environ('AlarmTable')

        

        # https://dynobase.dev/dynamodb-python-with-boto3/#get-item
        self.table = self.dynamodb.Table(self.table_name)
    

    """ Putting data into the dynamodb"""
    # https://dynobase.dev/dynamodb-python-with-boto3/#put-item
    def put_Data(self, messageid , timestamp , subject,message):
        response = self.table.put_item(
            Item={
                'id': messageid,
                'Timestamp': timestamp,
                'Subject': subject,
                'Message':message,
    }
)

