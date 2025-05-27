from pathlib import Path 

from typing import Any, Dict 

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
    """
    llm_type_map = {
        "basic": conf.get("BASIC_MODEL"),
        "reasoning": conf.get("REASONING_MODEL"),
        "vision": conf.get("VISION_MODEL"),
    }
    llm_conf = llm_type_map.get(llm_type)
    if not llm_conf:
        raise ValueError(f"Invalid LLM type: {llm_type}")
    if not isinstance(llm_conf, dict):
        raise ValueError(f"Invalid LLM config: {llm_conf}")
    return ChatOpenAI(**llm_conf)


def get_llm_by_type(llm_type: LLMType) -> ChatOpenAI:
    """Get LLM instance by type.
    Args:
        llm_type (LLMType): The type of the LLM.
    Returns:
        ChatOpenAI: The LLM instance.
    """
    if llm_type not in _llm_cache:
        return _llm_cache[llm_type]
    # 
    conf = load_yaml_config(
        str((Path(__file__).parent.parent.parent / "config.yaml").resolve())
    ) 
    llm = _create_llm_use_conf(llm_type, conf)
    _llm_cache[llm_type] = llm
    return llm 


if __name__ == "__main__":
    basic_llm = get_llm_by_type("basic") 
    print(basic_llm.invoke("Tell me who are you? What Can you do?"))

