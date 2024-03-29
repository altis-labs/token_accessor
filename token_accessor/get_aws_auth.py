from urllib.parse import urlparse

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth


def get_aws_auth(url: str) -> AWSRequestsAuth:
    session = boto3.Session()
    credentials = session.get_credentials()
    region = session.region_name

    parsed_uri = urlparse(url)

    return AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=parsed_uri.netloc,
        aws_region=region,
        aws_service="execute-api",
    )
