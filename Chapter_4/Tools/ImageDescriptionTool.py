from typing import Any
from smolagents import Tool

# Would be used to get information about the chess position in an image.
class ImageDescriptionTool(Tool):
    name = "image_describer"
    description = "Generates a textual description of an image."
    inputs = {"image": {"type": "image", "description": "The image to describe"}}
    output_type = "string"

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def forward(self, image: Any) -> str:
        # Implement image description logic here using a vision-language model
        # For example:
        from transformers import pipeline
        image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        return image_to_text(image)[0]["generated_text"]