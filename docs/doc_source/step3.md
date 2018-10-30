# Step 2\. Launch the Quick Start<a name="step3"></a>

**Note**  
 You are responsible for the cost of the AWS services used while running this Quick Start reference deployment\. There is no additional cost for using this Quick Start\. For full details, see the pricing pages for each AWS service you will be using in this Quick Start\. Prices are subject to change\. 

****

1.  [Launch the AWS CloudFormation template](https://fwd.aws/RKbgm) into your AWS account\. 

    [ ![\[Image NOT FOUND\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/images/launch-button.png) ](https://fwd.aws/RKbgm) 

   The deployment takes about 15 minutes to complete\.

1.  Check the region that’s displayed in the upper\-right corner of the navigation bar, and change it if necessary\. This is where the CI/CD pipeline for AWS CloudFormation templates will be built\. The template is launched in the US West \(Oregon\) Region by default\. 

1.  On the **Select Template** page, keep the default setting for the template URL, and then choose **Next**\. 

1.  On the **Specify Details** page, change the stack name if needed\. Review the parameters for the template\. Provide values for the parameters that require input\. For all other parameters, review the default settings and customize them as necessary\. When you finish reviewing and customizing the parameters, choose **Next**\. 

    In the following tables, parameters are listed and described by category\. 

    [View template](https://fwd.aws/K7nG8) 

    *GitHub Configuration:*     
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/step3.html)

    *AWS Quick Start Configuration:*     
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/step3.html)

1.  On the **Options** page, you can [specify tags](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) \(key\-value pairs\) for resources in your stack and [set advanced options](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-add-tags.html)\. When you’re done, choose **Next**\. 

1.  On the **Review** page, review and confirm the template settings\. Under **Capabilities**, select the check box to acknowledge that the template will create IAM resources\. 

1.  Choose **Create** to deploy the stack\. 

1.  Monitor the status of the stack\. When the status is **CREATE\_COMPLETE**, the CI/CD pipeline for AWS CloudFormation templates is ready\. 

    The **Outputs** tab for the stack will provide information about the resources that were created, as shown in Figure 2\. <a name="figure2"></a>  
![\[Quick Start stack outputs\]](http://docs.aws.amazon.com/quickstart/latest/cicd-taskcat/images/stack-outputs.png)

   **Figure 2: Quick Start stack outputs**