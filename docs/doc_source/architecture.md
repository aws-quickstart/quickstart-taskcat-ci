# Architecture<a name="architecture"></a>

 Deploying this Quick Start with **default parameters** builds the following CI/CD pipeline environment in the AWS Cloud\. <a name="figure1"></a>

![\[CI/CD pipeline for CloudFormation templates on AWS\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/images/pipeline-workflow.png)

**Figure 1: CI/CD pipeline for CloudFormation templates on AWS**

 The Quick Start sets up the following: 
+  A pipeline created by CodePipeline, which is triggered when a commit is made to the referenced branch of the Github repository used in the source stage\. 
+  A build project in CodeBuild to run TaskCat and launch AWS CloudFormation templates for testing\. 
+  A Lambda function that merges the source branch of the Github repository with the release branch\. 
+  AWS Identity and Access Management \(IAM\) roles for the Lambda function and the build project\. 
+  An S3 bucket to stash the build artifacts temporarily and to store the TaskCat report\. 