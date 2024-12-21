import boto3
from warrant import Cognito
import os

def get_unauthenticated_credentials():
    COGNITO_IDENTITY_POOL_ID = os.getenv("AWS_COGNITO_IDENTITY_POOL_ARN")
    COGNITO_REGION = os.getenv("AWS_COGNITO_REGION")

    cognito_identity = boto3.client("cognito-identity", region_name=COGNITO_REGION)
    
    # Get Identity ID for unauthenticated user
    identity_response = cognito_identity.get_id(
        IdentityPoolId=COGNITO_IDENTITY_POOL_ID
    )
    identity_id = identity_response["IdentityId"]
    
    # Get temporary AWS credentials for the unauthenticated user
    credentials_response = cognito_identity.get_credentials_for_identity(
        IdentityId=identity_id
    )
    return credentials_response["Credentials"]
