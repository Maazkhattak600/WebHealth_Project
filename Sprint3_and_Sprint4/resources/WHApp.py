#monitor web health --> Availability and latency
import urllib3
import datetime
from cloudwatch_putData import AWSCloudWatch
import constants as constants
import os 
import boto3

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
dynamodb = boto3.resource('dynamodb',region_name='us-east-2')
table_name = os.environ['URLTable']
table = dynamodb.Table(table_name)
topicname=os.environ["snsTopic"]
AlarmActions = ["arn:aws:sns:us-east-2:315997497220:{snsTopic}".format(snsTopic=snsTopic)]
URL = []
values = []

def lambda_handler(event,context):
    
    
    #Cloudwatch Object

    cloudwatch_object = AWSCloudWatch()

    #values = dict()
    # Function to fetch website avail and latency
    response = table.scan()
    lists = response['Items']
    for l in lists:
        URL.append(l['url'])
        
    for x in URL:
        dimensions = [
        {
               'Name' : 'URL' ,
               'Value': x,
        }]
        
        availability= getavail(x)
        latency = getlatency(x)
        
    
    #Sending Data to CloudWatch
        
        
        cloudwatch_object.cloudwatch_metric_data(constants.namespace , constants.AvailabilityMetric,dimensions,availability)
        cloudwatch_object.cloudWatch_metric_alarm("Availibility_of_Maaz " + str(x) ,AlarmActions,constants.AvailabilityMetric,constants.namespace,1,"LessThanThreshold")
        
        cloudwatch_object.cloudwatch_metric_data(constants.namespace,constants.LatencyMetric,dimensions,latency)
        cloudwatch_object.cloudWatch_metric_alarm("Latency_of_Maaz " + str(x) ,AlarmActions,constants.LatencyMetric,constants.namespace,0.5,"GreaterThanThreshold")
        values.append({"availability of "+str(x):availability, "latency of "+str(x):latency})
        
    return values

def getavail(a):
    http = urllib3.PoolManager()
    response = http.request("GET",a)
    if response.status == 200:
        return 1
    else:
        return 0

def getlatency(a):
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET",a)
    end = datetime.datetime.now()
    delta = end - start
    latencySec = round(delta.microseconds * .000001,6)
    return latencySec 
    
