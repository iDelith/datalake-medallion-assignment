#Imports
#import sys
#import os
#sys.path.append("/app")

from src.utils.logger import get_logger
from src.loaders.config_loader import ConfigLoader
from src.mappers.config_mapper import map_to_workflow
from src.writers.csv_writer import CSVWriter



# ------------------------------------------------------------------------------
# Main Code
# ------------------------------------------------------------------------------
logger = get_logger(__name__)




if __name__ == "__main__":

    infra_args = [
        "generate_employee_workflow",
        "generate_department_workflow",
        "generate_payroll_workflow"
     ]

    logger.info(f"Pipeline has started.")

    loader = ConfigLoader("config/config.json")

    for wkf in infra_args:
        logger.info(f"Pipeline has started: {wkf}")

        config = loader.load_workflow(wkf)
        workflow = map_to_workflow(config)


        if workflow.tasks.task_type == "file_generation":

            params = workflow.tasks.parameters
            parameter_fields = params.get_log_fields()

            logger.info(f"Trigger: {workflow.tasks.task_type}")
            logger.info(f"Parameters: {parameter_fields}")

            writer = CSVWriter(params)
            output_path = writer.write()

            logger.info(f"File written to: {output_path}")

            logger.info(f"Pipeline has ended: {workflow.workflow_name}")

    logger.info(f"Pipeline has ended.")


