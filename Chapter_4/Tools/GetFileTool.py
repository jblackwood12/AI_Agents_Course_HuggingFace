from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import requests
from smolagents import Tool

# (Keep Constants as is)
# --- Constants ---
DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"


class GetFileTool(Tool):
    name = "gets_file"
    description = (
        "Downloads a file, and returns a path to that file, related to the question id."
    )
    inputs = {
        "question_id": {
            "type": "string",
            "description": "The question id to get the file from.",
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, question_id):
        return self.get_file_for_task(question_id)

    def get_file_for_task(self, question_id: str):
        file_url = f"{DEFAULT_API_URL}/files/{question_id}"

        print(f"Fetching file from task_id: {question_id}")
        try:
            response = requests.get(file_url, timeout=15)
            response.raise_for_status()
            if not response.content:
                print("Fetched file is empty.")
                return "Fetched file is empty or invalid format.", None
            print(f"Fetched {len(response.content)} files.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching questions: {e}")
            return f"Error fetching questions: {e}", None
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON response from files endpoint: {e}")
            print(f"Response text: {response.text[:500]}")
            return f"Error decoding server response for files: {e}", None
        except Exception as e:
            print(f"An unexpected error occurred fetching files: {e}")
            return f"An unexpected error occurred fetching files: {e}", None
        
        headers_val = response.headers.get('content-disposition')

        split_str = headers_val.split(question_id)
        file_extension = split_str[1].replace('"', '')
        file_name = f"{question_id}{file_extension}"
        file_path = f"/tmp/{file_name}"

        # return the path of the file that was downloaded                                                                                                                                          
        with open(file_path, "wb") as f:                                                                                                                                              
            f.write(response.content)   
        return file_path  