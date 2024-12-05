import os
import logging
import boto3
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DataInjector:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.input_bucket = os.getenv('INPUT_BUCKET')
        self.processed_data_path = os.getenv('PROCESSED_DATA_PATH')
        self.batch_size = int(os.getenv('BATCH_SIZE', 1000))
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        
        # Database connection
        self.db_connection = create_engine(
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )

    def load_data(self):
        """Load processed data from S3"""
        try:
            logger.info(f"Loading data from s3://{self.input_bucket}/{self.processed_data_path}")
            response = self.s3_client.get_object(
                Bucket=self.input_bucket,
                Key=self.processed_data_path
            )
            df = pd.read_parquet(response['Body'])
            logger.info(f"Successfully loaded {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def inject_batch(self, df_batch):
        """Inject a batch of data into the database"""
        try:
            df_batch.to_sql(
                'processed_data',
                self.db_connection,
                if_exists='append',
                index=False,
                method='multi'
            )
            logger.info(f"Successfully injected batch of {len(df_batch)} rows")
            return True
        except Exception as e:
            logger.error(f"Error injecting batch: {str(e)}")
            return False

    def process_data(self):
        """Main processing function"""
        try:
            df = self.load_data()
            total_rows = len(df)
            successful_injections = 0

            for i in range(0, total_rows, self.batch_size):
                batch = df.iloc[i:i + self.batch_size]
                logger.info(f"Processing batch {i//self.batch_size + 1}, rows {i} to {min(i + self.batch_size, total_rows)}")
                
                # Retry logic for each batch
                for attempt in range(self.max_retries):
                    if self.inject_batch(batch):
                        successful_injections += len(batch)
                        break
                    logger.warning(f"Retry {attempt + 1} for batch starting at index {i}")

            success_rate = (successful_injections / total_rows) * 100
            logger.info(f"Injection complete. Success rate: {success_rate:.2f}% ({successful_injections}/{total_rows} rows)")
            return successful_injections == total_rows

        except Exception as e:
            logger.error(f"Error in process_data: {str(e)}")
            return False

def main():
    try:
        logger.info("Starting data injection process")
        injector = DataInjector()
        success = injector.process_data()
        
        if success:
            logger.info("Data injection completed successfully")
            exit(0)
        else:
            logger.error("Data injection failed")
            exit(1)
    
    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
