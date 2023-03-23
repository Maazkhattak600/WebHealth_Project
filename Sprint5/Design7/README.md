
# Welcome to your CDK Python project!

## Problem Statement:

***Design & Develop -*** What if we have a 15MB file that we have to upload on S3 using API gateway. We have the limitation that our API gateway has the maximum payload capacity of 10MB. How will you solve this problem?

## Proposed Solution:

To solve this problem we will create a presigned url and will upload files throught that url.

1)  We will create S3 bucket, API Gateway , Lambda function. 
2)  User will request through the API Gateway and lambda will be triggered and will create a ***Presigned-URL***.
3)  That URL will be given back to the user and now user will be able to upload files larger than 10MB using that URL.

### Design:

![design7 drawio](https://user-images.githubusercontent.com/112099093/208153837-7499218f-86e4-4882-a46b-31fb886cda12.png)

### Development:

Infrastructure will include S3 bucket, API gateway , Lambda Function.

So First of all user will request for the Preassigned url through API gateway and Lambda function will generate that.


![Capture33](https://user-images.githubusercontent.com/112099093/208154711-efdbc9eb-7a07-4989-bc1f-8064ed870185.PNG)

We will get url from there and then using Postman to put the file into the S3 bucket. That file will be larger than 10Mb and there will be no problem in uplaoding that file through API gateway. 

![Capture34](https://user-images.githubusercontent.com/112099093/208155791-b8cea0a3-c242-4451-9546-f590d2497978.PNG)

That file will be stored into S3 bucket using the Presigned-URL.

![Capture35](https://user-images.githubusercontent.com/112099093/208155929-c70646cd-d832-4355-8ef4-ec03a50b34a9.PNG)

## Author
Muhammad Maaz Khattak  
Email : muhammadmaaz.khattak.skipq@gmail.com





## Acknowledgments


* [SkipQ](https://www.skipq.org/)
