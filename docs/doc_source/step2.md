# Step 2\. Set Up Your GitHub Token and Collect Your Information<a name="step2"></a>

****

1.  Log in to your [GitHub](https://github.com/) account\. 

1.  Follow the steps in the [GitHub documentation](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) to create a new \(OAuth 2\) token with the following scopes \(permissions\): `admin:repo_hook` and `repo`\. If you already have a token with these permissions, you can use that\. You can find a list of all your personal access tokens in [https://github\.com/settings/tokens](https://github.com/settings/tokens)\. 

1.  Make a note of the following information: 
   +  GitHub token name\. 
   +  GitHub repository name – This repository should have the folder structure and files described earlier in the [Prerequisites](deployment.md#prerequisites) section\. 
   +  Source branch name – This is the branch that CodePipeline should monitor for any changes\. 
   +  Release branch name – This is the branch that the source branch will be merged into after a successful test\. 

      You will be prompted for this information when you launch the Quick Start\. 