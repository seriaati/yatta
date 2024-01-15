import re
from typing import Dict, List, Optional, Union


def format_str(text: str) -> str:
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}")
    return replace_pronouns(re.sub(clean, "", text).replace("\\n", "\n"))


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


def replace_pronouns(text: str) -> str:
    female_pronoun_pattern = r"\{F#(.*?)\}"
    male_pronoun_pattern = r"\{M#(.*?)\}"

    female_pronoun_match = re.search(female_pronoun_pattern, text)
    male_pronoun_match = re.search(male_pronoun_pattern, text)

    if female_pronoun_match and male_pronoun_match:
        female_pronoun = female_pronoun_match.group(1)
        male_pronoun = male_pronoun_match.group(1)
        replacement = f"{female_pronoun}/{male_pronoun}"

        text = re.sub(female_pronoun_pattern, replacement, text)
        text = re.sub(male_pronoun_pattern, "", text)
        text = text.replace("#", "")

    return text
