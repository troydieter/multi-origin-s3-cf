from aws_cdk import (
    Stack, Tags,
)
from aws_cdk.aws_cloudfront import Distribution, BehaviorOptions
from aws_cdk.aws_cloudfront_origins import S3Origin, OriginGroup
from aws_cdk.aws_s3 import Bucket, BucketEncryption
from constructs import Construct


class MultiOriginS3CfStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stage: str, context, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ###
        # Tag everything
        Tags.of(self).add("project", context["project"])
        primary_origin_bucket = self.create_origin_bucket(stage, "primary_origin")
        secondary_origin_bucket = self.create_origin_bucket(stage, "secondary_origin")
        Distribution(self, f"{context['tld']}_distribution",
                     default_behavior=BehaviorOptions(origin=OriginGroup(
                         primary_origin=S3Origin(primary_origin_bucket),
                         fallback_origin=S3Origin(secondary_origin_bucket),
                     ))
                     )

    def create_origin_bucket(self, stage: str, bucket_name: str):
        return Bucket(self,
                      f"{bucket_name}-{stage}",
                      encryption=BucketEncryption.S3_MANAGED,
                      enforce_ssl=True,
                      public_read_access=False,
                      versioned=True)
