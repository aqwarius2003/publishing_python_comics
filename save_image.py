import os
from urllib.parse import urlparse, unquote
import requests


def get_extension_file(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    unquoted_path = unquote(path)
    filename = os.path.basename(unquoted_path)
    extension_file = os.path.splitext(filename)[1]
    return extension_file


def save_image(url, save_path, payload=None):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)