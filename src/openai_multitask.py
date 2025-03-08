import os
import time
import json
from tqdm import tqdm
from pydantic import BaseModel

from openai import OpenAI
from utils.init_config import load_schema, load_config
from utils.call_llm import call_openai

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenAI Init.")
    parser.add_argument("--model", type=str, required=True,
                        help="The llm to be called")
    parser.add_argument("--player", type=str, required=True,
                        help="The player identifier")
    parser.add_argument("--retries", type=int, default=3,
                        help="Maximun retries on the question")
    parser.add_argument("--delay", type=int, default=2,
                        help="The delayed time after one retrial")
    args = parser.parse_args()

    # ------------------------------------------------------------------------------
    # Load hyperparameter configurations and the JSON schema for response validation
    # ------------------------------------------------------------------------------
    config = load_config(is_generation_deterministic=True)
    schema = load_schema(multitask=True)

    # Define player identifier
    player = args.player

    # ------------------------------------------------------------------------------
    # Data configuration
    # ------------------------------------------------------------------------------
    train_dir = "./train"
    multitask_dir = f"./{player}/multitask"
    os.makedirs(multitask_dir, exist_ok=True)

    # ------------------------------------------------------------------------------
    # Define the MultitaskResponse schema using Pydantic
    # ------------------------------------------------------------------------------
    class MultitaskResponse(BaseModel):
        task1: str
        task2: str
        task3: str
        task4: str
        task5: str
        task6: str
        task7: str
        task8: str
        task9: str

    # ------------------------------------------------------------------------------
    # Call the LLM for multitask generation
    # ------------------------------------------------------------------------------
    # Get a sorted list of training files that match "train_round_*.json"
    train_files = sorted(
        f for f in os.listdir(train_dir)
        if f.startswith("train_round_") and f.endswith(".json")
    )

    # Process each training file
    for train_file in tqdm(train_files, desc="Processing Training Files"):
        train_path = os.path.join(train_dir, train_file)

        # Read input JSON
        try:
            with open(train_path, "r", encoding="utf-8") as file:
                train_data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error: Failed to load {train_file}. Skipping...")
            continue

        round_id = train_data["round"]
        prompt = (
            "The following is a multi-task training dataset."
            "Please provide appropriate answers based on the questions:\n\n"
            f"{json.dumps(train_data, indent=2, ensure_ascii=False)}"
        )

        # Call OpenAI to get generated responses
        answers_json = call_openai(
            model=args.model,
            prompt=prompt,
            config=config,
            response_format=MultitaskResponse,
            retries=args.retries,
            delay=args.delay
        )

        answers_dict = answers_json if isinstance(answers_json, dict) else answers_json.model_dump()

        # Structure the output data
        output_data = {
            "round": round_id,
            "player": player,
            "task1": {
                "question": train_data["task1"]["question"],
                "answer": answers_dict.get("task1", "N/A"),
                "type": train_data["task1"]["type"]
            },
            "task2": {
                "question": train_data["task2"]["question"],
                "answer": answers_dict.get("task2", "N/A"),
                "type": train_data["task2"]["type"]
            },
            "task3": {
                "question": train_data["task3"]["question"],
                "answer": answers_dict.get("task3", "N/A"),
                "type": train_data["task3"]["type"]
            },
            "task4": {
                "question": train_data["task4"]["question"],
                "answer": answers_dict.get("task4", "N/A"),
                "type": train_data["task4"]["type"]
            },
            "task5": {
                "question": train_data["task5"]["question"],
                "answer": answers_dict.get("task5", "N/A"),
                "type": train_data["task5"]["type"]
            },
            "task6": {
                "question": train_data["task6"]["question"],
                "answer": answers_dict.get("task6", "N/A"),
                "type": train_data["task6"]["type"]
            },
            "task7": {
                "question": train_data["task7"]["question"],
                "answer": answers_dict.get("task7", "N/A"),
                "type": train_data["task7"]["type"]
            },
            "task8": {
                "question": train_data["task8"]["question"],
                "answer": answers_dict.get("task8", "N/A"),
                "type": train_data["task8"]["type"]
            },
            "task9": {
                "question": train_data["task9"]["question"],
                "answer": answers_dict.get("task9", "N/A"),
                "type": train_data["task9"]["type"]
            }
        }

        # Save the output JSON to the multitask directory
        output_file_name = f"{player}_round_{round_id}_multitask.json"
        output_file_path = os.path.join(multitask_dir, output_file_name)

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(output_data, output_file, ensure_ascii=False, indent=4)

    print(f"All tasks have been processed and saved at '{multitask_dir}' successfully!")
