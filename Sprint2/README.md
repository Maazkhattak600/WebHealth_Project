# Web Health Stack
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![AWS cdk 2.51.1](https://img.shields.io/badge/aws_cdk_lib-2.51.1-yellow.svg)](https://pypi.org/project/aws-cdk-lib/2.51.1/)



## Description

In this Project I am monitoring the health of 4 different websites based on the availability and latency metrics. I have also publish the metrics to the AWS cloudwatch where we can monitor the health of websites. Web health will be monitor every 60 minutes (Cron job). I have set an alarm that will be raised whenever the metric values breached the threshold. To get to know when alarm is raised I have added SNS topic and subscription that will send me an Email whenever metric values breach the threshold. After that I have create a dynamodb that will strore the relevant SNS into the dynamoDB table. 


## Getting Started

### Dependencies

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
##### Get the latency and availability values of the websites
![Capture1](https://user-images.githubusercontent.com/112099093/202847460-76f5179b-a593-473c-8c1b-15df94ac061b.PNG)

##### Published the metrics to the AWS CloudWatch and Set an Alarm if metrics value breached the threshold
![Capture2](https://user-images.githubusercontent.com/112099093/202847532-0e7e5d2a-f9f1-4a69-b5e9-898306376b03.PNG)

 ##### Added SNS topic and Subscription and then connceted it with alarm so that whenever an alarm is raised I will get an email informing me that alarm is raised
 ![Capture3](https://user-images.githubusercontent.com/112099093/202847659-dbbf4041-c69c-45b5-9a35-56f8bfe65d0e.PNG)

##### After that created a dynamoDB table and extract the relevant information from the SNS and stroe it into the dynamoDB. Connected the SNS with DynamoDb lambda so whenever an alarm is raised Relevant info from SNS will store into the dynamoDB

![Capture4](https://user-images.githubusercontent.com/112099093/202847803-eba254a6-e541-4de6-b65e-cb8e66115316.PNG)



## Author
Muhammad Maaz Khattak  
Email : muhammadmaaz.khattak.skipq@gmail.com





## Acknowledgments


* [SkipQ](https://www.skipq.org/)

