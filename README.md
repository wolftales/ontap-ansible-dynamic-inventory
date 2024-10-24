# ontap-ansible-dynamic-inventory

## Introduction

The `ontap-ansible-dynamic-inventory` project provides a dynamic inventory script for Ansible, designed to interact with NetApp ActiveIQ Unified Manager systems. This script automates the discovery and management of ONTAP resources, enabling seamless integration with Ansible playbooks.

NetApp's ActiveIQ Unified Manager is a powerful tool for monitoring and managing ONTAP storage systems. By leveraging its API, this project dynamically generates an inventory of ONTAP clusters and management IPs, which can be used by Ansible for configuration management, automation, and orchestration tasks.

## Features

- **Dynamic Inventory Generation**: Automatically discover ONTAP clusters and management IPs from ActiveIQ Unified Manager.
- **Automated Resource Discovery**: Simplify the management of ONTAP resources by dynamically updating the inventory.
- **Seamless Ansible Integration**: Use the generated inventory directly in your Ansible playbooks for efficient automation.
- **Enhanced Error Handling and Logging**: Robust error handling and logging to ensure reliability and ease of troubleshooting.

### Why Use This Project?

Managing ONTAP resources manually can be time-consuming and error-prone. This project aims to streamline the process by providing a dynamic inventory that automatically reflects the current state of your ONTAP environment. Whether you are deploying new configurations, updating existing ones, or performing routine maintenance, this dynamic inventory script ensures that your Ansible playbooks always have the most up-to-date information.

### Known Limitations

- **Node Information**: The current version only provides management IPs and does not include detailed node information.
- **Limited API Coverage**: Only specific endpoints of the ActiveIQ Unified Manager API are utilized.

### Future Enhancements

- **Node Information**: Add support for detailed node information in the inventory.
- **Extended API Coverage**: Utilize additional endpoints of the ActiveIQ Unified Manager API to provide more comprehensive inventory data.

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

## Usage

This script is used to dynamically generate an inventory for Ansible by collecting information from NetApp's ActiveIQ Unified Manager. This allows for automated discovery and management of ONTAP resources within your Ansible playbooks.

1. Ensure the required environment variables are set:
    ```sh
    export API_USERNAME="your_username"
    export API_PASSWORD="your_password"
    export API_HOSTNAME="your_activeiq_hostname_or_ip"
    export API_ENDPOINT="/datacenter/cluster/clusters"  # Optional, defaults to /datacenter/cluster/clusters
    ```

2. Test the script's ability to collect information from NetApp's ActiveIQ Unified Manager:
    ```sh
    ansible-inventory -i ontap_inventory.py --list
    ```

3. Run the Ansible playbook with the dynamic inventory:
    ```sh
    ansible-playbook -i ontap_inventory.py your_playbook.yml
    ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Acknowledgements

- NetApp for their ONTAP systems and Python client library
- Ansible community for their continuous support and development
