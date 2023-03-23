# AWS CODEPIPELINE
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![AWS cdk 2.51.1](https://img.shields.io/badge/aws_cdk_lib-2.51.1-yellow.svg)](https://pypi.org/project/aws-cdk-lib/2.51.1/)



## Description

Im this Sprint I have automated the deployment process using CI/CD. First I Created an AWS Codepipeline. Then Integrated the AWS Codepipeline wiht Github. Add Alpha/Beta/Gamma Stages to the pipeline and automated testing using pytest running. I have also built CloudWatch metrics (Throttles and duration) to monitor the operational health of my Application, Added alarms to it and if also Autoroll configuration allowing rollback to last version of Application. Then Setup the beta/prod environments and deploy using AWS Codedeploy. Also added manual Approval for the prod stage.


## Getting Started

### Requirements

* AWS account
* VS code 
* Linux/Windows

### Installing
```
nvm install v16.3.0 && nvm use v16.3.0 && nvm alias default v16.3.0
npm install -g aws-cdk
```
```
cdk init app --language python
```

```
python3 -m pip install -r requirements.txt
```


### Executing program


```
cdk synth
cdk deploy
```
### Create a AWS CodePiepeline , Add stages (Beta,Prod) to it and Deploy the Pipeline.

![Capture5](https://user-images.githubusercontent.com/112099093/204154559-7eacf952-cb48-4f2a-aa92-5126b0f501d2.PNG)

### Beta Stage
![Capture6](https://user-images.githubusercontent.com/112099093/204154655-3bdd996f-cd57-4fd9-8eae-c328537477ab.PNG)


### Built two operational CloudWatch metrics for web crawler and alarms added to it. (Duration and throttles)
![Capture7](https://user-images.githubusercontent.com/112099093/204155539-3dbf86ba-e10d-46a5-acf5-fc39836c4786.PNG)

In ***Sprint4*** I have created a CRUD Api gateway endpoint for the web crawler to create/read/update/delete the target list.

![Capture8](https://user-images.githubusercontent.com/112099093/205707048-46aec34f-f6ea-4571-828a-47357cecdaf8.PNG)

After that I have created a URL table, So the Client can Perform CRUD operations on it.

![Capture9](https://user-images.githubusercontent.com/112099093/205707169-407ebe39-a9fb-4c6e-8358-21f9cc55c417.PNG)

And then those URLs from URL table will be monitored on CloudWatch.
![Capture10](https://user-images.githubusercontent.com/112099093/205707260-7297df1e-c02e-4f87-b2d6-cf20cde46509.PNG)




## Author
Muhammad Maaz Khattak  
Email : muhammadmaaz.khattak.skipq@gmail.com





## Acknowledgments


* [SkipQ](https://www.skipq.org/)

