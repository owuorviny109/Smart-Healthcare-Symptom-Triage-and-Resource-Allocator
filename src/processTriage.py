# src/processTriage.py - FINAL CORS-ENABLED VERSION

import json
import boto3
import os
import uuid
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')
queue_table = dynamodb.Table(os.environ['QUEUE_TABLE'])
rules_table = dynamodb.Table(os.environ['RULES_TABLE'])

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
        logger.info(f"Triage Event Received: {event}")
        body = json.loads(event.get('body', '{}'))
        symptoms = body.get('symptoms', [])
        national_id = body.get('nationalId', None)

        if not symptoms or not national_id:
            logger.error(f"Validation Error: Missing required fields. Received nationalId: {national_id}, symptoms: {symptoms}")
            return {'statusCode': 400, 'headers': cors_headers, 'body': json.dumps({'error': 'Symptoms and a patient National ID are required.'})}

        rules_response = rules_table.scan()
        symptom_weights = {rule['symptom']: int(rule['weight']) for rule in rules_response.get('Items', [])}
        score = sum(symptom_weights.get(symptom, 1) for symptom in symptoms)
        logger.info(f"Calculated score for patient {national_id}: {score}")

        if score >= 10: urgency_level = 'High'
        elif score >= 5: urgency_level = 'Medium'
        else: urgency_level = 'Low'

        triage_id = str(uuid.uuid4())
        timestamp = int(time.time())
        item_to_queue = {
            'triageId': triage_id, 'patientNationalId': national_id, 'symptoms': symptoms,
            'urgencyScore': int(score), 'urgencyLevel': urgency_level,
            'status': 'PENDING_ASSIGNMENT', 'assignedWorkerId': None, 'timestamp': timestamp
        }
        queue_table.put_item(Item=item_to_queue)
        logger.info(f"Adding to TriageQueue: {item_to_queue}")

        return {
            'statusCode': 200, 'headers': cors_headers,
            'body': json.dumps({
                'triageId': triage_id, 'urgencyScore': int(score),
                'urgencyLevel': urgency_level, 'status': 'Patient queued successfully for assignment.'
            })
        }

    except Exception as e:
        logger.error(f"Error in processTriage: {str(e)}")
        return {'statusCode': 500, 'headers': cors_headers, 'body': json.dumps({'error': 'An internal server error occurred during triage.'})}