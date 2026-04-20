# ------------------------------------------------------------------------------
# Data Classes
# ------------------------------------------------------------------------------
"""
This module aims to apply the Object Calisthenics approach, moving away from
python primitives to abstract objects.

This should be evolved in case the configuration `.app/config/config.json` file
undergoes any updates, as the structure should follow the same pattern.

Examples:
1) workflow["tasks"]["parameters"] -> workflow.tasks.parameters

"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SchemaField:
    name: str
    type: str
    required: bool

@dataclass
class Parameters:
    log_fields: List[str]
    file_name: str
    file_type: str
    input_path: str | None
    output_path: str
    schema: List[Dict[str, Any]]
    content: List[Dict[str, Any]]

    def get_log_fields(self) -> dict:
        return {
            field: getattr(self, field)
            for field in self.log_fields
            if hasattr(self, field)
        }


@dataclass
class Task:
    task_name: str
    task_type: str
    parameters: Parameters


@dataclass
class Workflow:
    workflow_name: str
    description: str
    stage: str
    is_active: bool
    tasks: Task