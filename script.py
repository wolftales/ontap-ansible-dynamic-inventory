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

# Function to fetch host data from API
def get_hosts_from_api(url, username, password):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from API: {e}")
        return None

# Function to create Ansible inventory structure
def generate_inventory(url, username, password):
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

# Main function
def main():
    # Fetch API hostname and endpoint from environment variables
    hostname = os.getenv("API_HOSTNAME", "192.168.7.225")
    api_endpoint = os.getenv("API_ENDPOINT", "/datacenter/cluster/clusters")
    base_url = f"https://{hostname}/api"
    url = f"{base_url}{api_endpoint}"

    # Fetch credentials from environment variables
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")

    if not username or not password:
        logger.error("API credentials are not set in environment variables.")
        return 1

    # Generate and print the inventory
    inventory = generate_inventory(url, username, password)
    print(json.dumps(inventory, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
