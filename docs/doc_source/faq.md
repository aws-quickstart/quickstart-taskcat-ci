# FAQ<a name="faq"></a>

**Q\.** I encountered a CREATE\_FAILED error when I launched the Quick Start\.

**A\.** If AWS CloudFormation fails to create the stack, we recommend that you relaunch the template with **Rollback on failure** set to **No**\. \(This setting is under **Advanced** in the AWS CloudFormation console, **Options** page\.\) With this setting, the stack’s state will be retained and the instance will be left running, so you can troubleshoot the issue\.

**Important**  
When you set **Rollback on failure** to **No**, you'll continue to incur AWS charges for this stack\. Please make sure to delete the stack when you finish troubleshooting\.

For additional information, see [Troubleshooting AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html) on the AWS website\. 

**Q\.** I encountered a size limitation error when I deployed the AWS CloudFormation template\.

**A\.** We recommend that you launch the Quick Start templates from the location we’ve provided or from another S3 bucket\. If you deploy the template from a local copy on your computer or from a non\-S3 location, you might encounter template size limitations when you create the stack\. For more information about AWS CloudFormation limits, see the [AWS documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html)\. 

**Q\.** Where can I find the TaskCat report?

**A\.** The report for each TaskCat run is saved in the S3 bucket\. The path to the S3 bucket is listed as the value for the **TaskCatReports** key in the **Outputs** section of your CloudFormation stack, as illustrated in [Figure 2](step3.md#figure2)\. 