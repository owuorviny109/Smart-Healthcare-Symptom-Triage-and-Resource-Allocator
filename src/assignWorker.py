# src/assignWorker.py

import boto3
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
queue_table = dynamodb.Table(os.environ['QUEUE_TABLE'])
schedule_table = dynamodb.Table(os.environ['SCHEDULE_TABLE'])

def lambda_handler(event, context):
    logger.info("Starting worker assignment process...")
    try:
        # --- Step 1: Find all patients who are waiting for a worker ---
        response = queue_table.scan(
            FilterExpression='#s = :status',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':status': 'PENDING_ASSIGNMENT'}
        )
        # Sort by timestamp to ensure we process the earliest patients first (FIFO)
        waiting_patients = sorted(response.get('Items', []), key=lambda x: x.get('timestamp', 0))

        if not waiting_patients:
            logger.info("No patients are currently waiting for assignment. Exiting.")
            return {'statusCode': 200, 'body': json.dumps('No patients waiting for assignment.')}
        
        logger.info(f"Found {len(waiting_patients)} patients waiting.")

        # --- Step 2: Get all available staff members ---
        workers_response = schedule_table.scan(
            FilterExpression='#s = :status',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':status': 'AVAILABLE'}
        )
        all_available_workers = workers_response.get('Items', [])
        
        # Filter workers who have capacity
        available_doctors = [
            w for w in all_available_workers 
            if w['role'] == 'Doctor' and int(w['currentLoad']) < int(w['maxLoad'])
        ]
        available_nurses = [
            w for w in all_available_workers 
            if w['role'] == 'Nurse' and int(w['currentLoad']) < int(w['maxLoad'])
        ]
        
        logger.info(f"Found {len(available_doctors)} available doctors and {len(available_nurses)} available nurses with capacity.")

        # --- Step 3: Match patients to staff (The Core Logic) ---
        assignments_made = 0
        for patient in waiting_patients:
            target_worker = None
            
            # Rule: High urgency cases go to the least busy doctor
            if patient['urgencyLevel'] == 'High' and available_doctors:
                target_worker = min(available_doctors, key=lambda x: int(x['currentLoad']))
            
            # Rule: Medium urgency cases go to the least busy nurse
            elif patient['urgencyLevel'] == 'Medium' and available_nurses:
                target_worker = min(available_nurses, key=lambda x: int(x['currentLoad']))

            # If a suitable worker was found, perform the assignment
            if target_worker:
                worker_id = target_worker['workerId']
                patient_id = patient['patientId']
                
                logger.info(f"Assigning Patient '{patient_id}' (Urgency: {patient['urgencyLevel']}) to {target_worker['role']} '{worker_id}'")

                # Update the patient's record to show they've been assigned
                queue_table.update_item(
                    Key={'patientId': patient_id},
                    UpdateExpression='SET #s = :new_status, assignedWorkerId = :worker_id',
                    ExpressionAttributeNames={'#s': 'status'},
                    ExpressionAttributeValues={':new_status': 'ASSIGNED', ':worker_id': worker_id}
                )

                # Update the worker's schedule to increment their load
                schedule_table.update_item(
                    Key={'workerId': worker_id},
                    UpdateExpression='SET currentLoad = currentLoad + :inc',
                    ExpressionAttributeValues={':inc': 1}
                )
                
                # IMPORTANT: Remove the assigned worker from the pool for this run
                # This prevents assigning the same worker multiple patients in one go
                if target_worker in available_doctors:
                    available_doctors.remove(target_worker)
                if target_worker in available_nurses:
                    available_nurses.remove(target_worker)

                assignments_made += 1

        logger.info(f"Assignment process complete. Made {assignments_made} new assignments.")
        return {'statusCode': 200, 'body': json.dumps(f'Assignment process complete. Made {assignments_made} new assignments.')}

    except Exception as e:
        logger.error(f"An error occurred during worker assignment: {str(e)}")
        # In a real-world scenario, you might send an alert here
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}