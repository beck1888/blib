import subprocess
import json

class OnePasswordFetcher:
    def __init__(self, cli_path="op"):
        self.cli_path = cli_path

    def fetch_item_field(self, item_name, field_label):
        """
        Fetches a specific field's value from a 1Password item.
        
        :param item_name: The name of the item in 1Password.
        :param field_label: The label of the field to retrieve.
        :return: The value of the specified field.
        :raises RuntimeError, ValueError: On failure or if the field is not found.
        """
        try:
            result = subprocess.run(
                [self.cli_path, "item", "get", item_name, "--format", "json"],
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

    def get_openai_api_key(self):
        """
        Fetches the OpenAI API key from 1Password.
        
        :return: The OpenAI API key string.
        """
        return self.fetch_item_field("OpenAI API Key", "credential")
