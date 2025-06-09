import json
import boto3
import os
from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
logger.info(f"Table name: {table_name}")
table = dynamodb.Table(table_name)

# Kenya MOH-based triage rules
TRIAGE_RULES = {
    'chest_pain': 10,
    'fever': 8,
    'cough': 3,
}

def calculate_urgency(score):
    logger.info(f"Calculated score: {score}")
    if score >= 10:
        return 'High', 'Doctor'
    elif score >= 5:
        return 'Medium', 'Nurse'
    else:
        return 'Low', 'Nurse'

def lambda_handler(event, context):
    try:
        logger.info(f"Event: {event}")
        body = json.loads(event.get('body', '{}'))
        logger.info(f"Body: {body}")
        symptoms = body.get('symptoms', [])
        patient_id = body.get('patient_id', '')
        hospital_id = body.get('hospital_id', '')

        if not symptoms or not patient_id or not hospital_id:
            logger.error("Missing required fields")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing symptoms, patient_id, or hospital_id'})
            }

        score = sum(Decimal(str(TRIAGE_RULES.get(symptom, 0))) for symptom in symptoms)
        urgency, resource_type = calculate_urgency(score)

        item = {
            'patient_id': patient_id,
            'hospital_id': hospital_id,
            'symptoms': symptoms,
            'score': score,
            'urgency': urgency,
            'resource_type': resource_type,
            'timestamp': context.aws_request_id
        }
        logger.info(f"Putting item: {item}")
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'urgency': urgency,
                'resourceType': resource_type
            })
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }