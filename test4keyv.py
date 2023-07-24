from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
import re


credential = DefaultAzureCredential()

# add key vault name
vault_url = "https://KEY_VAULT_NAME.vault.azure.net"
secret_client = SecretClient(vault_url=vault_url, credential=credential)

secret_name = "your-secret-name"
secret_value = secret_client.get_secret(secret_name).value

blob_service_client = BlobServiceClient.from_connection_string(secret_value)

containers = blob_service_client.list_containers()

container_pattern = r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'

excluded_container_names = ['b2bappfs', 'b2bdata', 'b2barchivedata', 'b2bbackup', 'b2bdatahub', 'b2bdatahubapi', 'b2blogs', 'b2bops', 'b2bstage']

filtered_containers = [container for container in containers if re.match(container_pattern, container.name) and container.name not in excluded_container_names]

for container in filtered_containers:
    # container_client = blob_service_client.get_container_client(container.name)
    # container_client.delete_container()
    print(container.get("name"))