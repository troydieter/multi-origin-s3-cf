from aws_cdk import (
    Stack, Tags,
)
from aws_cdk.aws_certificatemanager import Certificate
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

        top_level_domain = context["tld"]
        primary_certificate = self.create_certificate(stage, cert_value=top_level_domain)

        primary_origin_bucket = self.create_origin_bucket(stage, "primary_origin")
        secondary_origin_bucket = self.create_origin_bucket(stage, "secondary_origin")
        Distribution(self, f"{context['tld']}_distribution",
                     default_behavior=BehaviorOptions(origin=OriginGroup(
                         primary_origin=S3Origin(primary_origin_bucket),
                         fallback_origin=S3Origin(secondary_origin_bucket)
                     )),
                     comment=f"{context['tld']}_distribution",
                     domain_names=[f"{top_level_domain}", f"*.{top_level_domain}", f"www.${top_level_domain}"],
                     certificate=primary_certificate
                     )

    def create_origin_bucket(self, stage: str, bucket_name: str):
        return Bucket(self,
                      f"{bucket_name}-{stage}",
                      encryption=BucketEncryption.S3_MANAGED,
                      enforce_ssl=True,
                      public_read_access=False,
                      versioned=True)

    def create_certificate(self, stage: str, cert_value: str):
        return Certificate(self,
                           f"{cert_value}-{stage}",
                           domain_name=cert_value,
                           subject_alternative_names=[f"*.{cert_value}", f"www.{cert_value}"])
