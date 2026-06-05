# Serverless Event-Driven Data Pipeline with AWS Lambda and SQS

## Project Overview
This project demonstrates a serverless data ingestion pipeline built on AWS. Utilizing a Pub/Sub fan-out pattern, the architecture has event configurations while ensuring data persistence through managed queue buffering.

## Infrastructure Architecture
- Message Fan-Out: Amazon SNS acts as the central ingestion point, broadcasting manual message triggers to two paths.
- Execution Branch 1: An AWS Lambda function get triggered by the event notification to programmatically verify and construct an Amazon DynamoDB table.
- Execution Branch 2: Concurrently, an Amazon SQS queue applies a 2-second delivery delay to prevent race conditions during database provisioning, holding payloads safely until a secondary Lambda function processes item insertions.
- Fault Tolerance: A dedicated Dead Letter Queue (DLQ) is mapped to the main SQS pipeline to capture and isolate processing anomalies without losing source payloads.
- Identity & Access Management: Security  using a single Unified IAM Execution Role containing AmazonSQSFullAccess, AmazonDynamoDBFullAccess, and AmazonSNSReadOnlyAccess attached to two Lambda functions and SQS.

## Deployment and Testing
To test the pipeline execution workflow:
1. Publishing a standard JSON payload directly into the Amazon SNS topic endpoint.
2. Confirming asynchronous execution loops by reviewing structural tables inside DynamoDB and tracking performance entries via Amazon CloudWatch Logs.
