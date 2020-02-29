##
# cloudcube操作
##

import boto3
from urllib.parse import urlparse
import pickle
import io
import load_settings

CLOUDCUBE_ACCESS_KEY_ID = load_settings.CLOUDCUBE_ACCESS_KEY_ID
CLOUDCUBE_SECRET_ACCESS_KEY = load_settings.CLOUDCUBE_SECRET_ACCESS_KEY
CLOUDCUBE_URL = load_settings.CLOUDCUBE_URL
BUCKET_NAME = urlparse(CLOUDCUBE_URL).netloc.split('.')[0]
PATH = urlparse(CLOUDCUBE_URL).path[1:] + "/cbbot_settings/"


def set_bucket():
    """
    s3Bucketを設定
    """
    s3 = boto3.resource('s3',
                        aws_access_key_id=CLOUDCUBE_ACCESS_KEY_ID,
                        aws_secret_access_key=CLOUDCUBE_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(BUCKET_NAME)
    return bucket


def save_text(text: str, filename: str, bucket=None):
    """
    s3Bucketにテキストを保存
    """
    if bucket is None:
        bucket = set_bucket()
    f = io.BytesIO()
    pickle.dump(text, f)
    f.seek(0)
    bucket.upload_fileobj(f, Key=PATH + filename)


def load_text(filename: str, bucket=None):
    """
    s3Bucketからテキストを読み込み
    """
    if bucket is None:
        bucket = set_bucket()
    f = io.BytesIO()
    bucket.download_fileobj(PATH + filename, f)
    f.seek(0)
    return pickle.loads(f.read())


if __name__ == "__main__":
    save_text("てすてす", "test")
    print(load_text("test"))
