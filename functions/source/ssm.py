# Lambda function to perform ssm operations
from __future__ import print_function
import json
import logging
import os
import requests
import boto3
from botocore.exceptions import ClientError

# set logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# global constants
CFN_SUCCESS = 'SUCCESS'
CFN_FAILED = 'FAILED'

# setup client
region = os.environ['AWS_REGION']
ssm = boto3.client('ssm', region_name=region)

def lambda_handler(event, context):
    """
    The Lambda function handler
    
    Create SSM secure string parameter in AWS Systems Manager parameter store.
    
    Args:
        event: The event passed by Lambda
        context: The context passed by Lambda
        
    """
    logger.debug("EVENT: %s", str(event))
    
    # If it's a DELETE event
    if event['RequestType'] == 'Delete':
        try:
            logger.debug('Deleting parameter - GITHUBTOKEN')
            
            # Delete GITHUBTOKEN securestring parameter
            ssm.delete_parameter(
                Name='GITHUBTOKEN'
            )
            
            # Signal success
            send_cfnresponse(event, context, CFN_SUCCESS, {})
            
        except Exception as inst:
            logger.error(inst)
            send_cfnresponse(event, context, CFN_FAILED, {})
    elif event['RequestType'] == 'Create':
        # If it's a CREATE event
        try:
            
            # Extract GITHUBTOKEN
            githubtoken = event['ResourceProperties']['GITHUBTOKEN']
            
            # Extract KMS KEY Resource Id
            kms_key_id = event['ResourceProperties']['KMS_KEY_ID']
            logger.debug('Github token = {}, kms_key_id = {}'.format(githubtoken, kms_key_id))
            
            # Create GITHUBTOKEN SecureString parameter
            response_data = ssm.put_parameter(
                Name='GITHUBTOKEN',
                Description='Github token',
                Value=githubtoken,
                Type='SecureString',
                KeyId=kms_key_id
            )
            
            # Signal SUCCESS
            send_cfnresponse(event, context, CFN_SUCCESS, response_data)
            
        except Exception as ex:
            print(ex)
            send_cfnresponse(event, context, CFN_FAILED, {})

def send_cfnresponse(event, context, response_status, data):
    """
    Signal SUCCESS or FAILURE to CloudFormation
    
    Args:
        event: The event passed by Lambda
        context: The context passed by Lambda
        response_status: Signal status SUCCESS or FAILURE
        data: The response data to be passed to CloudFormation
        
    """
    response_url = event['ResponseURL']
    logger.debug('CFN response url: {}'.format(response_url))

    # Create response body
    response_body = {}
    response_body['Status'] = response_status
    response_body['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name + ' ' + context.log_group_name
    response_body['PhysicalResourceId'] = context.log_stream_name
    response_body['StackId'] = event['StackId']
    response_body['RequestId'] = event['RequestId']
    response_body['LogicalResourceId'] = event['LogicalResourceId']
    response_body['Data'] = data

    json_response = json.dumps(response_body)
    logger.debug("Response body:\n%s", json_response)

    headers = {
        'content-type': '',
        'content-length': str(len(json_response))
    }

    try:
        response = requests.put(response_url, data=json_response, headers=headers)
        logger.info("Status code: %s", response.reason)
    except Exception as e:
        logger.error("send(..) failed executing requests.put(..): %s", str(e))