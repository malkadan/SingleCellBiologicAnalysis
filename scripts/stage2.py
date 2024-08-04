import json
import os

from utils.utils_funcs import load_config


def validate_hypothesis_per_experiment(experiment_id: str) -> None:
    """
    Validate the hypothesis for an individual experiment based on the processed data.

    Args:
    experiment_id (str): The ID of the experiment to process.
    """
    config = load_config()
    processed_path = config['paths']['processed_experiment_data']
    final_output_path = config['paths']['final_output']

    input_path = os.path.join(processed_path, f'{experiment_id}.json')
    output_path = os.path.join(final_output_path, f'{experiment_id}.json')

    # Ensure the input file exists
    if not os.path.isfile(input_path):
        print(f"Input file {input_path} does not exist.")
        return

    try:
        # Read the processed data from the JSON file
        with open(input_path, 'r') as file:
            data = json.load(file)

        # Extract cell responses based on environment
        in_vivo_responses = [entry["cell_response"] for entry in data if entry["environment"]["name"] == "In vivo"]
        other_responses = [entry["cell_response"] for entry in data if entry["environment"]["name"] != "In vivo"]

        # Calculate average responses
        average_in_vivo = sum(in_vivo_responses) / len(in_vivo_responses) if in_vivo_responses else 0
        average_other = sum(other_responses) / len(other_responses) if other_responses else 0

        # Determine if the hypothesis is valid for this experiment
        hypothesis_valid = average_in_vivo > average_other

        # Write the result to the output JSON file
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump({"hypothesis_valid": hypothesis_valid}, file, ensure_ascii=False, indent=4)

        print(f"Step 2 completed for {experiment_id}")

    except Exception as e:
        print(f"An error occurred while processing {experiment_id}: {e}")
