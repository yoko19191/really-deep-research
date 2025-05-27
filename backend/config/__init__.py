from .loader import load_yaml_config 
from .tools import SELECTED_SEARCH_ENGINE, SearchEngine 
from .agents import LLMType, AGENT_LLM_MAP
from .questions import BUILT_IN_QUESTIONS, BUILT_IN_QUESTIONS_ZH_CN


from dotenv import load_dotenv, find_dotenv 
_ = load_dotenv(find_dotenv()) # read local .env file 


TEAM_MEMBER_CONFIGURATIONS = {
    "researcher": {
        "name": "researcher",
        "desc": (
            "Responsible for searching and collecting relevant information, understanding user needs and conducting research analysis"
        ),
        "desc_for_llm": (
            "Uses search engines and web crawlers to gather information from the internet. "
            "Outputs a Markdown report summarizing findings. Researcher can not do math or programming."
        ),
        "is_optional": False,
    },
    "coder": {
        "name": "coder",
        "desc": (
            "Responsible for code implementation, debugging and optimization, handling technical programming tasks"
        ),
        "desc_for_llm": (
            "Executes Python or Bash commands, performs mathematical calculations, and outputs a Markdown report. "
            "Must be used for all mathematical computations."
        ),
        "is_optional": True,
    }
}


TEAM_MEMBERS = list(TEAM_MEMBER_CONFIGURATIONS.keys()) 

__all__ = [
    # __init__.py
    "TEAM_MEMBER_CONFIGURATIONS",
    "TEAM_MEMBERS",
    # loader.py
    "load_yaml_config",
    # tools.py
    "SELECTED_SEARCH_ENGINE", 
    "SearchEngine",
    # agents.py
    "LLMType",
    "AGENT_LLM_MAP",
    # questions.py
    "BUILT_IN_QUESTIONS", 
    "BUILT_IN_QUESTIONS_ZH_CN"
] 



# print(TEAM_MEMBERS, type(TEAM_MEMBERS))
# print(TEAM_MEMBER_CONFIGURATIONS, type(TEAM_MEMBER_CONFIGURATIONS))

# a = load_yaml_config()
# print(a, type(a))

# print(SELECTED_SEARCH_ENGINE, type(SELECTED_SEARCH_ENGINE))

# print(AGENT_LLM_MAP, type(AGENT_LLM_MAP))

# print(BUILT_IN_QUESTIONS, type(BUILT_IN_QUESTIONS))
# print(BUILT_IN_QUESTIONS_ZH_CN, type(BUILT_IN_QUESTIONS_ZH_CN))