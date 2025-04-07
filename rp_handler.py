import os
from uuid import uuid4

import boto3
import runpod
from DepthFlow.Scene import DepthScene

BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
AWS_REGION = os.environ.get("AWS_REGION")

def output_file_name():
    return f"{uuid4()}.mp4"

def output_path(file_name):
    if not os.path.exists("output"):
        os.makedirs("output")
    
    return os.path.join("output", file_name)

def init_scene():
    scene = DepthScene(backend="headless")
    return scene

def upload_file_to_s3(file_path, key):
    s3 = boto3.client('s3')
    print(file_path, key, BUCKET_NAME)

    s3.upload_file(file_path, BUCKET_NAME, key)

def handler(event):
    image = event['input']['image']
    output_file = output_file_name()
    output = output_path(output_file)
    
    scene = init_scene()
    scene.input(image=image)
    scene.main(output=output)

    s3_key = f"runpod/{output_file}"
    upload_file_to_s3(output, s3_key)

    return {
        "output": f"https://s3.{AWS_REGION}.amazonaws.com/{BUCKET_NAME}/{s3_key}"
    }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
