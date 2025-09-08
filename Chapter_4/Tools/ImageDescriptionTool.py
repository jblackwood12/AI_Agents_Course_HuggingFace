from typing import Any
from smolagents import Tool
from transformers import pipeline
from PIL import Image

# Would be used to get information about the chess position in an image.
# Not descriptive enough for getting Chess Positions
# Might be possible to use API from: https://helpman.komtera.lt/chessocr/
# What gets outputted is the "FEN" string that represents the position
# This would then require using a chess engine to analyze the position, and return the best move.
class ImageDescriptionTool(Tool):
    name = "image_describer"
    description = "Generates a textual description of an image."
    inputs = {"file_path_to_image": {"type": "string", "description": "The file path to the image that needs to be described."}}
    output_type = "string"

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def forward(self, file_path_to_image: str) -> str:
        # Implement image description logic here using a vision-language model
        # For example:
        image = Image.open(fp=file_path_to_image)
        image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        output = image_to_text(image)[0]["generated_text"]
        return output