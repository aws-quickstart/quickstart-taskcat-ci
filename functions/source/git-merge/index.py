# Lambda function to merge git branches
import json
import logging
import requests
import boto3
import os

# set logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# setup client
region = os.environ['AWS_REGION']
secretsmanager = boto3.client('secretsmanager', region_name=region)

# global constants
merge_endpoint = 'https://api.github.com/repos/{owner}/{repo}/merges'

# setup client
region = os.environ['AWS_REGION']
ssm = boto3.client('ssm', region_name=region)
code_pipeline = boto3.client('codepipeline', region_name=region)


def put_job_success(job: str, message: str):
    """Notify CodePipeline of a successful job

    Args:
        job: The CodePipeline job ID
        message: A message to be logged relating to the job status

    Raises:
        Exception: Any exception thrown by .put_job_success_result()

    """
    logger.info(f'Putting job success. {message}')
    code_pipeline.put_job_success_result(jobId=job)


def put_job_failure(job: str, message: str):
    """Notify CodePipeline of a failed job

    Args:
        job: The CodePipeline job ID
        message: A message to be logged relating to the job status

    Raises:
        Exception: Any exception thrown by .put_job_failure_result()

    """
    logger.info(f'Putting job failure. {message}')
    failure_details = {'message': message, 'type': 'JobFailed'}
    code_pipeline.put_job_failure_result(
        jobId=job, failureDetails=failure_details)


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
        raise Exception(
            'Your UserParameters JSON must include the base branch name')

    if 'headBranch' not in decoded_parameters:
        # Validate that the head branch name is provided, otherwise fail the job
        # with a helpful message.
        raise Exception(
            'Your UserParameters JSON must include the head branch name')

    if 'owner' not in decoded_parameters:
        # Validate that the repo owner is provided, otherwise fail the job
        # with a helpful message.
        raise Exception('Your UserParameters JSON must include the repo owner')

    if 'repo' not in decoded_parameters:
        # Validate that the repo name is provided, otherwise fail the job
        # with a helpful message.
        raise Exception('Your UserParameters JSON must include the repo name')

    if 'secretsManagerArn' not in decoded_parameters:
        # Validate that the Secrets Manager ARN is provided, otherwise fail the
        # job with a helpful message.
        raise Exception(
            'Your UserParameters JSON must include the Secrets Manager ARN')

    return decoded_parameters


def handler(event, context):
    """
    The Lambda function handler

    Merge the develop branch into master branch of the github repo.

    Args:
        event: The event passed by Lambda
        context: The context passed by Lambda

    """
    logger.info(f'Received event: {json.dumps(event)}')

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
        # token_id = params['tokenId']
        secretsmanager_arn = params['secretsManagerArn']

        # Get secret from Secrets Manager
        secret = json.loads(secretsmanager.get_secret_value(
            SecretId=secretsmanager_arn)['SecretString'])

        # Get GitHub token from secret
        github_token = secret['Token']

        # Construct merge endpoint
        global merge_endpoint
        merge_endpoint = merge_endpoint.format(
            owner=repo_owner, repo=repo_name)

        # Construct post data
        data = {
            'base': base_branch,
            'head': head_branch
        }

        # Construct header
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'token {github_token}'
        }

        # Submit request
        result = requests.post(
            merge_endpoint, data=json.dumps(data), headers=headers)
        logger.debug(result)

        if result.status_code == requests.codes.created:
            # Merge completed successfully.
            message = 'Merge completed successfully.'
            logger.info(message)
            put_job_success(job_id, message)
        elif result.status_code == requests.codes.no_content:
            # Merge not needed. Base already contains the head, nothing to merge.
            message = 'Nothing to merge.'
            logger.info(message)
            put_job_success(job_id, message)
        else:
            # Merge failed.
            status = str(result.raise_for_status())
            logger.error(status)
            put_job_failure(job_id, f'Merge failed: {status}')

    except Exception as e:
        # If any other exceptions which we didn't expect are raised
        # then fail the job and log the exception message.
        logger.error(f'Function failed due to exception: {e}')
        put_job_failure(job_id, f'Function exception: {str(e)}')

    logger.info('Function execution complete')
    return True
