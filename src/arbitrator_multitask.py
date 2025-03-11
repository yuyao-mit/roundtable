
import os
import time
import json
from tqdm import tqdm
from openai import OpenAI
from pydantic import BaseModel
from utils.init_config import load_config
import argparse

# Load your config
config = load_config(is_generation_deterministic=True)

from pydantic import BaseModel

class Player(BaseModel):
    confidence_weight: float
    uncertainty: float

class TaskConfidence(BaseModel):
    player_00001: Player
    player_00002: Player
    player_00003: Player
    player_00004: Player
    player_00005: Player
    player_00006: Player
    player_00007: Player
    player_00008: Player
    player_00009: Player

class MultitaskResponse(BaseModel):
    task1: TaskConfidence
    task2: TaskConfidence
    task3: TaskConfidence
    task4: TaskConfidence
    task5: TaskConfidence
    task6: TaskConfidence
    task7: TaskConfidence
    task8: TaskConfidence
    task9: TaskConfidence



def call_openai(model, system_prompt, user_prompt, config, retries=3, delay=2):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    for attempt in range(retries):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=config["temperature"],
                top_p=config["top_p"],
                frequency_penalty=config["frequency_penalty"],
                presence_penalty=config["presence_penalty"],
                response_format=MultitaskResponse,
            )
            content = response.choices[0].message.parsed
            parsed_content = json.loads(content) if isinstance(content, str) else content
            return parsed_content
        except Exception as e:
            print(f"Error calling OpenAI API: {e} (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
    print("OpenAI API failed after multiple attempts. Returning empty dict.")
    return {}



# 3) Use it in your loop
def main(model,player):
    # player = "arbitrator_00001"
    # model = "gpt-4.5-preview-2025-02-27"
    system_prompt_text = open("system_prompt.txt", "r", encoding="utf-8").read()

    multitask_dir = "./multitask/train"
    output_dir = "./multitask/eval"
    os.makedirs(output_dir, exist_ok=True)

    # Gather relevant files
    train_files = sorted(
        f for f in os.listdir(multitask_dir)
        if f.startswith("multitask_round_") and f.endswith(".json")
    )

    for train_file in tqdm(train_files, desc="Evaluating Multitask Responses"):
        train_path = os.path.join(multitask_dir, train_file)
        try:
            with open(train_path, "r", encoding="utf-8") as file:
                train_data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error: Failed to load {train_file}. Skipping...")
            continue

        round_id = train_data["round"]

        user_prompt_txt = (
            "Assess players' performances in the following multitask round, and for each task, "
            "give confidence weights and uncertainties for each player (player_00001 to player_00009).\n"
            f"{json.dumps(train_data, indent=2, ensure_ascii=False)}"
        )

        # Call the API
        answers_json = call_openai(model, system_prompt_text, user_prompt_txt, config)

        answers_dict = answers_json if isinstance(answers_json, dict) else answers_json.model_dump()

        # Build final output
        output_data = {
            "round": round_id,
            "arbitrator": player,
        }
    
        for i in range(1, 10):
            task_key = f"task{i}"
            if task_key not in answers_dict:
                print(f"Warning: {task_key} missing in response for {train_file}.")
                continue

            task_responses = answers_dict[task_key]
            task_output = {}
            for player_num in range(1,10):
                player_key = f"player_{player_num:05d}"
                player_response = task_responses.get(player_key,{})
                confidence_weight = player_response.get("confidence_weight","")
                uncertainty = player_response.get("uncertainty","")

                task_output[player_key] = {
                    "confidence_weight":confidence_weight,
                    "uncertainty":uncertainty
                }
            output_data[task_key] = task_output


        # Save output
        output_file_name = f"eval_{player}_round_{round_id}.json"
        output_file_path = os.path.join(output_dir, output_file_name)
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(output_data, output_file, ensure_ascii=False, indent=4)

    print(f"All tasks processed! Outputs saved in '{output_dir}'.")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Eval Multitask.")
    parser.add_argument("--model", type=str, required=True,
                        help="The llm to be called")
    parser.add_argument("--player", type=str, required=True,
                        help="The player identifier")
    #parser.add_argument("--retries", type=int, default=3,help="Maximun retries on the question")
    #parser.add_argument("--delay", type=int, default=2,help="The delayed time after one retrial")
    args = parser.parse_args()

    main(model=args.model,player=args.player)