import json
import logging
import threading
import boto3
import cfnresponse

# set logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# setup client
s3 = boto3.client('s3')


def delete_NonVersionedobjects(bucket):
    logger.info('Collecting data from' + bucket)
    paginator = s3.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket)
    objects = []
    for page in result:
        try:
            for k in page['Contents']:
                objects.append({'Key': k['Key']})
                logger.info('deleting objects')
                s3.delete_objects(Bucket=bucket, Delete={
                    'Objects': objects})
                objects = []
        except:
            pass
            logger.info('bucket is already empty')


def delete_versionedobjects(bucket):
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
        except:
            pass
    logger.info('bucket already empty')


def timeout(event, context):
    logger.error(
        'Execution is about to time out, sending failure response to CloudFormation')
    cfnresponse.send(event, context, cfnresponse.FAILED, {}, None)


def handler(event, context):
    # make sure we send a failure to CloudFormation if the function is going to timeout
    timer = threading.Timer((context.get_remaining_time_in_millis(
    ) / 1000.00) - 0.5, timeout, args=[event, context])
    timer.start()

    logger.info(f'Received event: {json.dumps(event)}')
    status = cfnresponse.SUCCESS
    try:
        dest_bucket = event['ResourceProperties']['DestBucket']
        if event['RequestType'] == 'Delete':
            CheckifVersioned = s3.get_bucket_versioning(Bucket=dest_bucket)
            logger.info(CheckifVersioned)
            if 'Status' in CheckifVersioned:
                logger.info(CheckifVersioned['Status'])
                logger.info('This is a versioned Bucket')
                delete_versionedobjects(dest_bucket)
            else:
                logger.info('This is not a versioned bucket')
                delete_NonVersionedobjects(dest_bucket)
        else:
            logger.info('Nothing to do')
    except Exception as e:
        logger.error(f'Exception: {e}', exc_info=True)
        status = cfnresponse.FAILED
    finally:
        timer.cancel()
        cfnresponse.send(event, context, status, {}, None)
