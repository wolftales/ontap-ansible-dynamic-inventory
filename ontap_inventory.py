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
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from API: {e}")
        return None

# Main function
if __name__ == "__main__":
    hosts = get_hosts_from_api()
    if hosts:
        logger.info("Successfully fetched host data.")
        # Transform the data into Ansible inventory format
        inventory = {
            "_meta": {
                "hostvars": {}
            },
            "all": {
                "hosts": []
            }
        }
        for host in hosts.get('records', []):
            hostname = host.get('name')
            inventory["all"]["hosts"].append(hostname)
            inventory["_meta"]["hostvars"][hostname] = {
                "ansible_host": host.get('ip_address')
            }
        print(json.dumps(inventory, indent=4))
    else:
        logger.error("Failed to fetch host data.")
        print(json.dumps({
            "_meta": {
                "hostvars": {}
            },
            "all": {
                "children": [
                    "ungrouped"
                ]
            }
        }, indent=4))
