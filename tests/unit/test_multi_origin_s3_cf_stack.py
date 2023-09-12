import aws_cdk as core
import aws_cdk.assertions as assertions

from multi_origin_s3_cf.multi_origin_s3_cf_stack import MultiOriginS3CfStack

# example tests. To run these tests, uncomment this file along with the example
# resource in multi_origin_s3_cf/multi_origin_s3_cf_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MultiOriginS3CfStack(app, "multi-origin-s3-cf")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
