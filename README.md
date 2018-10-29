# quickstart-taskcat-ci
## CI/CD Pipeline for AWS CloudFormation Templates Using TaskCat on the AWS Cloud


This Quick Start deploys a continuous integration and continuous delivery (CI/CD) pipeline on the Amazon Web Services (AWS) Cloud for automatically testing AWS CloudFormation templates from a GitHub repository. 

The Quick Start sets up a CI/CD environment that includes AWS TaskCat for testing, AWS CodePipeline for continuous integration, and AWS CodeBuild as your build service.

TaskCat is a tool that tests AWS CloudFormation templates. It creates stacks in multiple AWS Regions simultaneously and generates a report with a pass/fail grade for each region. You can specify the regions, indicate the number of Availability Zones you want to include in the test, and pass in the AWS CloudFormation parameter values you want to test. You can use this Quick Start to test any AWS CloudFormation templates, including nested templates, from a GitHub repository.

TaskCat is available as an [open-source tool in GitHub](https://github.com/aws-quickstart/taskcat).

![Quick Start architecture for CI/CD Pipeline for AWS CloudFormation templates on AWS](https://d0.awsstatic.com/partner-network/QuickStart/datasheets/cicd-taskcat-pipeline.png)

For architectural details, best practices, step-by-step instructions, and customization options, see the 
[deployment guide](https://fwd.aws/mnpXR).

To post feedback, submit feature ideas, or report bugs, use the **Issues** section of this GitHub repo.
If you'd like to submit code for this Quick Start, please review the [AWS Quick Start Contributor's Kit](https://aws-quickstart.github.io/). 
