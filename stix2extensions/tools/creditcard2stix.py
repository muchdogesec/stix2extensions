from functools import lru_cache
import logging
from urllib.parse import urljoin
import uuid
import requests
from stix2 import Relationship, Identity
from .._extensions import DOGESEC_IDENTITY_REF, S2E_MARKING_REFS

from ..bank_card import BankCard


UUID_NS = uuid.UUID("60c0f466-511a-5419-9f7e-4814e696da40")


@lru_cache(maxsize=4096)
def get_bin_data(card_number, api_key):
    try:
        bin_number = card_number[:6]
        url = f"https://bin-ip-checker.p.rapidapi.com/?bin={bin_number}"
        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": "bin-ip-checker.p.rapidapi.com",
            "x-rapidapi-key": api_key,
        }
        logging.debug(f"Requesting BIN data for card number: {card_number}")
        response = requests.post(
            url, headers=headers, json={"bin": bin_number}, timeout=10
        )
        response.raise_for_status()
        logging.debug(f"Received response: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching BIN data for {card_number}: {e}")
        return None


@lru_cache
def get_country(country):
    try:
        resp = requests.get(
            urljoin(
                os.environ.get("CTIBUTLER_BASE_URL", ""),
                f"v1/location/objects/?alpha2_code={country}",
            ),
            headers={"API-KEY": os.environ.get("CTIBUTLER_API_KEY")},
        )
        resp.raise_for_status()
        return resp.json()["objects"][0]
    except Exception as e:
        logging.error(f"Error fetching country data for {country}: {e}")


def create_identity(bin_data):
    issuer = bin_data["BIN"]["issuer"]
    country = bin_data["BIN"]["country"]
    name = f"{issuer['name']} ({country['alpha2']})"
    identity_id = f"identity--{str(uuid.uuid5(UUID_NS, name))}"

    if not issuer["name"]:
        return Identity(
            type="identity",
            spec_version="2.1",
            id="identity--643246fc-9204-5b4b-976d-2e605b355c24",
            created_by_ref=DOGESEC_IDENTITY_REF,
            created="2020-01-01T00:00:00.000Z",
            modified="2020-01-01T00:00:00.000Z",
            name="Unknown Bank",
            identity_class="organization",
            sectors=["financial-services"],
            object_marking_refs=S2E_MARKING_REFS,
        )

    return Identity(
        id=identity_id,
        name=name,
        created="2020-01-01T00:00:00.000Z",
        modified="2020-01-01T00:00:00.000Z",
        identity_class="organization",
        sectors=["financial-services"],
        contact_information=f"* Bank URL: {issuer['website']},\n* Bank Phone: {issuer['phone']}",
        created_by_ref=DOGESEC_IDENTITY_REF,
        object_marking_refs=S2E_MARKING_REFS,
    )


def create_credit_card_stix(card_data: dict, bin_data: dict):
    credit_card_data = {
        "type": "bank-card",
        "spec_version": "2.1",
        "number": card_data["card_number"],
    }
    if bin_data:
        credit_card_data.update(
            format=bin_data["BIN"]["type"],
            scheme=bin_data["BIN"]["scheme"],
            brand=bin_data["BIN"]["brand"],
            currency=bin_data["BIN"]["currency"],
            #
            level=bin_data["BIN"]["level"],
            is_commercial=bin_data["BIN"]["is_commercial"] == "true",
            is_prepaid=bin_data["BIN"]["is_prepaid"] == "true",
        )

    # Add optional fields if they are present and not empty
    optional_fields = [
        "card_holder_name",
        "card_valid_date",
        "card_expiry_date",
        "card_security_code",
    ]
    field_mapping = {
        "card_holder_name": "holder_name",
        "card_valid_date": "valid_from",
        "card_expiry_date": "valid_to",
        "card_security_code": "security_code",
    }

    for field in optional_fields:
        if card_data.get(field):
            credit_card_data[field_mapping[field]] = card_data[field]

    return credit_card_data


def create_objects(card_data, api_key):
    bin_data = get_bin_data(card_data["card_number"], api_key)
    card = create_credit_card_stix(card_data, bin_data)
    retval = []
    if bin_data and bin_data["BIN"]["valid"]:
        identity = create_identity(bin_data)
        if identity.contact_information:
            location = get_country(bin_data["BIN"]["country"]["alpha2"])
            retval.append(location)
            r_uuid = str(
                uuid.uuid5(UUID_NS, f'located-at+{identity.id}+{location["id"]}')
            )
            retval.append(
                Relationship(
                    type="relationship",
                    spec_version="2.1",
                    id="relationship--" + r_uuid,
                    created_by_ref="identity--9779a2db-f98c-5f4b-8d08-8ee04e02dbb5",
                    created="2020-01-01T00:00:00.000Z",
                    modified="2020-01-01T00:00:00.000Z",
                    relationship_type="located-at",
                    source_ref=identity.id,
                    target_ref=location["id"],
                    description=f"{bin_data['BIN']['issuer']['name']} is located at {bin_data['BIN']['country']['name']}",
                    object_marking_refs=S2E_MARKING_REFS,
                )
            )
        retval.append(identity)
        card.update(issuer_ref=identity.id)
    retval.insert(0, BankCard(**card))
    return retval


if __name__ == "__main__":
    import os
    from pprint import pprint
    from stix2.serialization import serialize

    print(
        serialize(
            create_objects(
                {"card_number": "559666123232123112312312332"},
                os.getenv("BIN_LIST_API_KEY"),
            )
        )
    )
    print(
        serialize(
            create_objects({"card_number": "410540"}, os.getenv("BIN_LIST_API_KEY"))
        )
    )
