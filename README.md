# ontap-ansible-dynamic-inventory

This repository provides a dynamic inventory script for Ansible to interact with NetApp ActiveIQ Unified Manager systems. The script allows for automated discovery and management of ONTAP resources.

## Features

- Dynamic inventory generation from ActiveIQ Unified Manager for ONTAP systems
- Automated resource discovery
- Seamless integration with Ansible playbooks
- Enhanced error handling and logging

## Requirements

- Python 3.x
- Ansible 2.9+
- NetApp ONTAP Python client library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ontap-ansible-dynamic-inventory.git
    ```
2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Set the following environment variables for API credentials and configuration:
```sh
export API_USERNAME="your_username"
export API_PASSWORD="your_password"
export API_HOSTNAME="your_activeiq_hostname_or_ip"
export API_ENDPOINT="/datacenter/cluster/clusters"  # Optional, defaults to /datacenter/cluster/clusters
```

## Testing

Test script's ability to collect information from NetApp's ActiveIQ Unified Manager:
```shell
ansible-inventory -i ontap_inventory.py --list
```

## Usage

1. Configure the inventory script by editing `inventory.ini`:
    ```ini
    [ontap]
    hostname = your_ontap_hostname
    username = your_username
    password = your_password
    ```

2. Run the Ansible playbook with the dynamic inventory:
    ```sh
    ansible-playbook -i ontap_inventory.py your_playbook.yml
    ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- NetApp for their ONTAP systems and Python client library
- Ansible community for their continuous support and development
