from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import re

credential = DefaultAzureCredential()

account_name = 'pocnikhilstgacc'

blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=credential)

containers = blob_service_client.list_containers()

container_pattern = r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'

# Container names to exclude from deletion
excluded_container_names = ['b2bappfs', 'b2bdata', 'b2barchivedata', 'b2bbackup', 'b2bdatahub',
                            'b2bdatahubapi', 'b2blogs', 'b2bops', 'b2bstage']


# Filter the containers based on the pattern and exclude specific container names
filtered_containers = [container for container in containers if re.match(container_pattern, container.name)
                       and container.name not in excluded_container_names]

# Delete the filtered containers
for container in filtered_containers:
    # container_client = blob_service_client.get_container_client(container.name)
    # container_client.delete_container()
    print(container.get("name"))