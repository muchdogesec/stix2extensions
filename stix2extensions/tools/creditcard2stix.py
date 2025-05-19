from functools import lru_cache
import logging
import uuid
import requests
from stix2 import Relationship, Identity

from ..bank_card import BankCard

IDENTITY_NS = uuid.UUID("d287a5a4-facc-5254-9563-9e92e3e729ac")
OASIS_NS    = uuid.UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

@lru_cache(maxsize=4096)
def get_bin_data(card_number, api_key):
    try:
        bin_number = card_number[:6]
        url = f"https://bin-ip-checker.p.rapidapi.com/?bin={bin_number}"
        headers = {
            'Content-Type': 'application/json',
            'x-rapidapi-host': 'bin-ip-checker.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        logging.debug(f"Requesting BIN data for card number: {card_number}")
        response = requests.post(url, headers=headers, json={"bin": bin_number}, timeout=10)
        response.raise_for_status()
        logging.debug(f"Received response: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching BIN data for {card_number}: {e}")
        return None

def create_identity(bin_data):
    issuer = bin_data['BIN']['issuer']
    country = bin_data['BIN']['country']
    name = f"{issuer['name']} ({country['alpha2']})"
    identity_id = f"identity--{str(uuid.uuid5(IDENTITY_NS, name))}"

    if not issuer['name']:
        return Identity(
            type="identity",
            spec_version="2.1",
            id="identity--643246fc-9204-5b4b-976d-2e605b355c24",
            created_by_ref="identity--d287a5a4-facc-5254-9563-9e92e3e729ac",
            created="2020-01-01T00:00:00.000Z",
            modified="2020-01-01T00:00:00.000Z",
            name="Unknown Bank",
            identity_class="organization",
            sectors=[
                "financial-services"
            ],
            object_marking_refs=[
                "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
                "marking-definition--d287a5a4-facc-5254-9563-9e92e3e729ac"
            ]
        )


    return Identity(
        id=identity_id,
        name=name,
        created="2020-01-01T00:00:00.000Z",
        modified="2020-01-01T00:00:00.000Z",
        identity_class="organization",
        sectors=["financial-services"],
        contact_information=f"* Bank URL: {issuer['website']},\n* Bank Phone: {issuer['phone']}",
        created_by_ref="identity--d287a5a4-facc-5254-9563-9e92e3e729ac",
        object_marking_refs=[
            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
            "marking-definition--d287a5a4-facc-5254-9563-9e92e3e729ac"
        ]
    )

def create_credit_card_stix(card_data, bin_data):
    card_id = f"bank-card--{str(uuid.uuid5(OASIS_NS, card_data['card_number']))}"

    credit_card_data = {
            'type': 'bank-card',
            'spec_version': '2.1',
            'id': card_id,
            'number': card_data['card_number'],
    }
    if bin_data:
        credit_card_data.update(
            format=bin_data['BIN']['type'],
            scheme=bin_data['BIN']['scheme'],
            brand=bin_data['BIN']['brand'],
            currency=bin_data['BIN']['currency'],
            #
            level=bin_data['BIN']['level'],
            is_commercial=bin_data['BIN']['is_commercial'] == 'true',
            is_prepaid=bin_data['BIN']['is_prepaid'] == 'true',
        )
        
    # Add optional fields if they are present and not empty
    optional_fields = ['card_holder_name', 'card_valid_date', 'card_expiry_date', 'card_security_code']
    field_mapping = {
        'card_holder_name': 'holder_name',
        'card_valid_date': 'valid_from',
        'card_expiry_date': 'valid_to',
        'card_security_code': 'security_code'
    }
        
    for field in optional_fields:
        if card_data.get(field):
            credit_card_data[field_mapping[field]] = card_data[field]
    
    return credit_card_data


def create_objects(card_data, api_key):
    bin_data = get_bin_data(card_data['card_number'], api_key)
    card = create_credit_card_stix(card_data, bin_data)
    retval = []
    if bin_data and bin_data['BIN']['valid']:
        identity = create_identity(bin_data)
        retval.append(identity)
        card.update(issuer_ref=identity.id)
    retval.insert(0, BankCard(**card))
    return retval

if __name__ == '__main__':
    import os
    from pprint import pprint

    pprint(create_objects({'card_number': "559666123232123112312312332"}, os.getenv("BIN_LIST_API_KEY")))
    pprint(create_objects({'card_number': "410540"}, os.getenv("BIN_LIST_API_KEY")))
