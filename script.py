#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
import os
import logging

# Suppress InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    exit(1)

# Fetch host data from API
def get_hosts_from_api():
    response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
        return None

# Function to create Ansible inventory structure
def generate_inventory():
    data = get_hosts_from_api()
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

if __name__ == "__main__":
    # Output the inventory in JSON format
    inventory = generate_inventory()
    print(json.dumps(inventory, indent=2))
