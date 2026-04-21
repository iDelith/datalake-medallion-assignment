# ------------------------------------------------------------------------------
# Pipeline Orchestrator Class
# ------------------------------------------------------------------------------
"""
This module aims to enable an Orchestrator class that will handle ETL tasks.

Usage:

```python
loader = ConfigLoader("./app/config/config.json")
config = loader.load_workflow("generate_file_workflow")
```

"""


from typing import List, Optional

from app.src.loaders.config_loader import ConfigLoader
from app.src.models.config_model import Workflow
from app.src.mappers.config_mapper import map_single_workflow, map_to_workflow
from app.src.utils.logger import get_logger

logger = get_logger(__name__)


class PipelineOrchestrator:

    def __init__(self, config_path: str):
        self.loader: ConfigLoader = self._load_configuration(config_path)
        self.workflow_objects: List[Workflow] = self._map_to_workflows()

    # --------------------------------------------------------------------------
    # Configuration
    # --------------------------------------------------------------------------

    def _load_configuration(self, config_path: str) -> ConfigLoader:
        return ConfigLoader(config_path)

    def _map_to_workflows(self) -> List[Workflow]:
        config = self.loader._load()

        # Handle BOTH single and multiple workflows
        if isinstance(config, dict):
            if "workflow_name" in config:
                # Single workflow
                return [map_single_workflow(config)]
            else:
                # Multiple workflows
                return map_to_workflow(config)

        raise ValueError("Invalid configuration format")

    # --------------------------------------------------------------------------
    # Execution
    # --------------------------------------------------------------------------

    def run_pre_ingestion(
            self,
            writer,
            workflow_names: Optional[List[str]] = None
    ) -> None:
        """
        Execute pre-ingestion workflows.

        Args:
            writer: Writer class (e.g., CSVWriter)
            workflow_names: Optional list to filter workflows
        """

        workflows = self._filter_workflows(workflow_names)

        for wf in workflows:
            if wf.stage != "pre_ingestion":
                continue

            params = wf.tasks.parameters
            log_fields = params.log_fields

            logger.info(f"Trigger: {wf.tasks.task_type}")
            logger.info(f"Parameters: {log_fields}")

            output_writer = writer(params)
            output_path = output_writer.write()

            logger.info(f"File written to: {output_path}")

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def _filter_workflows(
            self,
            workflow_names: Optional[List[str]] = None
    ) -> List[Workflow]:

        if not workflow_names:
            return self.workflow_objects

        return [
            wf for wf in self.workflow_objects
            if wf.workflow_name in workflow_names
        ]


