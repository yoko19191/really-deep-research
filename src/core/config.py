import configparser
from envyaml import EnvYAML
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
import logging
from typing import Dict, Any, Optional

def load_config(yaml_name: str = "config.yaml", default_config: Dict[str, Any] = None) -> Dict[str, Any]:
    """find .yaml file from project root to bottom

    Args:
        yaml_name (str): .yaml config you looking for. default: config.yaml
        default_config (Dict[str, Any]): default config. return config if some configuration missing in loaded .yaml. 

    Returns:
        Dict[str, Any]: prefer return configuration in .yaml. return default_config if any configuration missing in loaded.yaml.

    Raises:
        FileNotFoundError: if .yaml file not found.
        Exception: if any error occur during loading.
    """
    if default_config is None:
        default_config = {}
    
    # Get CWD 
    current_dir = Path(__file__).resolve().parent
    
    # GET yaml bottom down
    config_path = None
    search_dir = current_dir
    while search_dir.parent != search_dir:  # reach root
        test_path = search_dir / yaml_name
        if test_path.exists():
            config_path = test_path
            break
        search_dir = search_dir.parent
    
    if not config_path:
        raise FileNotFoundError(f"Could not find {yaml_name} in any parent directory")
    
    # Loading .env file
    if load_dotenv(find_dotenv()):
        logging.info("Loaded .env file")
    else:
        logging.warning("No .env file found")
    
    try:
        # load .yaml file
        yaml_config = EnvYAML(str(config_path), include_environment=True, strict=True)
        config_dict = dict(yaml_config)
        
        # validate config check if anything missing in loaded.yaml
        for key, value in default_config.items():
            if key not in config_dict:
                logging.error(f"Configuration key '{key}' missing in {yaml_name}, using default value")
                config_dict[key] = value
            elif isinstance(value, dict) and isinstance(config_dict[key], dict):
                # recursive check nested config item
                for sub_key, sub_value in value.items():
                    if sub_key not in config_dict[key]:
                        logging.error(f"Configuration key '{key}.{sub_key}' missing in {yaml_name}, using default value")
                        config_dict[key][sub_key] = sub_value
        
        return config_dict
        
    except Exception as e:
        logging.error(f"Error loading {yaml_name}: {e}")
        raise

