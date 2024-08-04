import json
import os

from utils.utils_funcs import load_config


def validate_hypothesis_across_experiments() -> None:
    """
    Validate the hypothesis across all processed experiments and print the overall accuracy percentage.
    """
    config = load_config()
    final_output_dir = config['paths']['final_output']
    result_output_file = config['paths']['result_output_file']

    if not os.path.isdir(final_output_dir):
        print(f"Directory {final_output_dir} does not exist.")
        return

    files = [f for f in os.listdir(final_output_dir) if f.endswith('.json')]

    if not files:
        print("No files found in final_output/ directory.")
        return

    total_experiments = len(files)
    valid_count = 0

    for file in files:
        file_path = os.path.join(final_output_dir, file)
        try:
            with open(file_path, 'r') as f:
                result = json.load(f)
                if result.get("hypothesis_valid", False):
                    valid_count += 1
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")

    # Calculate the percentage of valid experiments
    validity_percentage = (valid_count / total_experiments) * 100

    # Print the result
    print(f"Hypothesis is true for: {validity_percentage:.2f}%")

    # Write the result to an output file
    result = {
        "validity_percentage": validity_percentage
    }

    with open(result_output_file, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print(f"Result written to {result_output_file}")
