import os 
from typing import Any
import yaml


def replace_env_vars(value: str) -> str:
    """Replace environment variables in a string.
    Args:
        value (str): The string to replace environment variables in.
        
    Returns:
        str: The string with environment variables replaced.
    """
    if not isinstance(value, str):
        return value
    if value.startswith('$'):
        env_var = value[1:]
        return os.getenv(env_var, value)
    return value


def process_dict(config: dict[str, Any]) -> dict[str, Any]:
    """Recursively process a dictionary to replace environment variables.
    Args:
        config (dict[str, Any]): The dictionary to process.

    Returns:
        dict[str, Any]: The processed dictionary.
    """
    results = {}
    for key, value in config.items():
        if isinstance(value, dict):
            results[key] = process_dict(value)
        elif isinstance(value, list):
            results[key] = replace_env_vars(value)
        else:
            results[key] = value
            
    return results



_config_cache: dict[str, dict[str, Any]] = {}


def load_yaml_config(file_path: str) -> dict[str, Any]:
    """Load and process YAML configuration from .yaml configuration file. 
    Args:
        file_path (str): The path to the configuration file.
    Returns:
        dict[str, Any]: The processed configuration.
    """ 
    # Check if file_path is exists 
    if not os.path.exists(file_path):
        raise ValueError(f"Config file do not exists: {file_path}")
    
    # Check if file_path is yaml field 
    if not file_path.endswith('.yaml'):
        raise ValueError(f"Invalid config file path: {file_path} only .yaml files are allowed")
    
    # Check if file_path is in cache
    if file_path in _config_cache:
        return _config_cache[file_path]
    
    # load yaml file 
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f) 
    
    processed_config = process_dict(config)
    
    # load configuration into cache dict 
    _config_cache[file_path] = processed_config
    return processed_config
    
    
    
    
    