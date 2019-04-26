from .base import *


DEBUG = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', default=None)

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', default=None)

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', default=None)

AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', default=None)

AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION', default=None)

AWS_DEFAULT_ACL = None

AWS_QUERYSTRING_AUTH = False
