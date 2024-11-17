from environs import Env
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def create_api_key(project_id: str) -> Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = "My first API key"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    return response


if __name__ == "__main__":
    env = Env()
    env.read_env()
    dialog_flow_project_id = env.str("DIALOG_FLOW_PROJECT_ID")
    print("Successfully created an API key", create_api_key(dialog_flow_project_id))
