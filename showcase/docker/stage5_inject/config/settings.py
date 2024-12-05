import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_CONFIG = {
    'region': os.getenv('AWS_REGION', 'us-east-1'),
    'input_bucket': os.getenv('INPUT_BUCKET'),
    'processed_data_path': os.getenv('PROCESSED_DATA_PATH'),
}

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}

# Application Configuration
APP_CONFIG = {
    'batch_size': int(os.getenv('BATCH_SIZE', 1000)),
    'max_retries': int(os.getenv('MAX_RETRIES', 3)),
    'transaction_timeout': int(os.getenv('TRANSACTION_TIMEOUT', 300)),
    'memory_limit': os.getenv('MEMORY_LIMIT', '4096M'),
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
}

# Monitoring Configuration
MONITORING_CONFIG = {
    'enable_metrics': True,
    'metrics_namespace': 'SAR/Stage5',
    'health_check_interval': 30,
}
