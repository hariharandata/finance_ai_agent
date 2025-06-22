import re
from pathlib import Path
from typing import Dict
from .logger import get_logger

logger = get_logger("prompt_loader")

def load_markdown_sections(filepath: str) -> Dict[str, str]:
    """
    Parses a markdown file and extracts sections by headers.

    Returns a dictionary where keys are lowercase section headers
    and values are the content under those headers.
    """
    logger.info("Loading markdown sections from %s", filepath)
    try:
        content = Path(filepath).read_text(encoding="utf-8")

        # Regex to split content by markdown headers (e.g., "# Header")
        matches = re.split(r'(?m)^# (.+)', content)

        sections = {}
        for i in range(1, len(matches), 2):
            header = matches[i].strip().lower().replace(" ", "_")
            body = matches[i + 1].strip()
            sections[header] = body

        return sections
    except Exception as e:
        logger.error("Error loading markdown sections from %s: %s", filepath, e)
        raise

prompts = load_markdown_sections(str(Path(__file__).parent.parent / "prompts" / "instructions.md"))    
print(prompts["instructions"])  # list of instructions
print(prompts["query"])                     # main prompt