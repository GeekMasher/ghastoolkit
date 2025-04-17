import os
import json
import responses

__HERE__ = os.path.dirname(os.path.abspath(__file__))

def loadResponses(file: str, test_name: str):
    """
    Load the responses from a file and add them to the responses library.
    """
    path = os.path.join(__HERE__, "responses", file)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {file} not found in responses directory")
    with open(path, "r") as f:
        data = json.load(f)

    resps = data.get(test_name)
    if not resps:
        raise ValueError(f"Test name '{test_name}' not found in {file}")
    
    # Array of responses
    for resp in resps:
        method = resp.get("method", "GET")
        url = resp.get("url")
        content_type = resp.get("content_type", "application/json")
        status = resp.get("status", 200)
        json_data = resp.get("json", {})

        responses.add(
            method,
            url,
            content_type=content_type,
            status=status,
            json=json_data,
        )
