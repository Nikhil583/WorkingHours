from azure.identity import ClientSecretCredential
from azure.mgmt.eventhub import EventHubManagementClient
import json


def Authenticate(tenant_id, client_id, client_secret, subscription_id):
    # Authenticate using ClientSecretCredential
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    eventhub_client = EventHubManagementClient(credential, subscription_id)
    return eventhub_client


def Read_json(json_file_path):
    f = open(json_file_path)
    for i in f.readlines():
        x = json.loads(str(i))
        eventhub_name = x["eventhub"]
        partition_count = x["partition"]
        retention_duration = x["retention"]

    return eventhub_name, partition_count, retention_duration


def Create_Eventhub(
    eventhub_client,
    resource_group,
    namespace_name,
    eventhub_name,
    partition_count,
    retention_duration
):
    parameters = {
        "properties": {
            "messageRetentionInDays": retention_duration,
            "partitionCount": partition_count,
        }
    }

    eventhub_client.event_hubs.create_or_update(
        resource_group, namespace_name, eventhub_name, parameters
    )


def Store_metadata(json_file_path, Creation_file_path):
    try:
        with open(Creation_file_path) as output_file:
            existing_data = json.load(output_file)

    except FileNotFoundError:
        existing_data = []

    f = open(json_file_path)
    for i in f.readlines():
        x = json.loads(i)
        existing_data.append(x)

    with open(Creation_file_path, "w") as output_file:
        json.dump(existing_data, output_file, indent=2)


def main():
    tenant_id = ""
    client_id = ""
    client_secret = ""
    subscription_id = ""
    namespace_name = "pocnikhil-eventhub"
    resource_group = "pocnikhil"
    json_file_path = "/home/b2b_platform_admin/eventhubcreation/req.json"
    Creation_file_path = "/home/b2b_platform_admin/eventhubcreation/metadata.json"

    eventhub_client = Authenticate(tenant_id, client_id, client_secret, subscription_id)
    eventhub_name, partition_count, retention_duration = Read_json(json_file_path)
    Create_Eventhub(eventhub_client,resource_group,namespace_name,eventhub_name,partition_count,retention_duration)
    Store_metadata(json_file_path, Creation_file_path)
    print(f"Event Hub '{eventhub_name}' with {partition_count} partitions and a retention of {retention_duration} has been created in the {namespace_name} namespace.")


main()
