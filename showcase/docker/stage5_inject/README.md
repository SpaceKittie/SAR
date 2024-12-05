# Stage 5: Recommendation Injection for Smart Adaptive Recommendations (SAR)

This container handles the final stage of injecting SAR-generated recommendations into the target database.

## Features

- Database injection of SAR recommendations
- Transaction management
- Batch processing
- Error recovery
- Data consistency checks

## Docker Optimizations

1. **Database Management**
   - Connection pooling
   - Transaction handling
   - Batch operations
   - Error recovery

2. **Performance**
   - Optimized insertions
   - Batch processing
   - Memory management
   - Resource cleanup

3. **Reliability**
   - Transaction rollback
   - Error handling
   - Process monitoring
   - Automatic recovery

## Running Locally

1. Build the image:
```bash
docker build -t sar-stage5-inject .
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your values
```

3. Run the container:
```bash
docker run --env-file .env sar-stage5-inject
```

## AWS Integration

- S3 for data retrieval
- CloudWatch for logging
- ECS/Fargate for execution
- RDS for database operations

## Data Flow

1. Input: Processed recommendations with hashed emails
2. Processing:
   - Database connection management
   - Batch injection
   - Transaction handling
3. Output: Recommendations stored in database

## Monitoring

- Injection rates
- Transaction status
- Error rates
- Database metrics

## Data Consistency

- Transaction integrity
- Data validation
- Error handling
- Rollback management
