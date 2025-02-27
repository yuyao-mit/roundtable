import json
import yaml
import os


#####################################################################################################
#######################################  MACRO DEFINITION ###########################################
##################################################################################################### 


multitask_schema = {
    "name": "multitask_response",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "task1": {"type": "string"},
            "task2": {"type": "string"},
            "task3": {"type": "string"},
            "task4": {"type": "string"},
            "task5": {"type": "string"},
            "task6": {"type": "string"},
            "task7": {"type": "string"},
            "task8": {"type": "string"},
            "task9": {"type": "string"}
        },
        "required": ["task1", "task2", "task3", "task4", "task5", "task6", "task7", "task8", "task9"],
        "additionalProperties": False
    }
}

singletask_schema = {
    "name": "singletask_response",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "task1": {"type": "string"},
            "task2": {"type": "string"},
            "task3": {"type": "string"}
        },
        "required": ["task1", "task2", "task3"],
        "additionalProperties": False
    }
}


# FOR HIGHLY DETERMINISTIC ANSWERS:
config_deterministic = {
    "model": "gpt-4o-2024-08-06",
    "temperature": 0.2,
    "top_p": 0.5,
    "max_tokens": 1024,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.0,
    "stop_sequences": None
}

# FOR CREATIVE ANSWERS:
config_creative = {
    "model": "gpt-4o-2024-08-06",
    "temperature": 0.8,
    "top_p": 0.95,
    "max_tokens": 1024,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.3,
    "stop_sequences": None
}



#####################################################################################################
#######################################  UTILS DEFINITION ###########################################
##################################################################################################### 

def create_config(deterministic=True):
    """
    Selects the appropriate configuration based on `deterministic` 
    and writes it to the config.yaml file.

    Args:
        deterministic (bool): If True, uses `config_deterministic`,
                              otherwise uses `config_creative`.
    """
    config = config_deterministic if deterministic else config_creative
    config_path = os.path.abspath("config.yaml")  # Get absolute path of the file

    with open("config.yaml", "w") as file:
        yaml.dump(config, file, default_flow_style=False)

    print(f"Configuration saved to: {config_path} (deterministic={deterministic})")

def load_schema(multitask=True):
    return multitask_schema if multitask else singletask_schema

def load_config(is_generation_deterministic=True):
    create_config(deterministic=is_generation_deterministic) 
    with open("config.yaml", "r") as file:
         return yaml.safe_load(file)

