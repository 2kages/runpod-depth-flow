# RunPod serverless image for DepthFlow

This is a RunPod serverless image for generating video from an input image using DepthFlow.

See the full document of DepthFlow [here](https://github.com/BrokenSource/DepthFlow)

# Requirements:

- ffmpeg
- s3 account
- run on any cheap GPU serverless (T4 or L4 should be more than enough)

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

```
{
    "input": {
        "image": "<your image url>"
    }
}
```

# Output schema

```
{'output': '<output url>'}
```
