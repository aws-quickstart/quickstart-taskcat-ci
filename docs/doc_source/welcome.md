# CI/CD Pipeline for AWS CloudFormation Templates on the AWS Cloud Using AWS TaskCat<a name="welcome"></a>

**Deployment Guide**

*Shivansh Singh and Tony Vattathil — Solutions Architects, AWS Quick Start team*

*October 2018*

 This Quick Start deployment guide describes how to deploy a continuous integration and continuous delivery \(CI/CD\) pipeline with AWS TaskCat on the Amazon Web Services \(AWS\) Cloud, to automatically test and deploy AWS CloudFormation templates from a GitHub repository\. [AWS CloudFormation](https://aws.amazon.com/cloudformation/) templates automate the deployment of the CI/CD environment\. 

 The guide is for IT infrastructure architects, administrators, and DevOps professionals who are planning to implement or extend their AWS CloudFormation\-based workloads on the AWS Cloud\. 

 The following links are for your convenience\. Before you launch the Quick Start, please review the architecture, configuration, and other considerations discussed in this guide\. 
+ If you have an AWS account and you’re already familiar with AWS services and TaskCat, you can [launch the Quick Start](https://fwd.aws/RKbgm) to build an architecture for the workflow shown in [Figure 1](architecture.md#figure1)\. The deployment takes approximately 15 minutes\. If you’re new to AWS or to TaskCat, please review the details and follow the [step\-by\-step instructions](deployment.md) provided later in this guide\.

   

   [ ![\[Image NOT FOUND\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/images/launch-button.png) ](https://fwd.aws/RKbgm) 

   
+  If you want to take a look under the covers, you can [view the AWS CloudFormation template](https://fwd.aws/K7nG8) that automates the deployment\. 

   

   [ ![\[Image NOT FOUND\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/images/view-template.png) ](https://fwd.aws/K7nG8) 

## About Quick Starts<a name="about"></a>

 [Quick Starts](https://aws.amazon.com/quickstart/) are automated reference deployments for key workloads on the AWS Cloud\. Each Quick Start launches, configures, and runs the AWS compute, network, storage, and other services required to deploy a specific workload on AWS, using AWS best practices for security and availability\. 