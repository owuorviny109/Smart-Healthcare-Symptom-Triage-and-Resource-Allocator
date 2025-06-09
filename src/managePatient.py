# src/managePatient.py - FINAL CORS-ENABLED VERSION

import json
import boto3
import os
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')
patients_table = dynamodb.Table(os.environ['PATIENTS_TABLE'])

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
        
        if http_method == 'GET':
            patient_id = event['pathParameters']['nationalId']
            logger.info(f"Attempting to get patient with ID: {patient_id}")
            response = patients_table.get_item(Key={'nationalId': patient_id})
            if 'Item' in response:
                return {'statusCode': 200, 'headers': cors_headers, 'body': json.dumps(response['Item'], default=str)}
            else:
                return {'statusCode': 404, 'headers': cors_headers, 'body': json.dumps({'error': 'Patient not found'})}

        elif http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            required_fields = ['nationalId', 'fullName', 'dateOfBirth', 'gender', 'phoneNumber']
            if not all(field in body for field in required_fields):
                return {'statusCode': 400, 'headers': cors_headers, 'body': json.dumps({'error': 'Missing required fields'})}

            item = {
                'nationalId': body['nationalId'], 'fullName': body['fullName'],
                'dateOfBirth': body['dateOfBirth'], 'gender': body['gender'],
                'phoneNumber': body['phoneNumber'], 'nextOfKinName': body.get('nextOfKinName', ''),
                'nextOfKinPhone': body.get('nextOfKinPhone', '')
            }
            patients_table.put_item(Item=item)
            logger.info(f"Successfully created patient: {item['nationalId']}")
            return {'statusCode': 201, 'headers': cors_headers, 'body': json.dumps(item)}

    except ClientError as e:
        logger.error(f"DynamoDB Error: {e.response['Error']['Message']}")
        return {'statusCode': 500, 'headers': cors_headers, 'body': json.dumps({'error': 'Database error'})}
    except Exception as e:
        logger.error(f"Error in managePatient: {e}")
        return {'statusCode': 500, 'headers': cors_headers, 'body': json.dumps({'error': f'Internal server error: {str(e)}'})}