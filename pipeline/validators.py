from faster_whisper import WhisperModel
from jiwer import wer
import torch


class AudioValidator:
    def __init__(self, threshold=0.35):
        self.threshold = threshold
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "float16"
            print("Using CUDA")
        else:
            device = "cpu"
            compute_type = "int8"
            print("Using CPU")

        self.model = WhisperModel(
                "large-v3",
                device=device,
                compute_type=compute_type
            )   

    def transcribe(self, audio_path):
        segments, _ = self.model.transcribe(audio_path, language="ar")

        text = " ".join([segment.text for segment in segments])

        return text.strip()

    def validate(self, reference_text, audio_path):
        predicted_text = self.transcribe(audio_path)


        print("REF :", reference_text)
        print("PRED:", predicted_text)

        score = wer(reference_text, predicted_text)

        print("WER :", score)
        print("=" * 50)

        return {
            "prediction": predicted_text,
            "wer": score,
            "accepted": score <= self.threshold
        }
    
    