import os
import logging
import psutil
import sqlalchemy
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

def check_database_connection():
    """Test database connectivity"""
    try:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False

def check_memory_usage():
    """Check if memory usage is within limits"""
    try:
        memory_limit = int(os.getenv('MEMORY_LIMIT', '4096').rstrip('M'))
        current_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert to MB
        return current_memory < memory_limit
    except Exception as e:
        logger.error(f"Memory check failed: {str(e)}")
        return False

def main():
    """Main health check function"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Run checks
        db_healthy = check_database_connection()
        memory_healthy = check_memory_usage()
        
        # Evaluate overall health
        if db_healthy and memory_healthy:
            logger.info("Health check passed")
            exit(0)
        else:
            logger.error("Health check failed")
            exit(1)
            
    except Exception as e:
        logger.error(f"Critical error in health check: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
