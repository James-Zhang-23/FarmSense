import boto3
import credentials as keys
from boto3.dynamodb.conditions import Key, Attr

# send email using AWS SES
def send_plain_email(msg):
    ses_client = boto3.client("ses", 
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    region_name=keys.AWS_DEFAULT_REGION)
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "yuzhe@usc.edu",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": msg,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Warning: Bad environment condition",
            },
        },
        Source="yuzhe@usc.edu",
    )

if __name__ == '__main__':
    send_plain_email("hello world!")
