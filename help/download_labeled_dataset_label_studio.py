import argparse
import os

import requests
from dotenv import load_dotenv


def download_labeled_data(project_id, output_file):
    """
    Download labeled data from Label Studio for a specific project.

    Args:
        project_id (int): The ID of the Label Studio project.
        output_file (str): Path where the exported data will be saved.

    Returns:
        bool: True if download was successful, False otherwise.
    """

    api_token = os.getenv("LABEL_STUDIO_API_TOKEN")
    if not api_token:
        print("Error: Label Studio API token not found. Set LABEL_STUDIO_API_TOKEN environment variable or provide via --api-token.")
        return False

    host = os.getenv("LABEL_STUDIO_HOST")
    port = os.getenv("LABEL_STUDIO_PORT")
    base_url = f"http://{host}:{port}"

    url = f"{base_url}/api/projects/{project_id}/export?exportType=JSON"
    headers = {"Authorization": f"Token {api_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Data exported successfully to {output_file}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to export data: {str(e)}")
        if hasattr(e, "response") and e.response:
            print(f"Status code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Download labeled data from Label Studio")
    parser.add_argument("--project-id", type=int, required=True, help="Label Studio project ID")
    parser.add_argument("--output-file", type=str, default="exported_data.json", help="Output file path (default: exported_data.json)")

    args = parser.parse_args()

    download_labeled_data(project_id=args.project_id, output_file=args.output_file)


if __name__ == "__main__":
    load_dotenv()
    main()
