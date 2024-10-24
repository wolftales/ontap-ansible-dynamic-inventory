#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
import os
import sys
import logging

# Suppress InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for default values
DEFAULT_HOSTNAME = "192.168.7.225"
DEFAULT_API_ENDPOINT = "/datacenter/cluster/clusters"

def get_hosts_from_api(url, username, password):
    """
    Fetch host data from the API.

    Args:
        url (str): The API endpoint URL.
        username (str): The API username.
        password (str): The API password.

    Returns:
        dict: The JSON response from the API if successful, None otherwise.
    """
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from API: {e}")
        return None

def generate_inventory(url, username, password):
    """
    Create Ansible inventory structure from API data.

    Args:
        url (str): The API endpoint URL.
        username (str): The API username.
        password (str): The API password.

    Returns:
        dict: The inventory structure in JSON format.
    """
    data = get_hosts_from_api(url, username, password)
    if data is None:
        return {}

    inventory = {"_meta": {"hostvars": {}}}

    # Process the hosts from the API and add to inventory
    for record in data.get("records", []):
        name = record.get("name")
        management_ip = record.get("management_ip")

        # Adding the host to a group called 'datacenter_clusters'
        if "datacenter_clusters" not in inventory:
            inventory["datacenter_clusters"] = {"hosts": []}

        # Append host to the group
        inventory["datacenter_clusters"]["hosts"].append(management_ip)

        # Add host-specific variables under _meta
        inventory["_meta"]["hostvars"][management_ip] = {
            "ansible_host": management_ip,
            "cluster_name": name,
            "model": record.get("models"),
            "version": record.get("version", {}).get("full"),
            "location": record.get("location"),
            "uuid": record.get("uuid"),
        }

    return inventory

def fetch_configuration():
    """
    Fetch configuration from environment variables.

    Returns:
        tuple: A tuple containing the hostname, API endpoint, username, and password.
    """
    hostname = os.getenv("API_HOSTNAME", DEFAULT_HOSTNAME)
    api_endpoint = os.getenv("API_ENDPOINT", DEFAULT_API_ENDPOINT)
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")

    if not username or not password:
        logger.error("API credentials are not set in environment variables.")
        sys.exit(1)

    base_url = f"https://{hostname}/api"
    url = f"{base_url}{api_endpoint}"

    return url, username, password

def main():
    """
    Main function to fetch API credentials, generate inventory, and print it.

    Returns:
        int: Exit status code.
    """
    url, username, password = fetch_configuration()

    # Generate and print the inventory
    inventory = generate_inventory(url, username, password)
    print(json.dumps(inventory, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
