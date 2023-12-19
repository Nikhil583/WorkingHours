from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

resource_group_name = "tcp-azu0010-ase-rg-b2bdp-qa-data"
account_name = "tcp-azu0010-ase-cdb-b2bdp-qa-db01"
subscription_id = "de6c4a03-26cc-4b28-8666-f57b17ef373b"

cosmos_client = CosmosClient.from_connection_string("<your_connection_string>")

# Switch to the specified subscription
cosmos_client.get_database_client(database_name=subscription_id)

database_iter = cosmos_client.get_database_client().list_databases()

for database in database_iter:
    db_name = database['id']

    container_iter = cosmos_client.get_database_client(db_name).list_containers()

    for container in container_iter:
        container_name = container['id']

        throughput = cosmos_client.get_container_client(db_name, container_name).read_throughput()

        if throughput > 400:
            new_rus = 400
            cosmos_client.get_container_client(db_name, container_name).replace_throughput(new_rus)
            print(f"{container_name} throughput decreased to 400 from {throughput}")
