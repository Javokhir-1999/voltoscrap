import logging
import sys
import threading

import boto3
from botocore.exceptions import ClientError
import os

from config.settings import ACCESS_KEY, SECRET_ACCESS_KEY, BUCKET_NAME


def upload_public_pdf(file_name, folder, id):
    """Upload a file to an S3 bucket
    """
    name = id.hex + '.pdf'
    # Upload the file
    s3_client = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)
    try:
        response = s3_client.upload_file(
            file_name,
            BUCKET_NAME,
            f'{folder}/{name}',
            ExtraArgs={'ACL': 'public-read'},
            Callback=ProgressPercentage(file_name)
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_public_tex(file_name, folder, id):
    """Upload a file to an S3 bucket
    """
    name = id.hex + '.tex'
    # Upload the file
    s3_client = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)
    try:
        response = s3_client.upload_file(
            file_name,
            BUCKET_NAME,
            f'{folder}/{name}',
            ExtraArgs={'ACL': 'public-read'},
            Callback=ProgressPercentage(file_name)
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()