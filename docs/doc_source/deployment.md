# Deployment Steps<a name="deployment"></a>

## Prerequisites<a name="prerequisites"></a>

 This Quick Start requires a GitHub repository that contains the AWS CloudFormation templates you want to test as part of the CI/CD pipeline\. Your GitHub repository must have a specific folder structure: 
+  A **templates** folder, which includes your AWS CloudFormation templates\. Templates can be in either JSON or YAML format\. 
+  A **ci** folder, which includes a TaskCat configuration file named **taskcat\.yml** and an input **parameters file**\. The configuration file should specifiy the template name that needs to be tested, the parameters file, and the tests that TaskCat should run\. 

 For detailed information about these input files, see the [TaskCat documentation](https://aws-quickstart.github.io/input-files.html)\. 

 If you want to give TaskCat a trial run, you can download and use any of the AWS CloudFormation templates and configuration files in the Quick Start GitHub organization at [https://github\.com/aws\-quickstart](https://github.com/aws-quickstart)\. 