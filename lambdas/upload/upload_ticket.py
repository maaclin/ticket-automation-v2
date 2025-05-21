import os
import json
import time
import base64
import boto3

# Read bucket name and region from env vars
BUCKET = os.getenv("BUCKET_NAME", "rental-tickets-uploads")
REGION = os.getenv("AWS_REGION", "eu-west-2")

s3 = boto3.client("s3", region_name=REGION)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        img_b64 = body.get("image")
        if not img_b64:
            return {
                "statusCode": 400,
                "body": json.dumps({"success": False, "error": "No image provided"})
            }
        img_bytes = base64.b64decode(img_b64)
        key = f"{int(time.time())}.jpg"
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=img_bytes,
            ContentType="image/jpeg"
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "key": key})
        }
    except Exception as e:
        print("Error uploading to S3:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "error": str(e)})
        }


