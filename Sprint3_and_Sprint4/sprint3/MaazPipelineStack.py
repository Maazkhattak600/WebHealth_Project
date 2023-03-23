#import aws_cdk as cdk
from aws_cdk import (
    pipelines as pipelines_,
    Stack,
    aws_codepipeline_actions as actions_,
    SecretValue as secret_,
    aws_iam as iam_,
    aws_codebuild as codebuild

)
from constructs import Construct
from sprint3.MaazStage import MaazStage

class MaazPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Accessing the Github Source Repo
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/SecretValue.html#aws_cdk.SecretValue
        source = pipelines_.CodePipelineSource.git_hub("muhammadmaaz2022skipq/Sirius_Python", "main",
                                                        authentication = secret_.secrets_manager("MaazToken"),
                                                        trigger = actions_.GitHubTrigger('POLL'),
                                                        
                                         
        ) 
        # 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

        # Adding Shell step to synthesize Application
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html
        synth=pipelines_.ShellStep("Synth",
                                    commands = ["cd MaazKhattak/Sprint3_and_Sprint4/","npm install -g aws-cdk","pip install -r requirements.txt","cdk synth"],
                                    primary_output_directory = "MaazKhattak/Sprint3_and_Sprint4/cdk.out",
                                    
                                    input = source,
        )
        
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodeBuildStep.html
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codebuild/BuildEnvironment.html#aws_cdk.aws_codebuild.BuildEnvironment
        # This is a CodeBuild Step that is used to run the API tests.
        pyresttest = pipelines_.CodeBuildStep("MaazApiTests",
                                commands=[],
                                build_environment = codebuild.BuildEnvironment(build_image = codebuild.LinuxBuildImage.from_asset(self,"Image" , directory = "docker-image/").from_docker_registry(name="docker:dind"),
                                privileged = True,),
                                partial_build_spec = codebuild.BuildSpec.from_object(
                                    {
                                        "version": 0.2,
                                        "phases": {
                                            "install": {
                                            "commands": [
                                                "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
                                                "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\""
                                            ]
                                            },
                                            "pre_build": {
                                            "commands": [
                                                "cd MaazKhattak/Sprint3_and_Sprint4/docker-image",
                                                "docker build -t apitests:maaz ."
                                            ]
                                            },
                                            "build": {
                                            "commands": [

                                                "docker run --name crudtests apitests:maaz"
                                            ]
                                            }
                                        }
                                        }
                                    
                                    ),      
        )
        
        # Create Pipeline
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        pipeline = pipelines_.CodePipeline(self, "MaazPipelineSprint3", synth = synth)
        
        

        """ Adding Stages """
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html
        # Beta Satge
        betaTesting = MaazStage(self , "Beta")
        pipeline.add_stage(betaTesting,
                pre=[
                pipelines_.ShellStep("Synth",
                                    input = source,
                                    commands = ["cd MaazKhattak/Sprint3_and_Sprint4/",
                                    "npm install -g aws-cdk",
                                    "pip install -r requirements.txt",
                                    "pip install -r requirements-dev.txt",
                                    "python3 -m pytest",
                                    ],),],
                post=[pyresttest],
        )
        # Production Stage
        prod = MaazStage(self , "prod")

        # Manual Approval 
        
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html
        pipeline.add_stage(prod,
            pre=[
                pipelines_.ManualApprovalStep("PromotetoProd")
    ]
        )