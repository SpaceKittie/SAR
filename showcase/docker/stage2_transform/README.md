# Stage 2: Data Transformation for Smart Adaptive Recommendations (SAR)

This container handles the data transformation phase of the SAR pipeline, preparing interaction data for the Smart Adaptive Recommendations model.

## Features

- User interaction data transformation
- Feature preparation for SAR
- Time-based aggregations
- Memory-efficient processing
- Data quality checks

## Docker Optimizations

1. **Resource Management**
   - Memory optimization
   - Batch processing
   - Resource monitoring
   - Efficient cleanup

2. **Performance**
   - Parallel processing
   - Efficient aggregations
   - Memory-efficient operations
   - Optimized transformations

3. **Reliability**
   - Error handling
   - Data validation
   - Process monitoring
   - Automatic recovery

## Running Locally

1. Build the image:
```bash
docker build -t sar-stage2-transform .
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your values
```

3. Run the container:
```bash
docker run --env-file .env sar-stage2-transform
```

## AWS Integration

- S3 for data storage
- CloudWatch for logging
- ECS/Fargate for execution

## Data Flow

1. Input: Validated raw data from Stage 1
2. Processing:
   - User interaction processing
   - Time-based feature creation
   - Data aggregation
3. Output: Transformed data ready for SAR model

## Monitoring

- Transformation metrics
- Memory usage
- Error rates
- Processing speed

## Data Quality

- Feature validation
- Aggregation checks
- Data completeness
- Error logging
