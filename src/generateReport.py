import boto3
import os
import csv
import io
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
queue_table = dynamodb.Table(os.environ['QUEUE_TABLE'])
bucket_name = os.environ['REPORTS_BUCKET']

def lambda_handler(event, context):
    try:
        logger.info("Generating daily report...")
        # 1. Fetch all records from the TriageQueue
        # In a real high-volume system, you'd query for yesterday's records only.
        # For the hackathon, scanning the whole table is fine.
        records = queue_table.scan().get('Items', [])
        
        if not records:
            logger.info("No records to report. Exiting.")
            return {'statusCode': 200, 'body': 'No records to report.'}

        # 2. Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        header = ['patientId', 'timestamp', 'urgencyLevel', 'urgencyScore', 'symptoms', 'assignedWorkerId', 'status']
        writer.writerow(header)

        # Write rows
        for record in records:
            writer.writerow([
                record.get('patientId'),
                datetime.fromtimestamp(record.get('timestamp', 0)).isoformat(),
                record.get('urgencyLevel'),
                record.get('urgencyScore'),
                ', '.join(record.get('symptoms', [])),
                record.get('assignedWorkerId'),
                record.get('status')
            ])

        # 3. Upload to S3
        csv_data = output.getvalue().encode('utf-8')
        report_date = datetime.utcnow().strftime('%Y-%m-%d')
        file_key = f'reports/{report_date}-triage-report.csv'

        s3.put_object(Bucket=bucket_name, Key=file_key, Body=csv_data)
        
        logger.info(f"Successfully uploaded report to s3://{bucket_name}/{file_key}")
        return {'statusCode': 200, 'body': 'Report generated successfully.'}

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {'statusCode': 500, 'body': json.dumps({'error': 'Failed to generate report.'})}