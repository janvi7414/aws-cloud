import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('RecruiterPipelineATS')
    
    candidates_to_insert = []
    
    # 1. Check if the trigger contains live data from an SQS queue array
    if 'Records' in event and len(event['Records']) > 0:
        print("Processing live data flow from SQS batch trigger...")
        
        record = event['Records'][0]
        sqs_body = json.loads(record['body'])
        
        # FIX: If the message came through SNS, the actual data is wrapped inside a 'Message' string
        if 'Message' in sqs_body:
            print("Unwrapping SNS-over-SQS message layer...")
            inner_data = json.loads(sqs_body['Message'])
        else:
            inner_data = sqs_body
        
        candidates_to_insert.append({
            'candidateId': inner_data.get('candidateId', 'cand_fallback'),
            'candidateName': inner_data.get('candidateName', 'Unknown Applicant'),
            'roleApplied': inner_data.get('roleApplied', 'General Software Engineer'),
            'interviewStage': inner_data.get('interviewStage', 'Screening')
        })
        
    # 2. Fallback: Seed multiple mockup entries if manually run inside the AWS console test tab
    else:
        print("Processing manual console test event. Seeding multiple mock candidate values...")
        candidates_to_insert = [
            { 'candidateId': 'cand_01', 'candidateName': 'Janvi Chichudde', 'roleApplied': 'Cloud Engineer', 'interviewStage': 'Technical Round' },
            { 'candidateId': 'cand_02', 'candidateName': 'Shreya Patil', 'roleApplied': 'Full Stack Developer', 'interviewStage': 'Managerial Interview' },
            { 'candidateId': 'cand_03', 'candidateName': 'Aditya Rao', 'roleApplied': 'DevOps Architect', 'interviewStage': 'Offer Letter Sent' }
        ]
        
    try:
        with table.batch_writer() as batch:
            for candidate in candidates_to_insert:
                batch.put_item(Item=candidate)
                
        print(f"Data flow success! Multi-value batch insertion completed for {len(candidates_to_insert)} candidates.")
        
    except Exception as e:
        print(f"Error executing database batch operation: {e}")
        raise e
