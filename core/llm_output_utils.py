# core/llm_output_utils.py
import re

def clean_markdown_code(text: str) -> str:
    return re.sub(r"^```(?:java)?\n|```$", "", text.strip())