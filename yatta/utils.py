import re
from typing import Dict, List, Optional, Union


def remove_html_tags(text: str) -> str:
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}")
    return re.sub(clean, "", text).replace("\\n", "\n")


def find_next_letter(text: str, placeholder: str) -> str:
    """Find the next letter after a placeholder in a string"""
    index = text.find(placeholder)
    index += len(placeholder)
    return text[index]


def replace_placeholders(
    string: str, params: Optional[Union[Dict[str, List[Union[float, int]]], List[int]]]
):
    if params is None:
        return string
    if isinstance(params, list):
        for i, value in enumerate(params):
            placeholder = f"#i[{i}]"
            if placeholder in string:
                if find_next_letter(string, placeholder) == "%":
                    value *= 100
                string = string.replace(placeholder, str(value))
        return string
    for key, values in params.items():
        value = values[0]
        placeholder = f"#{key}[i]"
        if placeholder in string:
            if find_next_letter(string, placeholder) == "%":
                value *= 100
            string = string.replace(placeholder, str(value))
    return string
