import boto3
import json

def lambda_handler(event, context):
    print(event)
    producto = event['body']
    
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
    response = table.put_item(Item=producto)
    return {'statusCode': 200, 'response': response}
