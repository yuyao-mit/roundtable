import os
import time
import json
import anthropic
from anthropic import Anthropic


def call_claude(prompt, config, response_format, retries=3, delay=2):
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
            json_instructions = f"Return your response as a JSON object that follows this schema: {json.dumps(response_format)}"
            full_system_prompt = f"{system_prompt}\n\n{json_instructions}"
            
            # Prepare the message request - removed the incorrect response_format parameter
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",  # Using the specified model
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