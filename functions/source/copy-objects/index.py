import json
import logging
import threading
import boto3
import cfnresponse
import os
from s3transfer.manager import TransferManager, TransferConfig

# set logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# setup client
region = os.environ['AWS_REGION']
s3 = boto3.client('s3', region_name=region)
manager = TransferManager(s3, TransferConfig(max_request_concurrency=20))


def copy_objects(source_bucket, dest_bucket, prefix, objects):
    logger.info(f"Processing keys: '{json.dumps(objects)}'")
    for o in objects:
        key = prefix + o
        copy_source = {
            'Bucket': source_bucket,
            'Key': key,
        }
        logger.info(
            f"Copying: '{key}' from '{source_bucket}' to '{dest_bucket}'.")
        manager.copy(copy_source=copy_source,
                     bucket=dest_bucket, key=key).result()


def delete_objects(bucket):
    logger.info('Collecting data from' + bucket)
    paginator = s3.get_paginator('list_object_versions')
    result = paginator.paginate(Bucket=bucket)
    objects = []
    for page in result:
        try:
            for k in page['Versions']:
                objects.append({'Key': k['Key'], 'VersionId': k['VersionId']})
            try:
                for k in page['DeleteMarkers']:
                    version = k['VersionId']
                    key = k['Key']
                    objects.append({'Key': key, 'VersionId': version})
            except:
                pass
            logger.info('deleting objects')
            s3.delete_objects(Bucket=bucket, Delete={'Objects': objects})
            # objects = []
        except:
            pass
    logger.info('bucket already empty')


def timeout(event, context):
    logger.error(
        'Execution is about to time out, sending failure response to CloudFormation')
    cfnresponse.send(event, context, cfnresponse.FAILED, {}, None)


def handler(event, context):
    # make sure we send a failure to CloudFormation if the function is going to timeout
    remaining_time_in_ms = (
        context.get_remaining_time_in_millis() / 1000.00) - 0.5
    timer = threading.Timer(remaining_time_in_ms,
                            timeout, args=[event, context])
    timer.start()

    logger.info(f'Received event: {json.dumps(event)}')
    status = cfnresponse.SUCCESS
    try:
        source_bucket = event['ResourceProperties']['SourceBucket']
        dest_bucket = event['ResourceProperties']['DestBucket']
        prefix = event['ResourceProperties']['Prefix']
        objects = event['ResourceProperties']['Objects']
        if event['RequestType'] == 'Delete':
            delete_objects(dest_bucket)
        else:
            copy_objects(source_bucket, dest_bucket, prefix, objects)
    except Exception as e:
        logger.error(f'Exception: {e}', exc_info=True)
        status = cfnresponse.FAILED
    finally:
        timer.cancel()
        cfnresponse.send(event, context, status, {}, None)
