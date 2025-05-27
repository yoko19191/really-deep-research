from typing import Any, Dict 
from pathlib import Path 

from langchain_openai import ChatOpenAI  

from backend.config import load_yaml_config 
from backend.config.agents import LLMType


# Create for LLM Instance 
_llm_cache: dict[LLMType, ChatOpenAI] = {} 


def _create_llm_use_conf(llm_type: LLMType, conf: Dict[str, Any]) -> ChatOpenAI:
    """Create LLM instance using config.
    Args:
        llm_type (LLMType): The type of the LLM.
        conf (Dict[str, Any]): The config for the LLM.
    Returns:
        ChatOpenAI: The created LLM instance.
    Raises:
        ValueError: If the LLM type is invalid or config is missing/invalid.
    """
    llm_type_map = {
        "basic": conf.get("BASIC_MODEL"),
        "reasoning": conf.get("REASONING_MODEL"),
        "vision": conf.get("VISION_MODEL"),
    }
    llm_conf = llm_type_map.get(llm_type)
    if not llm_conf:
        # Provide a more specific error if the llm_type is not found in the map
        raise ValueError(
            f"Invalid LLM type: '{llm_type}'. "
            f"Available types are: {list(llm_type_map.keys())}. "
            f"Please check your 'config.yaml' for model configurations."
        )
    if not isinstance(llm_conf, dict):
        raise ValueError(
            f"Invalid LLM config for type '{llm_type}': {llm_conf}. "
            f"Expected a dictionary. Please check your 'config.yaml'."
        )
    return ChatOpenAI(**llm_conf)


def get_llm_by_type(llm_type: LLMType) -> ChatOpenAI:
    """Get LLM instance by type.

    Retrieves an LLM instance from cache if available, otherwise creates,
    caches, and returns a new instance.

    Args:
        llm_type (LLMType): The type of the LLM.

    Returns:
        ChatOpenAI: The LLM instance.

    Raises:
        ValueError: If the LLM type is invalid or configuration is missing,
                    propagated from _create_llm_use_conf.
    """
    # Corrected logic: if in cache, return it. Otherwise, create, cache, and return.
    if llm_type in _llm_cache:
        return _llm_cache[llm_type]
    
    # Load configuration
    # Ensure the path to config.yaml is correct
    config_file_path = Path(__file__).parent.parent.parent / "config.yaml"
    conf = load_yaml_config(str(config_file_path.resolve()))
    
    try:
        llm = _create_llm_use_conf(llm_type, conf)
        _llm_cache[llm_type] = llm
        return llm
    except ValueError as e:
        # Re-raise the ValueError with additional context if needed, or let it propagate
        # For now, we let the more specific error from _create_llm_use_conf propagate
        raise ValueError(f"Can not get llm by type: {e}")

    

