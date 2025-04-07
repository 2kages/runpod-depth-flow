# RunPod serverless image for DepthFlow

This is a RunPod serverless image for generating video from an input image using DepthFlow.

See the full document of DepthFlow [here](https://github.com/BrokenSource/DepthFlow)

# Requirements:

- ffmpeg
- s3 account
- run on any NVIDIA GPU serverless on RunPod

# prepare environment variable 

create `.env` file

```
AWS_ACCOUNT_ID=<account id>
AWS_ACCESS_KEY_ID=<access key>
AWS_SECRET_ACCESS_KEY=<secret key>
AWS_REGION=<region>
AWS_BUCKET_NAME=<bucket>
```

then run 

```
source .env
```

# Input schema 

```json
{
  "input": {
    "image": "<your image url>",
    "presets": ["<list of animation preset>"]
  }
}
```

List of available animation preset:
* orbital
* vertical
* horizontal
* zoom
* circle
* dolly

The `presets` input is optional. We will use `orbital` if not provided. You can also combine multiple presets

# Output schema

```json
{
  "output": {
    "video": "<output url>"
  }
}
```

# LICENSE

DepthFlow license is GNU Affero General Public License v3.0