from __future__ import annotations

import re


def format_str(text: str) -> str:
    """Format a string by removing HTML tags, sprite presets, and ruby tags, and replacing pronouns.

    Args:
        text: The input string to format.

    Returns:
        The formatted string.
    """
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}")
    return remove_ruby_tags(replace_pronouns(re.sub(clean, "", text).replace("\\n", "\n")))


def find_next_letter(text: str, placeholder: str) -> str:
    """Find the next letter after a placeholder in a string.

    Args:
        text: The string to search within.
        placeholder: The placeholder string to find.

    Returns:
        The character immediately following the placeholder.
    """
    index = text.find(placeholder)
    index += len(placeholder)
    return text[index]


def replace_placeholders(
    string: str, params: dict[str, list[float | int]] | list[int] | None
) -> str:
    """Replace placeholders in a string with values from parameters.

    Handle both list-based and dictionary-based parameters.
    Multiply values by 100 if the character following the placeholder is '%'.

    Args:
        string: The string containing placeholders.
        params: A dictionary or list of parameters to substitute.

    Returns:
        The string with placeholders replaced by values.
    """
    if params is None:
        return string
    if isinstance(params, list):
        for i, value in enumerate(params):
            placeholder = f"#i[{i}]"
            if placeholder in string:
                value_ = value * 100 if find_next_letter(string, placeholder) == "%" else value
                string = string.replace(placeholder, str(value_))
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
    """Replace gendered pronouns in the format {F#female}/{M#male} with a combined format.

    Example:
        "{F#She}/{M#He} is here." -> "She/He is here."

    Args:
        text: The input string containing pronouns.

    Returns:
        The string with pronouns replaced.
    """
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


def remove_ruby_tags(text: str) -> str:
    """Remove ruby tags ({RUBY_B...} and {RUBY_E#}) from a string.

    Args:
        text: The input string containing ruby tags.

    Returns:
        The string with ruby tags removed.
    """
    # Remove {RUBY_E#} tags
    text = re.sub(r"\{RUBY_E#\}", "", text)
    # Remove {RUBY_B...} tags
    return re.sub(r"\{RUBY_B[^}]*\}", "", text)
