from app.src.models.pipeline_orchestrator_model import PipelineOrchestrator
from app.src.utils.logger import get_logger
from app.src.writers.csv_writer import CSVWriter

from pyspark.sql import SparkSession

# ------------------------------------------------------------------------------
# Main Code
# ------------------------------------------------------------------------------

logger = get_logger(__name__)

def main():
    logger.info(f"Pipeline has started.")

    pipeline = PipelineOrchestrator(config_path='app/src/config/config.json')

    pipeline.run_pre_ingestion(writer=CSVWriter)

    logger.info(f"Pipeline has ended.")



if __name__ == "__main__":
    main()

