import random

from pipeline.utils import load_config, save_json


FOOD = [
    "انا جعان",
    "عايز اطلب بيتزا",
    "هاتلي ساندوتش شاورما",
    "نفسي اكل كشري",
    "ممكن اطلب عصير"
]

TRANSPORT = [
    "المترو زحمة النهاردة",
    "عايز اروح المعادي",
    "فين اقرب محطة",
    "التاكسي غالي شوية",
    "المواصلات متأخرة"
]

SHOPPING = [
    "بكام التيشيرت ده",
    "عايز اشتري جزمة",
    "فيه خصومات النهاردة",
    "المحل ده غالي",
    "محتاج شنطة جديدة"
]

MEDICAL = [
    "عايز احجز عند دكتور",
    "بطني وجعاني",
    "عندي صداع جامد",
    "محتاج دوا للكحة",
    "الدكتور موجود النهاردة"
]

DAILY = [
    "عامل ايه النهاردة",
    "الجو حر جدا",
    "هتروح الشغل امتى",
    "انا تعبان شوية",
    "لسه صاحي من النوم"
]


CATEGORIES = {
    "food": FOOD,
    "transport": TRANSPORT,
    "shopping": SHOPPING,
    "medical": MEDICAL,
    "daily": DAILY
}


class PromptGenerator:

    def __init__(self):

        config = load_config()

        self.num_prompts = config["num_prompts"]

    def run(self):

        all_prompts = []

        sample_id = 1

        while len(all_prompts) < self.num_prompts:

            category = random.choice(
                list(CATEGORIES.keys())
            )

            text = random.choice(
                CATEGORIES[category]
            )

            sample = {
                "id": sample_id,
                "category": category,
                "text": text
            }

            all_prompts.append(sample)

            sample_id += 1

        save_json(
            all_prompts,
            "data/prompts/prompts.json"
        )

        print(
            f"Generated {len(all_prompts)} prompts"
        )


if __name__ == "__main__":

    PromptGenerator().run()