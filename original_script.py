#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
import os

# Suppress InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API credentials and URL
base_url = "https://192.168.7.225/api"
api_endpoint = "/datacenter/cluster/clusters"
url = f"{base_url}{api_endpoint}"

# Fetch credentials from environment variables
username = os.getenv("AIQUM_USERNAME", "admin")
password = os.getenv("AIQUM_PASSWORD", "Netapp1!")

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