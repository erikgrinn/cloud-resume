import unittest
import json
import boto3
from moto import mock_aws
from lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    
    @mock_aws
    def test_lambda_handler_success(self):
        # Create mock DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        table = dynamodb.create_table(
            TableName='visitCounter',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Add initial item
        table.put_item(Item={'id': 'counter', 'visits': 5})
        
        # Call the lambda function
        result = lambda_handler({}, {})
        
        # Assert the response
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Access-Control-Allow-Origin'], '*')
        
        body = json.loads(result['body'])
        self.assertEqual(body['visits'], 6)

if __name__ == '__main__':
    unittest.main()