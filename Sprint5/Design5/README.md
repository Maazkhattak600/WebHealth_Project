
# Welcome to Design-5!

## Problem Statement:
***Design & Develop*** - Suppose there are 10 files uploading to S3 bucket each day. For each file received on cloud storage, you have a mechanism to process the file. During the processing, your code parses the text and counts the number of times each word is repeated in the file. For example, in the following text: “Hello World and Hello There”, your code should be able to say that "hello" has been used twice, "world" has occurred once and so on. Then it will store the results in some storage and email to some email address after successful processing.

## Proposed Solution:
1) We will use Amazon S3 to store the files, and then use AWS Lambda to process the files as they are uploaded. We can trigger a Lambda function to run whenever a file is uploaded to S3, and the function can parse the text in the file and count the number of times each word is used.

2) Once the function has processed the file, it can store the results in another service such as Amazon DynamoDB, which is a fully managed NoSQL database. Then, the function can use Amazon SES (Simple Email Service) to send an email with the results to the specified email address.

## Design:

![Design5 drawio drawio](https://user-images.githubusercontent.com/112099093/207568536-bd9ce9f0-db9f-4612-8374-1ace7d80b137.png)

### Development:

First we will upload a file to S3 bucket. 

![Capture30](https://user-images.githubusercontent.com/112099093/208151115-5aa10b95-b2ad-48eb-9f95-5fafee3fd52b.PNG)

After that Lambda will be triggered, parse the text in file and count the number of times each word is written and will store the file name and word-counts in DynamoDb.

![Capture31](https://user-images.githubusercontent.com/112099093/208151875-38265131-29ad-4dfb-8776-cc6927339b25.PNG)

And atlast email will be sent to inform that data has been stored into the dynamoDB.

![Capture32](https://user-images.githubusercontent.com/112099093/208152072-268ec9f5-901d-468b-933a-4ae6d7e98d62.PNG)

