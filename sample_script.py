#!/usr/bin/env python

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
                    'ansible_host': '192.168.1.10',
                    'ansible_port': 22
                },
                'host2': {
                    'ansible_host': '192.168.1.11',
                    'ansible_port': 2222
                },
                'host3': {
                    'ansible_host': 'ec2-3-123-456-789.compute.amazonaws.com',
                    'ansible_port': 22
                }
            }
        }
    }
    return inventory

if __name__ == "__main__":
    inventory = get_inventory()
    print(json.dumps(inventory))