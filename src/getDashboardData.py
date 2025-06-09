import json
import boto3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')
queue_table = dynamodb.Table(os.environ['QUEUE_TABLE'])
schedule_table = dynamodb.Table(os.environ['SCHEDULE_TABLE'])

def lambda_handler(event, context):
    try:
        # 1. Get all patient data from the queue
        patients = queue_table.scan().get('Items', [])
        
        # 2. Get all worker data
        workers = schedule_table.scan().get('Items', [])

        # 3. Aggregate data for the dashboard
        dashboard_data = {
            'patient_queue_summary': {
                'total': len(patients),
                'pending_assignment': sum(1 for p in patients if p['status'] == 'PENDING_ASSIGNMENT'),
                'assigned': sum(1 for p in patients if p['status'] == 'ASSIGNED'),
                'high_urgency': sum(1 for p in patients if p['urgencyLevel'] == 'High'),
                'medium_urgency': sum(1 for p in patients if p['urgencyLevel'] == 'Medium'),
            },
            'staff_heatmap': [
                {
                    'workerId': w['workerId'],
                    'name': w['workerName'],
                    'role': w['role'],
                    'status': w['status'],
                    'load': f"{int(w['currentLoad'])}/{int(w['maxLoad'])}"
                } for w in workers
            ],
            'live_patient_queue': patients # Full list for detailed view
        }
        
        logger.info("Successfully fetched dashboard data.")
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps(dashboard_data, default=int) # Use default=int to handle Decimal types
        }

    except Exception as e:
        logger.error(f"Error fetching dashboard data: {e}")
        return {'statusCode': 500, 'body': json.dumps({'error': 'Could not fetch dashboard data.'})}