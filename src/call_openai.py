import os
import time
import json
from openai import OpenAI


def call_openai(prompt, config, response_format, retries=3, delay=2):
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
                model=config["model"],
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

