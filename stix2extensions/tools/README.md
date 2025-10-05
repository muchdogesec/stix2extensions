## creditcard2stix

This script contains logic to enrich a credit card number input with more information about the card (e.g. issuer, country, etc.).

The script takes a card number (required), card holder name (optional), expiry date (optional), security code (optional) as inputs (as a list) and outputs a range of STIX 2.1 objects for each credit card with added enrichment data.

The script requires an API key for [BIN/IP Checker](https://rapidapi.com/trade-expanding-llc-trade-expanding-llc-default/api/bin-ip-checker)


