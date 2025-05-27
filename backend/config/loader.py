import os 
from typing import Any, Union
from pathlib import Path 
import yaml

_config_cache: dict[str, dict[str, Any]] = {} # Cache for configs


def replace_env_vars(value: Any) -> Any:
    """Replace environment variables in a string or list.
    Args:
        value (Any): The value to replace environment variables in.
        
    Returns:
        Any: The value with environment variables replaced.
    """
    if isinstance(value, str):
        if value.startswith('$'):
            env_var = value[1:]
            return os.getenv(env_var, value)
        # Optional: handle embedded env vars like ${VAR} or $VAR
        # return os.path.expandvars(value)
        return value
    return value



def process_value(value: Any) -> Any:
    """Recursively process a value to replace environment variables.
    Args:
        value (Any): The value to process.

    Returns:
        Any: The processed value.
    """
    if isinstance(value, dict):
        return {k: process_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [process_value(item) for item in value]
    else:
        return replace_env_vars(value)


def load_yaml_config(file_path: Union[Path, str]=None) -> dict[str, Any]:
    """Load yaml configuration from .yaml configuration file.
    Args:
        file_path (Union[Path, str]): The path to the configuration file.
    Returns:
        dict[str, Any]: The processed configuration.
    """
    if file_path is None:
        root_path = Path(__file__).parent.parent.parent.resolve() 
        file_path = root_path / 'config.yaml' # default read config.yaml from project root dir 
    else:
        file_path = Path(file_path).resolve()  # Convert to absolute path
        
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    if file_path.suffix.lower() not in (".yaml", ".yml"):
        raise ValueError(
            f"Invalid config file extension: {file_path.suffix}. "
            "Expected .yaml or .yml"
        )
        
    # Use absolute path as cache key
    cache_key = str(file_path)
    if cache_key in _config_cache:
        return _config_cache[cache_key]
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        processed_config = process_value(config) # read value from environment variable
        _config_cache[cache_key] = processed_config
        return processed_config
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to parse YAML in {file_path}: {e}")
    