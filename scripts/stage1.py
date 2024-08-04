import json
import os

from utils.utils_funcs import load_config


def extract_relevant_data(experiment_id: str) -> None:
    """
    Extract relevant data from a raw experiment JSON file and save it to the processed directory.

    Args:
    experiment_id (str): The ID of the experiment to process.
    """
    config = load_config()
    raw_path = config['paths']['raw_experiment_data']
    processed_path = config['paths']['processed_experiment_data']

    input_path = os.path.join(raw_path, f'{experiment_id}.json')
    output_path = os.path.join(processed_path, f'{experiment_id}.json')

    # Ensure the input file exists
    if not os.path.isfile(input_path):
        print(f"Input file {input_path} does not exist.")
        return

    try:
        # Read the raw data from the JSON file
        with open(input_path, 'r') as file:
            data = json.load(file)

        # Extract relevant fields for Neuron cell types
        relevant_data = [{
            "cell_type": entry["cell_type"],
            "environment": entry["environment"],
            "cell_response": entry["cell_response"],
            "treatment": entry["treatment"]
        } for entry in data if entry["cell_type"]["name"] == "Neuron"]

        # Write the relevant data to the output JSON file
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(relevant_data, file, ensure_ascii=False, indent=4)

        print(f"Step 1 completed for {experiment_id}")

    except Exception as e:
        print(f"An error occurred while processing {experiment_id}: {e}")

