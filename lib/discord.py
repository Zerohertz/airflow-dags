import json

import requests


def _send_discord_message(webhook_url, content):
    data = {"content": content}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response.status_code
