##
# S3操作
##

import boto3
import pickle
import io
import load_settings

S3_ENDPOINT = load_settings.S3_ENDPOINT
S3_ACCESS_KEY_ID = load_settings.S3_ACCESS_KEY_ID
S3_SECRET_ACCESS_KEY = load_settings.S3_SECRET_ACCESS_KEY
S3_BUCKET_NAME = load_settings.S3_BUCKET_NAME
PATH = "cbbot_settings2/"


def set_bucket():
    """
    s3Bucketを設定
    """
    s3 = boto3.resource('s3',
                        endpoint_url=S3_ENDPOINT,
                        aws_access_key_id=S3_ACCESS_KEY_ID,
                        aws_secret_access_key=S3_SECRET_ACCESS_KEY
                        )
    bucket = s3.Bucket(S3_BUCKET_NAME)
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
