#from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

def get_cosmos_client(endpoint, key):
    return CosmosClient(endpoint, credential=key)

def get_database_and_container(client, database_name, container_name):
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return database, container

def cosmos_ru_changer(container):
    offer = container.read_offer()
    
    if offer is not None:
        current_ru = offer.offer_throughput
        print("Current RU/s:", current_ru)

        # Uncomment and update the following lines if you want to change throughput
        # updated_throughput = offer.properties["content"]["offerIsRUPerMinuteThroughputEnabled"] = False
        # updated_throughput = offer.properties["content"]["offerThroughput"] = 400
        # container.replace_throughput(updated_throughput)
    else:
        print("Failed to retrieve the offer for the container.")

def list_cosmos_databases_and_containers(client):
    databases = client.list_databases()
    for database in databases:
        db_name = database['id']
        container_iter = client.get_database_client(db_name).list_containers()

        for container in container_iter:
            container_name = container['id']
            print(db_name + "------------" + container_name)
            database, container = get_database_and_container(client, db_name, container_name)
            cosmos_ru_changer(container)

def main(account_name, endpoint, key):
    client = get_cosmos_client(endpoint, key)
    list_cosmos_databases_and_containers(client)

account_name = []
account_endpoint = []
account_key=[]
for i in range(len(account_name)):
    print(account_name[i])
    main(account_name[i], account_endpoint[i], account_key[i])
