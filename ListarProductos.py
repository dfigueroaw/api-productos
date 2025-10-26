import boto3
import json

def lambda_handler(event, context):
    data = json.loads(event['body'])
    tenant_id = data['tenant_id']
    
    token = event['headers']['Authorization']
    lambda_client = boto3.client('lambda')
    payload_string = json.dumps({'token': token})
    invoke_response = lambda_client.invoke(FunctionName="ValidarTokenAcceso",
                                           InvocationType='RequestResponse',
                                           Payload=payload_string)
    response = json.loads(invoke_response['Payload'].read())
    if response['statusCode'] == 403:
        return {'statusCode': 403, 'status': 'Forbidden - Acceso No Autorizado'}
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_productos')
    result = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('tenant_id').eq(tenant_id))
    return {'statusCode': 200, 'items': result['Items']}
