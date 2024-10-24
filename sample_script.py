#!/usr/bin/env python

# Sample script for dynamic inventory in Ansible
# Source: Ansible Documentation (https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)

import json

def get_inventory():
    # Define your dynamic hosts and groups here
    inventory = {
        'group1': {
            'hosts': ['host1', 'host2'],
            'vars': {
                'ansible_user': 'admin',
                'ansible_ssh_private_key_file': '~/.ssh/id_rsa'
            }
        },
        'group2': {
            'hosts': ['host3'],
            'vars': {
                'ansible_user': 'ubuntu',
                'ansible_ssh_private_key_file': '~/.ssh/id_rsa_aws'
            }
        },
        '_meta': {
            'hostvars': {
                'host1': {
                    # Host-specific variables
                },
                'host2': {
                    # Host-specific variables
                },
                'host3': {
                    # Host-specific variables
                }
            }
        }
    }
    return inventory

if __name__ == "__main__":
    inventory = get_inventory()
    print(json.dumps(inventory, indent=2))