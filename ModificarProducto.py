import boto3
import json

def lambda_handler(event, context):
    data = event['body']
    tenant_id = data['tenant_id']
    producto_id = data['producto_id']
    updates = data['updates']
    
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
    update_expr = "SET " + ", ".join(f"#{k}=:{k}" for k in updates.keys())
    expr_attr_names = {f"#{k}": k for k in updates.keys()}
    expr_attr_vals = {f":{k}": v for k, v in updates.items()}
    response = table.update_item(
        Key={'tenant_id': tenant_id, 'producto_id': producto_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_vals,
        ReturnValues="UPDATED_NEW"
    )
    return {'statusCode': 200, 'response': response}
