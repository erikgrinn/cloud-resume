import boto3
import json
import os

def lambda_handler(event, context):
    table_name = os.environ.get('TABLE_NAME', 'visitCounter')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)
    
    try:
        response = table.update_item(
            Key={'id': 'counter'},
            UpdateExpression='ADD visits :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        visits = int(response['Attributes']['visits'])  # Convert Decimal to int
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},  
            'body': json.dumps({'visits': visits})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},  
            'body': json.dumps({'error': str(e)})
        }