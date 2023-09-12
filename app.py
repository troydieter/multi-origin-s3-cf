#!/usr/bin/env python3
import os

import aws_cdk as cdk

from multi_origin_s3_cf.multi_origin_s3_cf_stack import MultiOriginS3CfStack

app = cdk.App()
context = {
    "tld": app.node.try_get_context("tld"),
    "project": app.node.try_get_context("project")
}

MultiOriginS3CfStack(app, "MultiOriginS3CfStack", env=cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]), stage="develop", context=context)

app.synth()
