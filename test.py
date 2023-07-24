from azure.storage.blob import BlobServiceClient
import re

# Replace with your actual connection string and pattern
connection_string = 'DefaultEndpointsProtocol=https;AccountName=pocnikhilstgacc;AccountKey=uJVTl2CIGjVsfKWkT+bbw+VqHC+KK1UKBsRtpp/SvM8UjJmn7w7dIAYmTWdw7pn3lGWfYUxFJWSG+AStCpWMTg==;EndpointSuffix=core.windows.net'

container_pattern = r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a list of all containers
containers = blob_service_client.list_containers()

# Filter the containers based on the pattern and creation date
filtered_containers = [container for container in containers if re.match(container_pattern, container.name)]

# Delete the filtered containers
# for container in filtered_containers:
#     container_client = blob_service_client.get_container_client(container.name)
#     container_client.delete_container()
[print(i.get('name')) for i in filtered_containers]