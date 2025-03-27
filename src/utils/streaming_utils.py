import json

def process_streaming_response(response):
    """
    Process a streaming HTTP response and yield parsed JSON content.
    """
    buffer = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            buffer += line
            try:
                json_data = json.loads(buffer)
                buffer = ""  # Clear the buffer after successful parsing
                if "message" in json_data and "content" in json_data["message"]:
                    yield json_data["message"]["content"]
            except json.JSONDecodeError:
                # Wait for more data to complete the JSON
                continue