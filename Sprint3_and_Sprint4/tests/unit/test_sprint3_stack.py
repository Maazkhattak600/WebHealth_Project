import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
from sprint3.sprint3_stack import Sprint3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3/sprint3_stack.py

"""Fixture added to avoid repeatition of Code"""
# https://docs.pytest.org/en/7.1.x/how-to/fixtures.html
@pytest.fixture
def fixture_fun():
    app = core.App()
    stack = Sprint3Stack(app,"sprint3")
    template = assertions.Template.from_stack(stack)

    return template

# UNIT TESTS
# Counting Resources
# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/README.html#counting-resources
#1  
def test_lambda_count(fixture_fun):
    
    fixture_fun.resource_count_is("AWS::Lambda::Function", 3)

#2
def test_DB(fixture_fun):

    fixture_fun.resource_count_is("AWS::DynamoDB::Table", 2)



# Resource Matching & Retrieval
# asserting that a resource with specific properties are present
# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/README.html#resource-matching-retrieval

#3
def test_SNS_Subscription_Properties(fixture_fun):
    
    fixture_fun.has_resource_properties("AWS::SNS::Subscription", {
    "Protocol": "email",
    "TopicArn": {
     "Ref": "WHNotifications19AE210E"
    },
    "Endpoint": "muhammadmaaz.khattak.skipq@gmail.com"
})

# #4
def test_DB_properties(fixture_fun):
    
    fixture_fun.has_resource_properties("AWS::DynamoDB::Table", {
        "ProvisionedThroughput": {
     "ReadCapacityUnits": 5,
     "WriteCapacityUnits": 5
    }
    
})

# #5
def test_Event_Rule_props(fixture_fun):
    
    fixture_fun.has_resource_properties("AWS::Events::Rule", {
      "ScheduleExpression": "rate(1 hour)"
    
})

# #6
# # Object Matchers
# # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/README.html#object-matchers

def test_Event_Rule(fixture_fun):
    
    fixture_fun.has_resource_properties("AWS::SNS::Subscription", {
        "TopicArn": assertions.Match.object_like({
        "Ref": "WHNotifications19AE210E"
    })
})

# #7
# # Presence and Absence
# # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/README.html#presence-and-absence

def test_Presence(fixture_fun):
    
    fixture_fun.has_resource_properties("AWS::SNS::Subscription", {
    "TopicArn": assertions.Match.object_like({
        "Rif":  assertions.Match.absent()
    })
})

