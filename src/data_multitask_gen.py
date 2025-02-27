import json
import random
import os
import argparse

json_files = {
    "macro mechanics": "./dataset/qk_pair/macro mechanics.json",
    "micro mechanics": "./dataset/qk_pair/micro mechanics.json",
    "electrical and electronic": "./dataset/qk_pair/electrical and electronic.json",
    "optical and microscopic": "./dataset/qk_pair/optical and microscopic.json",
    "thermodynamical": "./dataset/qk_pair/thermodynamical.json",
    "semiconductor": "./dataset/qk_pair/semiconductor.json",
    "math": "./dataset/qk_pair/math.json",
    "geoscience": "./dataset/qk_pair/geoscience.json",
    "biology": "./dataset/qk_pair/biology.json"
}


data_dict = {}
for category, file_path in json_files.items():
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data_dict[category] = data

parser = argparse.ArgumentParser()
parser.add_argument("--rounds", type=int, required=True, help="Number of rounds to generate")
args = parser.parse_args()

eval_dir = "eval"
train_dir = "train"
os.makedirs(eval_dir, exist_ok=True)
os.makedirs(train_dir, exist_ok=True)

for round_num in range(1, args.rounds + 1):
    selected_questions = {}
    for category, data in data_dict.items():
        total_count = data["total"]
        random_index = random.randint(0, total_count - 1)
        selected_question = data["data"][random_index]
        selected_questions[category] = selected_question

    eval_data = {
        "round": f"{round_num:05d}",
        "task1": {
            "question": selected_questions["macro mechanics"]["question"],
            "key": selected_questions["macro mechanics"]["key"],
            "type": "macro mechanics"
        },
        "task2": {
            "question": selected_questions["micro mechanics"]["question"],
            "key": selected_questions["micro mechanics"]["key"],
            "type": "micro mechanics"
        },
        "task3": {
            "question": selected_questions["electrical and electronic"]["question"],
            "key": selected_questions["electrical and electronic"]["key"],
            "type": "electrical and electronic"
        },
        "task4": {
            "question": selected_questions["optical and microscopic"]["question"],
            "key": selected_questions["optical and microscopic"]["key"],
            "type": "optical and microscopic"
        },
        "task5": {
            "question": selected_questions["thermodynamical"]["question"],
            "key": selected_questions["thermodynamical"]["key"],
            "type": "thermodynamical"
        },
        "task6": {
            "question": selected_questions["semiconductor"]["question"],
            "key": selected_questions["semiconductor"]["key"],
            "type": "semiconductor"
        },
        "task7": {
            "question": selected_questions["math"]["question"],
            "key": selected_questions["math"]["key"],
            "type": "math"
        },
        "task8": {
            "question": selected_questions["geoscience"]["question"],
            "key": selected_questions["geoscience"]["key"],
            "type": "geoscience"
        },
        "task9": {
            "question": selected_questions["biology"]["question"],
            "key": selected_questions["biology"]["key"],
            "type": "biology"
        }
    }

    train_data = {
        "round": f"{round_num:05d}",
        "task1": {
            "question": selected_questions["macro mechanics"]["question"],
            "type": "macro mechanics"
        },
        "task2": {
            "question": selected_questions["micro mechanics"]["question"],
            "type": "micro mechanics"
        },
        "task3": {
            "question": selected_questions["electrical and electronic"]["question"],
            "type": "electrical and electronic"
        },
        "task4": {
            "question": selected_questions["optical and microscopic"]["question"],
            "type": "optical and microscopic"
        },
        "task5": {
            "question": selected_questions["thermodynamical"]["question"],
            "type": "thermodynamical"
        },
        "task6": {
            "question": selected_questions["semiconductor"]["question"],
            "type": "semiconductor"
        },
        "task7": {
            "question": selected_questions["math"]["question"],
            "type": "math"
        },
        "task8": {
            "question": selected_questions["geoscience"]["question"],
            "type": "geoscience"
        },
        "task9": {
            "question": selected_questions["biology"]["question"],
            "type": "biology"
        }
    }

    eval_file_name = f"eval_round_{round_num:05d}.json"
    eval_file_path = os.path.join(eval_dir, eval_file_name)
    with open(eval_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(eval_data, output_file, ensure_ascii=False, indent=4)

    train_file_name = f"train_round_{round_num:05d}.json"
    train_file_path = os.path.join(train_dir, train_file_name)
    with open(train_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(train_data, output_file, ensure_ascii=False, indent=4)

print(f"DATA GENERATION COMPLETE!\n{args.rounds} eval and train JSON files have been successfully sampled.")

