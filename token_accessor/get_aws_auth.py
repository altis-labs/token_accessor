import os
from typing import Optional
from urllib.parse import urlparse

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth


def get_aws_auth(url: str, session: Optional[boto3.Session] = None) -> AWSRequestsAuth:
    if session is None:
        session = boto3.Session()

    credentials = session.get_credentials()
    region = session.region_name

    if region is None:
        region = os.getenv("AWS_REGION", "ca-central-1")

    parsed_uri = urlparse(url)

    return AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=parsed_uri.netloc,
        aws_region=region,
        aws_service="execute-api",
    )
