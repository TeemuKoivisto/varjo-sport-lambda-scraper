
import boto3

import os

from scrapy.extensions.feedexport import BlockingFeedStorage

SERVERLESS_STAGE = os.environ.get('SERVERLESS_STAGE')
AWS_PROFILE = os.environ.get('AWS_PROFILE')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
KEY_NAME = os.environ.get('OUTPUT_FILE')
ACL = 'public-read'
CACHE_CONTROL = 'max-age=120'

class UnisportS3FeedStorage(BlockingFeedStorage):
    def __init__(self, uri):
        if SERVERLESS_STAGE == 'local':
            session = boto3.Session(profile_name=AWS_PROFILE)
            self.s3_client = session.client('s3')
        else:
            self.s3_client = boto3.client('s3')

    def _store_in_thread(self, file):
        file.seek(0)
        self.s3_client.put_object(Bucket=BUCKET_NAME, Key=KEY_NAME, Body=file, ACL=ACL, CacheControl=CACHE_CONTROL)
