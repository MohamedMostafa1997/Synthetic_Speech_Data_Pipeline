import json

from pipeline.utils import load_json


class DatasetExporter:
    def run(self):
        reviewed = load_json("data/reviewed/reviewed.json")

        accepted = [sample for sample in reviewed if sample["accepted"]]

        with open("data/exports/final_dataset.jsonl", "w", encoding="utf-8") as file:
            for sample in accepted:
                row = {
                    "audio": sample["audio"],
                    "text": sample["text"]
                }

                file.write(json.dumps(row, ensure_ascii=False) + "\n")

        print(f"Exported {len(accepted)} samples")


if __name__ == "__main__":
    DatasetExporter().run()