from pipeline.prompt_generator import PromptGenerator
from pipeline.audio_synthesizer import AudioSynthesizer
from pipeline.review_dataset import DatasetReviewer
from pipeline.export_dataset import DatasetExporter


def run_pipeline():
    PromptGenerator().run()

    AudioSynthesizer().run()

    DatasetReviewer().run()

    DatasetExporter().run()


if __name__ == "__main__":
    run_pipeline()