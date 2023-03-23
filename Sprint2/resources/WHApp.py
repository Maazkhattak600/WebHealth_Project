#monitor web health --> Availability and latency
import urllib3
import datetime
from cloudwatch_putData import AWSCloudWatch
import constants as constants

def lambda_handler(event,context):
    
    #Cloudwatch Object

    cloudwatch_object = AWSCloudWatch()

    values = dict()
    
    for x in constants.urls:
        availability= getavail(x)
        latency = getlatency(x)
        values.update({"availability of "+str(x):availability, "latency of "+str(x):latency})
    
    #Sending Data to CloudWatch
        dimensions = [
        {
               'Name' : 'URL' ,
               'Value': x,
        }
        ]
        cloudwatch_object.cloudwatch_metric_data(constants.namespace , constants.AvailabilityMetric,dimensions,availability)
        cloudwatch_object.cloudwatch_metric_data(constants.namespace,constants.LatencyMetric,dimensions,latency)
        
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
    
