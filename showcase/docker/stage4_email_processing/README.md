# Stage 4: Email Processing for Smart Adaptive Recommendations (SAR)

This container handles secure email processing and hashing in the SAR pipeline, preparing user data for secure recommendation delivery.

## Features

- Secure email hashing
- Salt generation and management
- Privacy-preserving processing
- Batch operations
- Data security compliance

## Docker Optimizations

1. **Security**
   - Secure hash implementation
   - Salt management
   - Memory wiping
   - Secure environment

2. **Performance**
   - Batch email processing
   - Efficient hashing
   - Memory management
   - Resource cleanup

3. **Reliability**
   - Error handling
   - Hash verification
   - Process monitoring
   - Automatic recovery

## Running Locally

1. Build the image:
```bash
docker build -t sar-stage4-email .
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your values
```

3. Run the container:
```bash
docker run --env-file .env sar-stage4-email
```

## AWS Integration

- S3 for data storage
- CloudWatch for logging
- ECS/Fargate for execution
- KMS for key management

## Data Flow

1. Input: User data with emails from Stage 3
2. Processing:
   - Email validation
   - Secure hashing
   - Salt application
3. Output: Processed data with hashed emails

## Monitoring

- Hash processing rates
- Memory usage
- Error rates
- Security metrics

## Security Features

- Secure hash algorithms
- Salt management
- Memory security
- Access logging
