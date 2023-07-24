from azure.storage.blob import BlobServiceClient
import getpass
import re

def infodel(connection_string):
    # Replace with your actual connection string and pattern
    container_pattern = r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'

    # Container names to exclude from deletion
    excluded_container_names = ['b2bappfs', 'b2bdata', 'b2barchivedata', 'b2bbackup', 'b2bdatahub',
                                'b2bdatahubapi', 'b2blogs', 'b2bops', 'b2bstage']

    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a list of all containers
    containers = blob_service_client.list_containers()

    # Filter the containers based on the pattern and exclude specific container names
    filtered_containers = [container for container in containers if re.match(container_pattern, container.name)
                           and container.name not in excluded_container_names]

    # Delete the filtered containers
    for container in filtered_containers:
        # container_client = blob_service_client.get_container_client(container.name)
        # container_client.delete_container()
        print(container.get("name"))
        
connection_string=getpass.getpass("Enter SAS Token")
infodel(connection_string)