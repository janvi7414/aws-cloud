import boto3
import botocore

def lambda_handler(event, context):
    # Initialize the low-level DynamoDB client
    dynamodb = boto3.client('dynamodb')
    table_name = 'RecruiterPipelineATS'
    
    print(f"SNS Trigger received. Initializing {table_name} table setup...")
    
    try:
        # Attempt to create the table structure
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'candidateId', 'KeyType': 'HASH'} # Partition Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'candidateId', 'AttributeType': 'S'} # 'S' means String
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"Table '{table_name}' creation initiated successfully.")
        
    except botocore.exceptions.ClientError as e:
        # Handle the error gracefully if the table already exists
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{table_name}' already exists! Skipping infrastructure setup safely.")
        else:
            print(f"Unexpected error provisioning table: {e}")
            raise e
