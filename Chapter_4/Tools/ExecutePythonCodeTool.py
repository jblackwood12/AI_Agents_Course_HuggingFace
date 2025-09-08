from typing import Any
from smolagents import Tool
import subprocess

# Takes the path of the Python file, and executes the code, and returns the output.
class ExecutePythonCodeTool(Tool):
    name = "execute_python_code"
    description = "Takes a path of a Python file, executes the code, and returns the output."
    inputs = {"python_code_file_path": {"type": "string", "description": "The path of the Python file to execute."}}
    output_type = "string"

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def forward(self, python_code_file_path: str) -> str:
        result = subprocess.run(
            ["python", python_code_file_path],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout