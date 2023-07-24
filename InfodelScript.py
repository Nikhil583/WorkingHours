from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from datetime import datetime,timedelta
import datetime

# Set variables for Azure Storage account and date
rg = "poc_test_nikhil_s"
acc_name = "pocnikhilstgacc"
d = datetime.now() - timedelta(days=7)
compare_d = datetime.timestamp(d)

# Connect to Azure Blob Storage API using Spark SQL configuration settings
spark = SparkSession.builder.appName("AzureBlobStorageAPI").getOrCreate()
sc = spark.sparkContext
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.azure.account.auth.type." + acc_name + ".blob.core.windows.net", "OAuth")
hadoop_conf.set("fs.azure.account.oauth.provider.type." + acc_name + ".blob.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
hadoop_conf.set("fs.azure.account.oauth2.client.id." + acc_name + ".blob.core.windows.net", "")
hadoop_conf.set("fs.azure.account.oauth2.client.secret." + acc_name + ".blob.core.windows.net", "")
hadoop_conf.set("fs.azure.account.oauth2.client.endpoint." + acc_name + ".blob.core.windows.net", "")

# Retrieve a list of all containers associated with the specified Azure Storage account
df_containers = spark.read.format("com.microsoft.azure.cosmosdb.spark").\
option("database", "AzureStorage").\
option("collection", "containers").\
option("spark.cosmos.read.inferSchema.enabled", "true").\
option("spark.cosmos.read.inferSchemaSamplingRatio", "1.0").\
load()

# Filter the list of storage containers based on a regular expression pattern and a specified date
pattern = "([a-z0-9]{8})-([a-z0-9]{4})-([a-z0-9]{4})-([a-z0-9]{4})-([a-z0-9]{12})"
df_filtered = df_containers.filter((col("name").rlike(pattern)) & (col("lastModifiedDate") < compare_d))

# Define a list of container names to keep
array1 = ["b2bdata", "b2bops", "b2bappfs"]

# Identify any containers in the filtered list that are not present in the list of container names to keep
array2 = [row.name for row in df_filtered.select("name").collect()]
note = list(set(array2) - set(array1))

# Remove any identified containers from the specified Azure Storage account
for c in note:
    df_filtered.filter(df_filtered.name == c).write.format("com.microsoft.azure.cosmosdb.spark").\
    mode("overwrite").\
    option("database", "AzureStorage").\
    option("collection", "containers").\
    save()

print(c + " is removed from " + acc_name)