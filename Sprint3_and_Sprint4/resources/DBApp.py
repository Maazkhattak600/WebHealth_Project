from DB_put_data import Dynamodb


def lambda_handler(event , context):
    #print(event)
    #Parse the event variable - extract the relevant info and populate the table
    messageid = event['Records'][0]['Sns']['MessageId'] 
    timestamp = event['Records'][0]['Sns']['Timestamp']
    subject = event['Records'][0]['Sns']['Subject']
    message = event['Records'][0]['Sns']['Message']

    """ Object to put data into the dynamodb"""
    dynamodb_obj = Dynamodb()
    dynamodb_obj.put_Data(messageid,timestamp,subject,message)
    

    

