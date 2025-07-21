import subprocess
import json

def fetch_item_field(item_name: str, field_label: str, cli_path: str = "op") -> str:
    """
    Fetches a specific field's value from a 1Password item.

    :param item_name: The name of the item in 1Password.
    :param field_label: The label of the field to retrieve.
    :param cli_path: Path to the 1Password CLI binary.
    :return: The value of the specified field.
    :raises RuntimeError, ValueError: On failure or if the field is not found.
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
    Convenience function to fetch the OpenAI API key from 1Password.

    :return: The OpenAI API key string.
    """
    return fetch_item_field("OpenAI API Key", "credential")