from langgraph.prebuilt import create_react_agent

from backend.prompts import apply_prompt_template 
from backend.config.agents_map import AGENT_LLM_MAP 

from .llms import get_llm_by_type


# Create agents using configured LLM types
def create_agent(agent_name: str, agent_type: str, tools: list, prompt_template: str):
    """create an react agent based on the provided agent type, tools, and prompt template. 
    tool node execute tool calling in parallel within a single message.(version::v1) 
    implementation based langgraph `create_react_agent`.
    Args:
        agent_name (str): The name of the agent.
        agent_type (str): The type of the agent.
        tools (list): The tools the agent can use.
        prompt_template (str): The prompt template for the agent.
    Returns:
        Agent: The created agent.
    """    
    return create_react_agent(
        name=agent_name,
        model=get_llm_by_type(AGENT_LLM_MAP[agent_type]),
        tools=tools,
        prompt=lambda state: apply_prompt_template(prompt_template, state),
    )