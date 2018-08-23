# quickstart-taskcat-ci

## Overview

![Architecture Diagram](assets/Taskcat%20CI%20Quick%20Start%20architecture%20diagram.png)
Create a CI/CD pipeline to test Quick Starts. This Quick Start uses following AWS services:
- AWS CodePipeline
- AWS CodeBuild
- Amazon S3
- AWS Lambda
- AWS CloudFormation

The pipeline created by this Quick Start consist of 3 stages - Source, Build and Deploy. Source stage is integrated with Github repository which is monitored for any changes. If any changes to the source branch is detected, it triggers the pipeline. Source stage pulls the latest version of the code from the github branch, zips it and upload it into an S3 bucket. Build stage uses AWS CodeBuild and [Taskcat](https://github.com/aws-quickstart/taskcat) to test the CloudFormation templates. Code Build takes the zip file from the S3 bucket, un-packs it and runs Taskcat to test the CloudFormation templates. If test passes successfully, build job is marked as success. The last stage is Deploy, which invokes lambda function to merge the source branch of github repository into release branch, on successfull build.
Taskcat reports are uploaded to the artifact S3 bucket.

## Pre-requisites
1. Github repository - Quick Start github repository (or fork repo) which you want to use as a source for the CI/CD pipeline.
2. Github token - Goto github (https://github.com/settings/tokens) to create an OAuth2 token with following permissions - admin:repo_hook and repo. This is needed to merge branches via Git API.

## Steps to deploy
1. Login to the AWS console and select a region where you want to deploy this Quick Start.
2. Create parameter in SSM Parameter store - Go to Systems Manager console, select Parameter store from the left navigation and create the following parameter. Currently, CloudFormation doesn't support creating SSM parameter with SecureString Type, therefore this manual step is needed.
 1. Name: GITHUBTOKEN
 	Description: Github token used by Lambda function to merge branches via API
 	Type: SecureString
 	KMS key source: My current account
 	KMS Key ID: alias/aws/ssm
 	Value: <Github-token>
3. Go to CloudFormation console and launch taskcat-ci-pipeline.template to deploy the CI/CD pipeline. Make sure you are in the same region where you created the parameters in previous step.