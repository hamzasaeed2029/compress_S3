import os
import boto3
import zipfile
from io import BytesIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        # Download the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read()
        
        # Compress the file content
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(os.path.basename(object_key), file_content)
        
        # Upload the compressed file to S3
        compressed_object_key = f'{object_key}.zip'
        s3_client.put_object(Bucket='highqbucket', Key=compressed_object_key, Body=zip_buffer.getvalue())
        
        # Delete the original object from S3
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)

