import base64
import logging
import json
import boto3
#import numpy
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

print('Loading Lambda function')

runtime=boto3.Session().client('sagemaker-runtime')
s3 = boto3.client('s3')
endpoint_Name='pytorch-inference-2023-11-03-18-24-23-219'
bucket_name = 'sagemaker-instance-bucket'


def lambda_handler(event, context):

    object = s3.get_object(Bucket=bucket_name, Key=event['url'])
    data = object['Body'].read()
#    x=event['content']
#    aa=x.encode('ascii')
#    bs=base64.b64decode(data)
    print('Context:::',context)
    print('EventType::',type(event))
#    bs=event

    response=runtime.invoke_endpoint(EndpointName=endpoint_Name,
                                    #ContentType="application/json",
                                    ContentType="image/jpeg",                                    
                                    Accept='application/json',
                                    Body=data) # Body=bytearray(data),
                                    #Body=json.dumps(bs))
    
    result=response['Body'].read().decode('utf-8')
    sss=json.loads(result)
    
    return {
        'statusCode': 200,
        'headers' : { 'Content-Type' : 'text/plain', 'Access-Control-Allow-Origin' : '*' },
        'type-result':str(type(result)),
        'Content-Type-In':str(context),
        'body' : json.dumps(sss)
        #'updated_result':str(updated_result)

        }