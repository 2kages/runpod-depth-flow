import os
from enum import StrEnum
from uuid import uuid4

import boto3
import runpod
from DepthFlow.Animation import Animation
from DepthFlow.Scene import DepthScene

BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
AWS_REGION = os.environ.get("AWS_REGION")

class AnimationPreset(StrEnum):
    ORBITAL = "orbital"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    ZOOM = "zoom"
    CIRCLE = "circle"
    DOLLY = "dolly"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

def addAnimationPreset(scene: DepthScene, preset: str):
    # check if preset is valid
    if not AnimationPreset.has_value(preset):
        raise ValueError(f"Invalid preset: {preset}")

    if preset == AnimationPreset.ORBITAL:
        scene.config.animation.add(Animation.Orbital())
    elif preset == AnimationPreset.VERTICAL:
        scene.config.animation.add(Animation.Vertical())
    elif preset == AnimationPreset.HORIZONTAL:
        scene.config.animation.add(Animation.Horizontal())
    elif preset == AnimationPreset.ZOOM:
        scene.config.animation.add(Animation.Zoom())
    elif preset == AnimationPreset.CIRCLE:
        scene.config.animation.add(Animation.Circle())
    elif preset == AnimationPreset.DOLLY:
        scene.config.animation.add(Animation.Dolly())

def output_file_name() -> str:
    return f"{uuid4()}.mp4"

def output_path(file_name: str) -> str:
    if not os.path.exists("output"):
        os.makedirs("output")
    
    return os.path.join("output", file_name)

def init_scene() -> DepthScene:
    scene = DepthScene(backend="headless")
    return scene

def upload_file_to_s3(file_path: str, key: str):
    s3 = boto3.client('s3')
    print(file_path, key, BUCKET_NAME)

    s3.upload_file(file_path, BUCKET_NAME, key)

def handler(event):
    image = event['input']['image']
    animation_presets = event['input'].get('animation_presets', [AnimationPreset.ORBITAL])
    output_file = output_file_name()
    output = output_path(output_file)
    
    scene = init_scene()
    scene.input(image=image)
    
    for preset in animation_presets:
        addAnimationPreset(scene, preset)

    scene.main(output=output)

    s3_key = f"runpod/{output_file}"
    upload_file_to_s3(output, s3_key)

    return {
        "key": s3_key,
        "video": f"https://s3.{AWS_REGION}.amazonaws.com/{BUCKET_NAME}/{s3_key}"
    }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
