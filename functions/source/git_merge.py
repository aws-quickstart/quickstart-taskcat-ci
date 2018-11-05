# Lambda function to merge git branches

import json
import logging
import requests
import boto3
import os

# set logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# global constants
merge_endpoint = 'https://api.github.com/repos/{owner}/{repo}/merges'

# setup client
region = os.environ['AWS_REGION']
ssm = boto3.client('ssm', region_name=region)
code_pipeline = boto3.client('codepipeline', region_name=region)

def put_job_success(job, message):
    """Notify CodePipeline of a successful job
    
    Args:
        job: The CodePipeline job ID
        message: A message to be logged relating to the job status
        
    Raises:
        Exception: Any exception thrown by .put_job_success_result()
    
    """
    logger.info('Putting job success')
    logger.info(message)
    code_pipeline.put_job_success_result(jobId=job)
  
def put_job_failure(job, message):
    """Notify CodePipeline of a failed job
    
    Args:
        job: The CodePipeline job ID
        message: A message to be logged relating to the job status
        
    Raises:
        Exception: Any exception thrown by .put_job_failure_result()
    
    """
    logger.info('Putting job failure')
    logger.info(message)
    code_pipeline.put_job_failure_result(jobId=job, failureDetails={'message': message, 'type': 'JobFailed'})


def get_user_params(job_data):
    """Decodes the JSON user parameters and validates the required properties.
    
    Args:
        job_data: The job data structure containing the UserParameters string which should be a valid JSON structure
        
    Returns:
        The JSON parameters decoded as a dictionary.
        
    Raises:
        Exception: The JSON can't be decoded or a property is missing.
        
    """
    try:
        # Get the user parameters which contain the base branch name, branch to be merged, repo owner and repo name
        user_parameters = job_data['actionConfiguration']['configuration']['UserParameters']
        decoded_parameters = json.loads(user_parameters)
            
    except Exception as e:
        # We're expecting the user parameters to be encoded as JSON
        # so we can pass multiple values. If the JSON can't be decoded
        # then fail the job with a helpful message.
        raise Exception('UserParameters could not be decoded as JSON')
    
    if 'baseBranch' not in decoded_parameters:
        # Validate that the base branch name is provided, otherwise fail the job
        # with a helpful message.
        raise Exception('Your UserParameters JSON must include the base branch name')
    
    if 'headBranch' not in decoded_parameters:
        # Validate that the head branch name is provided, otherwise fail the job
        # with a helpful message.
        raise Exception('Your UserParameters JSON must include the head branch name')
    
    if 'owner' not in decoded_parameters:
        # Validate that the repo owner is provided, otherwise fail the job
        # with a helpful message.
        raise Exception('Your UserParameters JSON must include the repo owner')
    
    if 'repo' not in decoded_parameters:
        # Validate that the repo name is provided, otherwise fail the job
        # with a helpful message.
        raise Exception('Your UserParameters JSON must include the repo name')
    
    return decoded_parameters


def get_ssm_parameter(param_name):
    """
    Get value of the given parameter from the AWS SSM Parameter store
    
    Args:
        key: The parameter name whose value needs to be fetched from Parameter store
    
    Returns:
        The value of the given parameter from Parameter store
    
    Raises:
        Exception: Given parameter name doesn't exist in the Parameter store
    """
    try:
        # Get the requested parameter
        response = ssm.get_parameter(
            Name= param_name,
            WithDecryption=True)
    
    except Exception as e:
        # If the given parameter name doesn't exist in SSM parameter store
        # then fail.
        logger.error(e)
        raise Exception("Error getting parameter value {}".format(param_name))

    return response['Parameter']['Value']


def lambda_handler(event, context):
    """
    The Lambda function handler
    
    Merge the develop branch into master branch of the github repo.
    
    Args:
        event: The event passed by Lambda
        context: The context passed by Lambda
        
    """
    logger.debug("EVENT: " + str(event))
    
    try:
        # Extract the Job ID
        job_id = event['CodePipeline.job']['id']
        
        # Extract the Job Data 
        job_data = event['CodePipeline.job']['data']
        
        # Extract the params
        params = get_user_params(job_data)
        
        repo_owner = params['owner']
        repo_name = params['repo']
        base_branch = params['baseBranch']
        head_branch = params['headBranch']
        
        # Get github token from parameter store
        github_token = get_ssm_parameter('GITHUBTOKEN')
        
        # Construct merge endpoint
        global merge_endpoint
        merge_endpoint = merge_endpoint.format(owner=repo_owner, repo=repo_name)
        
        # Construct post data
        data = {
          'base': base_branch,
          'head': head_branch
        }
        
        # Construct header
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token  ' + github_token
        }
        
        # Submit request
        result = requests.post(merge_endpoint, data=json.dumps(data), headers=headers)
        logger.debug(result)
        
        if result.status_code == requests.codes.created:
            # Merge completed successfully.
            logger.info('Merge completed successfully!')
            put_job_success(job_id, 'Merge complete!')
        elif result.status_code == requests.codes.no_content:
            # Merge not needed. Base already contains the head, nothing to merge.
            logger.info('Nothing to merge!')
            put_job_success(job_id, 'Nothing to merge!')
        else:
            # Merge failed.
            logger.error(str(result.raise_for_status()))
            put_job_failure(job_id, 'Merge failed: ' + status)

    except Exception as e:
        # If any other exceptions which we didn't expect are raised
        # then fail the job and log the exception message.
        logger.info('Function failed due to exception.') 
        logger.error(e)
        put_job_failure(job_id, 'Function exception: ' + str(e))
    
    logger.info("Function execution complete")
    return True