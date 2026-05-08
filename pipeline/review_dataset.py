import json

from pipeline.utils import load_json, load_config
from pipeline.validators import AudioValidator


class DatasetReviewer:
    def __init__(self):
        config = load_config()

        self.threshold = config["validation"]["wer_threshold"]
        self.validator = AudioValidator(self.threshold)

    def run(self):
        prompts = load_json("data/prompts/prompts.json")

        reviewed = []

        for sample in prompts:
            audio_path = f"data/audio/{sample['id']}.wav"

            result = self.validator.validate(
                reference_text=sample["text"],
                audio_path=audio_path
            )

            reviewed.append({
                "id": sample["id"],
                "category": sample["category"],
                "text": sample["text"],
                "audio": audio_path,
                "prediction": result["prediction"],
                "wer": result["wer"],
                "accepted": result["accepted"]
            })

            print(f"Reviewed sample {sample['id']}")

        with open("data/reviewed/reviewed.json", "w", encoding="utf-8") as file:
            json.dump(reviewed, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    DatasetReviewer().run()