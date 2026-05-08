import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import generate, save, set_api_key

from pipeline.utils import load_json, load_config


load_dotenv()


class AudioSynthesizer:
    def __init__(self):
        config = load_config()

        self.voice_id = config["voice"]["voice_id"]
        self.model = config["voice"]["model"]

        api_key = os.getenv("ELEVENLABS_API_KEY")
        set_api_key(api_key)


    def synthesize_sample(self, sample):
        audio_path = f"data/audio/{sample['id']}.wav"

        if Path(audio_path).exists():
            return

        audio = generate(
            text=sample["text"],
            voice=self.voice_id,
            model=self.model
        )

        save(audio, audio_path)


    def run(self):
        prompts = load_json("data/prompts/prompts.json")

        for sample in prompts:
            try:
                self.synthesize_sample(sample)
                print(f"Generated audio for sample {sample['id']}")

            except Exception as error:
                print(f"Failed sample {sample['id']}: {error}")

if __name__ == "__main__":
    AudioSynthesizer().run()                     