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
    # aws_sqs as sqs,
)
from constructs import Construct
from resources import constants as constants
class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #cloudWatchRole
        my_role = self.create_lambda_role()
        
        """ Creating Lambda Functions to deploy DBApp and WHApp """

        fn = self.create_lambda("WHLambda","./resources","WHApp.lambda_handler",my_role)
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        
        dbLambda = self.create_lambda("DBLambda","./resources","DBApp.lambda_handler",my_role)
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        
        schedule=events_.Schedule.rate(Duration.minutes(60))
        
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events_targets/LambdaFunction.html
        target=targets_.LambdaFunction(handler=fn)

        #Defininng a rule to convert my lambda into cronjob
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events.html
        rule = events_.Rule(self, "WHRule",schedule = schedule , targets = [target])
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        """ Create SNS Topic and Subscription """
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        topic =  sns_.Topic(self, "WHNotifications")

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions_.EmailSubscription("muhammadmaaz.khattak.skipq@gmail.com"))

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
        topic.add_subscription(subscriptions_.LambdaSubscription(dbLambda))



        #Alarms
        for x in constants.urls:
            dimensions = {
                'URL' : x
            }
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            availability_metric = cw_.Metric(
                metric_name = constants.AvailabilityMetric,
                namespace = constants.namespace,
                dimensions_map = dimensions
        )
         # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            availability_alarm = cw_.Alarm(self, x+" Availibility Errors",
            metric=availability_metric,
            evaluation_periods=60,
            threshold=1,
            comparison_operator=cw_.ComparisonOperator.LESS_THAN_THRESHOLD,
            
            
            )
            """ Use an SNS topic as an alarm action. """
            #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))


            latency_metric = cw_.Metric(
                metric_name = constants.LatencyMetric,
                namespace = constants.namespace,
                dimensions_map = dimensions,
            )
            latency_alarm = cw_.Alarm(self, x+" Latency Errors",
            metric=latency_metric,
            evaluation_periods=60,
            threshold=0.5,
            comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            
            )
            """ Use an SNS topic as an alarm action. """
            #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        """ Creating DynamoDB table"""    
        dbtable = self.create_db_table()
        dbtable.grant_full_access(dbLambda)
        
        dbLambda.add_environment('Table_Name',dbtable.table_name)
        

            
        
    #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
    def create_lambda(self,id,asset,handler,role):
        """ 
            Create Lambda function from the construct library
            Parameters:
                assets(str) -> Stack file path for the app to be deployed on lambda
                handler (str) -> Handler function to execute
                role (str) -> IAM role for lambda Function
            Return:
                Lambda Function
        """
        return lambda_.Function(self,
        id = id , 
        handler = handler , 
        runtime=lambda_.Runtime.PYTHON_3_9,
        code=lambda_.Code.from_asset(asset),
        role = role,
    )
    def create_lambda_role(self):
        """ 
            Create role iam user
            Parameters:
                assumed_by (IPrincipal) -> The Iam principal which can assume this role
                managed_policies -> (IManagedPolicy) -> A list to managed policies
            Return:
                Role object
        """
        lambda_role = iam_.Role(self ,"lambda_role",
        assumed_by = iam_.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies =[
            iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            ])
        return lambda_role
    """ Creating a dynamodb 

            Parameters:
            partition_key - Unique id
            sort_key -> Just like composite primary keys
    
    """
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html

    def create_db_table(self):
        table = db_.Table(self, "AlarmTable",
            partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
            sort_key = db_.Attribute(name="Timestamp" , type=db_.AttributeType.STRING),)
        return table


