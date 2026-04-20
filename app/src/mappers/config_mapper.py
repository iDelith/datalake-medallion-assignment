# ------------------------------------------------------------------------------
# Configuration Mapper
# ------------------------------------------------------------------------------
"""
This module aims to work in hand-to-hand with the model to map the configuration
file raw primitives into concrete objects. Applying this mapper will enable the
concrete implementation of the Object Calisthenics approach.

This should be evolved in case the configuration `.app/config/config.json` file
undergoes any updates, as the structure should follow the same pattern.

Examples:
1) workflow["tasks"]["parameters"] -> workflow.tasks.parameters

Usage:
workflow = map_to_workflow(config)

"""

from src.models.config_model import (
  SchemaField,
  Workflow,
  Parameters,
  Task
)

def map_to_workflow(data: dict) -> Workflow:
    task_data = data["tasks"]
    params_data = task_data["parameters"]

    schema = [SchemaField(**field) for field in params_data["schema"]]

    parameters = Parameters(
        file_name=params_data.get("file_name", []),
        file_type=params_data.get("file_type", []),
        input_path=params_data.get("input_path", []),
        output_path=params_data.get("output_path", []),
        schema=schema,
        content=params_data.get("content", []),
        log_fields=params_data.get("log_fields", [])
    )

    task = Task(
        task_name=task_data["task_name"],
        task_type=task_data["task_type"],
        parameters=parameters
    )

    return Workflow(
        workflow_name=data["workflow_name"],
        description=data["description"],
        stage=data["stage"],
        is_active=data["is_active"],
        tasks=task
    )
