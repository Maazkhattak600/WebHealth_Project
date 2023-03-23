from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    RemovalPolicy,
    aws_cloudwatch as cw_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as db_ ,
    aws_codedeploy as codedeploy_,
    aws_apigateway as apigateway_,
    # aws_sqs as sqs,
)
from constructs import Construct
from resources import constants as constants
class Sprint3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #cloudWatchRole
        my_role = self.create_lambda_role()
        
        #""" Creating Lambda Functions to deploy DBApp and WHApp """

        fn = self.create_lambda("WHLambda","./resources","WHApp.lambda_handler",my_role)
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        
        dbLambda = self.create_lambda("DBLambda","./resources","DBApp.lambda_handler",my_role)
        dbLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        apiLambda = self.create_lambda("ApiLambda","./resources","ApiApp.lambda_handler",my_role)
        apiLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
         
        
        """ Step 1 :Obtain AWS Lambda Metrics"""
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.metric_duration
        duration_metric = fn.metric_duration()

        # Step2 : Create Alarms on metrics
        duration_alarm = cw_.Alarm(self, "Duration Errors",
            metric=duration_metric,
            evaluation_periods=60,
            threshold=600000,
            comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD,)
        
        # Throttle Metric
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.metric_throttles
        throttle_metric = fn.metric_throttles()
        throttle_alarm = cw_.Alarm(self, "Throttle Errors",
            metric=throttle_metric,
            evaluation_periods=60,
            threshold=0,
            comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            )

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html    
        version = fn.current_version
        alias = lambda_.Alias(self, "LambdaAlias",
            alias_name="Prod",
            version=version
        )
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "LambdaDeployment",
                #application=application,
                alias=alias,
                alarms = [duration_alarm ,throttle_alarm],
                deployment_config= codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
                # auto_rollback=codedeploy_.AutoRollbackConfig(
                #     failed_deployment=True,  # default: true
                #     stopped_deployment=True,  # default: false
                #     deployment_in_alarm=True
                #     )
                )
        
        
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        schedule=events_.Schedule.rate(Duration.minutes(60))
        
         #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events_targets/LambdaFunction.html
        target=targets_.LambdaFunction(handler=fn)

         #Defininng a rule to convert my lambda into cronjob
         #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events.html
        rule = events_.Rule(self, "WHRule",schedule = schedule , targets = [target])
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        # """ Create SNS Topic and Subscription """
         # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        topic =  sns_.Topic(self, "WHNotifications")

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions_.EmailSubscription("muhammadmaaz.khattak.skipq@gmail.com"))

         # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
        topic.add_subscription(subscriptions_.LambdaSubscription(dbLambda))

        # Sprint 4 - Removing Stack URL Metrics as they are defined in WHAPP using Boto3 SDK

   

        # """ Creating DynamoDB Alarm table"""    
        dbtable = self.create_db_table()
        dbtable.grant_full_access(dbLambda)
        
        dbLambda.add_environment('AlarmTable',dbtable.table_name)
        
        """Sprint 4"""
    
        # """ Creating URL Table"""
        # #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
        urlTable = self.create_urlTable()
        urlTable.grant_full_access(apiLambda)
        urlTable.grant_read_write_data(apiLambda)
        apiLambda.add_environment('URLTable',urlTable.table_name)
        
        #WHApp --> URLTable 
        fn.add_environment('snsTopic',topic.topic_name)
        fn.add_environment('URLTable',urlTable.table_name)
        
        """Creating API Gateway"""
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/README.html
        api = apigateway_.LambdaRestApi(self, "MaazAPI",
                                handler= apiLambda,
                                proxy=False
                            ) 
        getUrl = api.root.add_resource("GetUrl")
        getUrl.add_method("GET")
        updateUrl = api.root.add_resource("updateUrl")
        updateUrl.add_method("PATCH")
        postUrl = api.root.add_resource("postUrl")
        postUrl.add_method("POST")
        deleteUrl = api.root.add_resource("deleteUrl")        
        deleteUrl.add_method("DELETE")
        
        
        
        
        

            
        
     #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
    def create_lambda(self,id,asset,handler,role):
        #  """ 
        #      Create Lambda function from the construct library
        #      Parameters:
        #          assets(str) -> Stack file path for the app to be deployed on lambda
        #          handler (str) -> Handler function to execute
        #          role (str) -> IAM role for lambda Function
        #      Return:
        #          Lambda Function
        #  """
        return lambda_.Function(self,
        id = id , 
        handler = handler , 
        runtime=lambda_.Runtime.PYTHON_3_9,
        code=lambda_.Code.from_asset(asset),
        role = role,
    )
    def create_lambda_role(self):
        #  """ 
        #      Create role iam user
        #      Parameters:
        #          assumed_by (IPrincipal) -> The Iam principal which can assume this role
        #          managed_policies -> (IManagedPolicy) -> A list to managed policies
        #      Return:
        #          Role object
        #  """
        lambda_role = iam_.Role(self ,"lambda_role",
        assumed_by = iam_.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies =[
            iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            ])
        return lambda_role
    # """ Creating a dynamodb 

    #         Parameters:
    #         partition_key - Unique id
    #         sort_key -> Just like composite primary keys
    
    # """
    # # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html

    def create_db_table(self):
        table = db_.Table(self, "AlarmTable",
            partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
            sort_key = db_.Attribute(name="Timestamp" , type=db_.AttributeType.STRING),)
        return table

    def create_urlTable(self):
        table = db_.Table(self, "URLTable",
            partition_key = db_.Attribute(name="URL", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
    )
        return table
    
    
