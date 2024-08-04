import yaml


def load_config() -> dict:
    """Load configuration from config.yaml"""
    with open('utils\config.yml', 'r') as file:
        return yaml.safe_load(file)
