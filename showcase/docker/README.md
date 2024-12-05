# Smart Adaptive Recommendations (SAR) Pipeline Showcase

This showcase demonstrates a containerized Smart Adaptive Recommendations pipeline implemented using Docker and AWS services.

## Pipeline Architecture

The pipeline is orchestrated using AWS Step Functions, with each stage running as an ECS task on AWS Fargate:

1. **Stage 1: Data Loading**
   - Initial data ingestion and validation
   - Processes raw interaction data

2. **Stage 2: Data Transformation**
   - Data preprocessing and transformation
   - Prepares data for SAR model

3. **Stage 3: SAR Model Training**
   - Smart Adaptive Recommendations model training
   - Generates personalized recommendations

4. **Stage 4: Email Processing**
   - Secure email hashing
   - Privacy-preserving operations

5. **Stage 5: Recommendation Injection**
   - Database injection of recommendations
   - Transaction management

## AWS Infrastructure

- Step Functions for workflow orchestration
- ECS/Fargate for containerized execution
- S3 for stage data storage
- CloudWatch for logging and monitoring
- IAM for security and access control

## Implementation Features

- Docker containerization
- Resource constraints for Fargate compatibility
- Proper error handling and logging
- Security best practices
- CloudWatch logging

## Running Locally

Each stage can be run independently using Docker:

```bash
cd stage1_load
docker build -t sar-stage1 .
docker run --env-file .env sar-stage1
```

## Security

- IAM roles and policies
- Secure environment variables
- Data encryption
- Access logging

## Monitoring

- CloudWatch logs
- Container metrics
- Step Functions execution tracking
- Resource utilization
