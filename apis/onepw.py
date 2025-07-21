"""
onepw.py

Provides a utility function to fetch items from 1Password (assuming it's installed).
"""

import subprocess
import json

def fetch_item_field(item_name: str, field_label: str, cli_path: str = "op") -> str:
    """
    Fetches a specific field's value from a 1Password item.

    Args:
        item_name (str): The name of the item in 1Password.
        field_label (str): The label of the field to retrieve.
        cli_path (str): Path to the 1Password CLI binary. Defaults to "op".

    Returns:
        str: The value of the specified field.

    Raises:
        RuntimeError: If the 1Password CLI command fails.
        ValueError: If the specified field is not found in the item.
    """
    try:
        result = subprocess.run(
            [cli_path, "item", "get", item_name, "--format", "json"],
            check=True,
            capture_output=True,
            text=True
        )
        item_json = json.loads(result.stdout)

        for field in item_json.get("fields", []):
            if field.get("label") == field_label:
                return field.get("value")

        raise ValueError(f"Field '{field_label}' not found in item '{item_name}'.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve item '{item_name}': {e.stderr.strip()}")

def get_openai_api_key() -> str:
    """
    Fetches the OpenAI API key from 1Password.

    Returns:
        str: The OpenAI API key string.

    Raises:
        RuntimeError: If the 1Password CLI command fails.
        ValueError: If the "credential" field is not found in the "OpenAI API Key" item.
    """
    return fetch_item_field("OpenAI API Key", "credential")