import json_repair 
import json 

import logging
logger = logging.getLogger(__name__)

def apply_json_repair(content: str) -> str:
    """Repair and normalize a possible broken JSON.

    Args:
        content (str): a string that may be broken JSON.

    Returns:
        str: Repaired JSON string, or the original string if it's not broken.
    """
    content = content.strip()
    if content.startswith(("{", "[")) or "```json" in content or "```ts" in content:
        try:
            # remove markdown code block
            if content.startswith("```json"):
                content = content.removeprefix("```json")
            if content.startswith("```ts"):
                content = content.removeprefix("```ts")    
            if content.endswith("```"):
                content = content.removesuffix("```")
            # get content repair with json_repair
            repaired_content = json_repair.repair(content)
            return json.dumps(repaired_content, ensure_ascii=False)
        except json.JSONDecodeError as e:
            logger.warning(f"JSONDecodeError: {e}")
        except Exception as e:
            logger.warning(f"An unexpected error occurred: {e}")
    return content