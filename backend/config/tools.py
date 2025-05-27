import os 
import enum 

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class SearchEngine(enum.Enum):
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"
    BRAVE_SEARCH = "brave_search"
    ARXIV = "arxiv"
    
    
# TOOL CONFIGURATION 
SELECTED_SEARCH_ENGINE = os.getenv("SEARCH_API", SearchEngine.TAVILY.value)
