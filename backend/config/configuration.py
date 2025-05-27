import os 

from dataclasses import dataclass, fields 
from typing import Any, Optional 

from langchain_core.runnables import RunnableConfig 

@dataclass(kw_only=True)
class Configuration:
    """Configuration for the application."""
    max_plan_iterations: int = 1 # Maximum number of planning iterations
    max_step_num: int = 3 # Maximum number of steps in a plan
    max_search_results: int = 3 # Maximum number of search results
    mcp_settings: dict = None # MCP settings, including dynamic loader tools 
    
    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration from a RunnableConfig.
        Args:
            config (Optional[RunnableConfig]): The RunnableConfig.
        Returns:
            Configuration: The created Configuration.
        """
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})
        
    
    