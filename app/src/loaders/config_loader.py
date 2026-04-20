# ------------------------------------------------------------------------------
# Config Loader
# ------------------------------------------------------------------------------
"""
This module aims to enable the user to load a JSON configuration file, that
contains multiple information on a `workflow` granularity.

Usage:

```python
loader = ConfigLoader("./app/config/config.json")
config = loader.load_workflow("generate_file_workflow")
```

"""

import os
import json
from typing import List, Dict, Any
from mappers.config_mapper import map_to_workflow



class ConfigLoader:
    def __init__(self, config_path: str):
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        self.config_path = config_path
        self._config = self._load()

    def _load(self) -> Dict:
        with open(self.config_path, "r", encoding="utf-8") as file:
            return json.load(file)


    def load_workflow(self, workflow_name: str, as_object: bool = False):
        try:
          data = self._config[workflow_name]
        except KeyError:
            raise KeyError(f"Workflow '{workflow_name}' not found in config")

        if as_object:
            return map_to_workflow(data)

        return data




    def load_parameters(self, workflow_name: str) -> Dict:
        workflow = self.load_workflow(workflow_name)

        try:
            return workflow["tasks"]["parameters"]
        except KeyError as e:
            raise KeyError(f"Invalid workflow structure: missing {e}")

    def list_workflows(self) -> list:
        return list(self._config.keys())

    def load_workflows(self) -> list:
        return list(self._config.keys())
