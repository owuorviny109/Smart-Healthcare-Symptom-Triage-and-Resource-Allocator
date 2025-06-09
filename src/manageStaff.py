# src/manageStaff.py - FINAL PRODUCTION-READY VERSION

import json
import boto3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')
schedule_table = dynamodb.Table(os.environ['SCHEDULE_TABLE'])

def lambda_handler(event, context):
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }

    # Handle the OPTIONS preflight request for CORS
    if event['requestContext']['http']['method'] == 'OPTIONS':
        return {'statusCode': 204, 'headers': cors_headers}

    try:
        http_method = event['requestContext']['http']['method']
        
        if http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            
            # The HTML form sends `workerName`, so we expect `workerName`
            required_fields = ['workerId', 'workerName', 'role', 'status', 'maxLoad']
            if not all(field in body for field in required_fields):
                return {
                    'statusCode': 400, 
                    'headers': cors_headers,
                    'body': json.dumps({'error': f'Missing required fields. Received: {body}'})
                }

            item = {
                'workerId': body['workerId'],
                'workerName': body['workerName'], # Correctly expects workerName
                'role': body['role'],
                'status': body['status'],
                'maxLoad': int(body['maxLoad']),
                'currentLoad': 0
            }
            schedule_table.put_item(Item=item)
            logger.info(f"Successfully added/updated worker: {body['workerId']}")
            
            return {'statusCode': 201, 'headers': cors_headers, 'body': json.dumps(item)}

        elif http_method == 'GET':
            response = schedule_table.scan()
            staff_list = response.get('Items', [])
            logger.info(f"Fetched {len(staff_list)} staff members.")
            return {'statusCode': 200, 'headers': cors_headers, 'body': json.dumps(staff_list, default=int)}

    except Exception as e:
        logger.error(f"Error in manageStaff: {e}")
        return {'statusCode': 500, 'headers': cors_headers, 'body': json.dumps({'error': f'Internal server error: {str(e)}'})}