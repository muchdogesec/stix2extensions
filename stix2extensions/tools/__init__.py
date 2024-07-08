import uuid
import requests
from stix2 import parse, Identity, Relationship
import logging

def load_stix_object_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return parse(response.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error loading JSON from {url}: {e}")
        raise
