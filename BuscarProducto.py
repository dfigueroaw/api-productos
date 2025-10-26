import boto3
import json

def lambda_handler(event, context):
    data = json.loads(event['body'])
    tenant_id = data['tenant_id']
    producto_id = data['producto_id']
    
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
    result = table.get_item(Key={'tenant_id': tenant_id, 'producto_id': producto_id})
    return {'statusCode': 200, 'item': result.get('Item', {})}
