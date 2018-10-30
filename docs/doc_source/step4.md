# Step 4\. Verify the Deployment<a name="step4"></a>

 In the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/), in the **Outputs** tab of your stack, choose the URL for **CodePipelineURL**\. This will redirect you to the AWS CodePipeline console\. 

 You should see the CI/CD pipeline for your AWS CloudFormation templates being triggered and the *Source* stage in progress, as shown in Figure 3\. 

![\[CI/CD pipeline for the templates in your GitHub repository\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/images/codepipeline.png)

**Figure 3: CI/CD pipeline for the templates in your GitHub repository**