import os
import time
import json
import requests
from openai import OpenAI
import anthropic
from anthropic import Anthropic


#################################################################################################################################################

def call_openai(model, prompt, config, response_format, retries=3, delay=2):
    """
    Calls the OpenAI API with the given prompt and config settings.
    
    Args:
        prompt (str): The user prompt to send to the model.
        config (dict): Configuration dict containing model hyperparameters.
        response_format: The model response format definition (e.g. Pydantic Model).
        retries (int, optional): Number of retries in case of API failure. Defaults to 3.
        delay (int, optional): Delay (in seconds) between retries. Defaults to 2.

    Returns:
        dict or None: The JSON-parsed response if successful, otherwise None (or a fallback dict).
    """

    # Initialize the client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    for attempt in range(retries):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a structured AI assistant. Always return a valid JSON response strictly following the response_format."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                # Generation hyperparameter settings
                temperature=config["temperature"],
                top_p=config["top_p"],
                max_tokens=config["max_tokens"],
                frequency_penalty=config["frequency_penalty"],
                presence_penalty=config["presence_penalty"],
                
                # NOTE: stop might not be supported by chat completions 
                # stop=config["stop_sequences"],
                
                response_format=response_format,
            )

            # Extract content from response
            # Some versions of the API return string JSON, others return a Python dict
            content = response.choices[0].message.parsed
            parsed_content = json.loads(content) if isinstance(content, str) else content

            return parsed_content

        except Exception as e:
            print(f"Error calling OpenAI API: {e} (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)

    print("OpenAI API failed after multiple attempts. Using empty responses.")
    return {} 


#################################################################################################################################################


def call_xai(model,prompt, config, response_format, retries=3, delay=2):
    """
    Calls the OpenAI API with the given prompt and config settings.
    
    Args:
        prompt (str): The user prompt to send to the model.
        config (dict): Configuration dict containing model hyperparameters.
        response_format: The model response format definition (e.g. Pydantic Model).
        retries (int, optional): Number of retries in case of API failure. Defaults to 3.
        delay (int, optional): Delay (in seconds) between retries. Defaults to 2.

    Returns:
        dict or None: The JSON-parsed response if successful, otherwise None (or a fallback dict).
    """

    # Initialize the client
    client = OpenAI(api_key=os.environ.get("XAI_API_KEY"),base_url="https://api.x.ai/v1",)

    for attempt in range(retries):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a structured AI assistant. Always return a valid JSON response strictly following the response_format."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                # Generation hyperparameter settings
                temperature=config["temperature"],
                top_p=config["top_p"],
                max_tokens=config["max_tokens"],
                frequency_penalty=config["frequency_penalty"],
                presence_penalty=config["presence_penalty"],
                
                # NOTE: stop might not be supported by chat completions 
                # stop=config["stop_sequences"],
                
                response_format=response_format,
            )

            # Extract content from response
            # Some versions of the API return string JSON, others return a Python dict
            content = response.choices[0].message.parsed
            parsed_content = json.loads(content) if isinstance(content, str) else content

            return parsed_content

        except Exception as e:
            print(f"Error calling OpenAI API: {e} (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)

    print("OpenAI API failed after multiple attempts. Using empty responses.")
    return {} 


#################################################################################################################################################


def call_claude(model,prompt, config, response_format, retries=3, delay=2):
    """
    Calls the Anthropic API with the given prompt and config settings.
    
    Args:
        prompt (str): The user prompt to send to the model.
        config (dict): Configuration dict containing model hyperparameters.
        response_format (dict): The model response format definition (e.g. JSON schema).
        retries (int, optional): Number of retries in case of API failure. Defaults to 3.
        delay (int, optional): Delay (in seconds) between retries. Defaults to 2.

    Returns:
        dict or None: The JSON-parsed response if successful, otherwise None (or a fallback dict).
    """

    # Initialize the client
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    for attempt in range(retries):
        try:
            # Set up system prompt to ensure structured output
            system_prompt = "You are a structured AI assistant. Always return a valid JSON response strictly following the provided schema."
            
            # For JSON response, we need to specify this in the system prompt instead
            json_instructions = f"You should answer the questions as clear and concise as possible. Then return your response as a JSON object that follows this schema: {json.dumps(response_format)}"
            full_system_prompt = f"{system_prompt}\n\n{json_instructions}"
            
            # Prepare the message request - removed the incorrect response_format parameter
            response = client.messages.create(
                model=model,  # Using the specified model
                system=full_system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                # Generation hyperparameter settings
                temperature=config["temperature"],
                top_p=config["top_p"],
                max_tokens=config["max_tokens"]
                # Anthropic doesn't use response_format like OpenAI does
            )

            # Extract content from response
            content = response.content[0].text
            
            # Parse JSON response
            try:
                # Look for JSON object in the response
                import re
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                
                if json_match:
                    json_content = json_match.group(1)
                else:
                    # If no code block, try to parse the entire text
                    json_content = content
                
                parsed_content = json.loads(json_content)
                return parsed_content
            except json.JSONDecodeError:
                print(f"Error parsing JSON response: {content[:100]}...")
                # Fallback: try to extract just JSON parts from the response
                try:
                    # Look for anything that resembles JSON
                    possible_json = re.search(r'\{.*\}', content, re.DOTALL)
                    if possible_json:
                        parsed_content = json.loads(possible_json.group(0))
                        return parsed_content
                except:
                    raise
                
        except Exception as e:
            print(f"Error calling Anthropic API: {e} (Attempt {attempt + 1}/{retries})")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("Anthropic API failed after multiple attempts. Using empty responses.")
                return {}

    return {}


#################################################################################################################################################


def call_openrouter(model, prompt, config, response_format, retries=3, delay=2):
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    API_URL = "https://openrouter.ai/api/v1/chat/completions" #"https://openrouter.ai/api/v1/" #

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a structured AI assistant. Always return a valid JSON response strictly following the response_format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "provider": {"allow_fallbacks": True,
                     'require_parameters': False},
        "max_tokens": config["max_tokens"],
        "top_p": config["top_p"],
        "temperature": config["temperature"],
        "frequency_penalty": config["frequency_penalty"],
        "presence_penalty": config["presence_penalty"],
        "response_format": {
            "type": "json_schema",
            "json_schema": response_format
        },
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()

            response_data = response.json()

            # Correct extraction path from response
            content = response_data["choices"][0]["message"]["content"]

            # Remove markdown code block if present
            if content.strip().startswith("```"):
                content = content.strip().strip("`").split("\n", 1)[1]

            parsed_content = json.loads(content)

            return parsed_content

        except requests.RequestException as req_err:
            print(f"HTTP Request error: {req_err} (Attempt {attempt}/{retries})")

        except json.JSONDecodeError as json_err:
            print(f"JSON decoding error: {json_err} - Response Text: '{response.text}' (Attempt {attempt}/{retries})")

        except (KeyError, IndexError) as key_err:
            print(f"Unexpected response structure, missing key: {key_err} - Response JSON: {response_data} (Attempt {attempt}/{retries})")

        if attempt < retries:
            time.sleep(delay)

    print("OpenRouter API failed after multiple attempts. Returning empty response.")
    return {}
    
