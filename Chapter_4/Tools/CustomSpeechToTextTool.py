from smolagents import Tool
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

class CustomSpeechToTextTool(Tool):
    """ Implemented from here: https://huggingface.co/openai/whisper-large-v3-turbo """
    default_checkpoint = "openai/whisper-large-v3-turbo"
    description = "This is a tool that transcribes an audio into text. It returns the transcribed text."
    name = "transcriber"
    inputs = {
        "audio": {
            "type": "audio",
            "description": "The audio to transcribe. Can be a local path, an url, or a tensor.",
        }
    }
    output_type = "string"

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def forward(self, audio):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"        
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model_id = "openai/whisper-large-v3-turbo"

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(model_id)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
            return_timestamps=True
        )

        pipe_results = pipe(audio)
        formatted_text = f"<transcribed_text>{pipe_results['text']}</transcribed_text> Refer to the question_text section to ensure the correct data is retrieved from this transcribed_text. Ensure that you read context carefully."

        return formatted_text