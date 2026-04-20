# ------------------------------------------------------------------------------
# CSV Writer
# ------------------------------------------------------------------------------
"""
This module aims to create a concrete implementation of a Writer interface,
enabling the user to transform the parameters passed by the configuration into
a concrete CSV file.

Usage:
```python
writer = CSVWriter(params)
output_path = writer.write()
```

Disclaimer: the arguments passed into the class should be a Parameter object,
not a raw primitive type.

"""
import csv
import os

from src.models.config_model import Parameters

class CSVWriter:
    def __init__(self, parameters: Parameters):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

        self.file_name = parameters.file_name
        self.output_path = os.path.join(PROJECT_ROOT, parameters.output_path)
        self.schema = parameters.schema
        self.content = parameters.content
        self.columns = [field.name for field in self.schema]

    def _validate(self):
        for row in self.content:
            for field in self.schema:
                name = field.name

                if field.required and name not in row:
                    raise ValueError(f"Missing required field: {name}")

    def write(self):
        self._validate()

        os.makedirs(self.output_path, exist_ok=True)

        file_path = os.path.join(self.output_path, f"{self.file_name}.csv")

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.columns)

            writer.writeheader()
            writer.writerows(self.content)

        return file_path