from setuptools import find_packages, setup

setup(
    name="common",  # Required
    version="0.0.0",  # Required
    author="Altis Labs, Inc.",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    python_requires=">=3.11.6",
    install_requires=[
        "aws-requests-auth==0.4.3",
        "backoff==2.2.1; python_version >= '3.7' and python_version < '4.0'",
        "boto3==1.26.165; python_version >= '3.7'",
        "botocore==1.29.165; python_version >= '3.7'",
        "certifi==2023.11.17; python_version >= '3.6'",
        "charset-normalizer==2.0.12; python_version >= '3'",
        "gevent==22.10.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
        "gql[requests]==3.4.1",
        "graphql-core==3.2.3; python_version >= '3.6' and python_version < '4'",
        "greenlet==3.0.3; platform_python_implementation == 'CPython'",
        "idna==3.6; python_version >= '3'",
        "jmespath==1.0.1; python_version >= '3.7'",
        "multidict==6.0.4; python_version >= '3.7'",
        "pydantic==1.10.13; python_version >= '3.7'",
        "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "requests==2.27.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
        "requests-toolbelt==0.10.1",
        "s3transfer==0.6.2; python_version >= '3.7'",
        "setuptools==69.0.3; python_version >= '3.8'",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "typing-extensions==4.9.0; python_version >= '3.8'",
        "urllib3==1.26.18; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
        "yarl==1.9.4; python_version >= '3.7'",
        "zope.event==5.0; python_version >= '3.7'",
        "zope.interface==6.1; python_version >= '3.7'",
    ],
)
