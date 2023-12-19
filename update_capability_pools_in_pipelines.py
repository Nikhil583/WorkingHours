                                                                                                                            # This python script is used to update the capability pool parameter in all the python activities in a pipeline.
# It takes csv file named as "pipelinename-poolname-mapping-test.csv" as input. The CSV file has two fields comma separated - pipeline name and new global parameter name (which needs to be updated).
# There should be no header row in the CSV.
# If the name of CSV file has been changed then the filename valiable in below script should be changed to that filename.
# The script loops through all the pipeline names in the CSV file and checks all the python activities in the pipeline. If the python activity is having global parameter as - "@pipeline().globalParameters.DefaultPool", it will update it to the pool name mentioned in the CSV file.


import csv
import json

filename = 'pipelinename-poolname-mapping-test.csv'
defaultpoolname = "@pipeline().globalParameters.DefaultPool"
path = "C:\\AzureDevOps\\B2BDP-ETL-Jobs\\pipeline\\"

def parse_json_recursively(json_object, target_key):
    if type(json_object) is dict and json_object:
        for key in json_object:
            if key == target_key:
                if json_object['linkedServiceName']['referenceName'][0:11]=="B2BDP_DBR10":
                    #print("ADB Linked Service Found")
                    if "parameters" in json_object['linkedServiceName'].keys():
                        if "capabilityPool" in json_object['linkedServiceName']['parameters'].keys():
                            try:
                                if "value" in json_object['linkedServiceName']['parameters']['capabilityPool'].keys():
                                    if json_object['linkedServiceName']['parameters']['capabilityPool']['value']=="@pipeline().globalParameters.DefaultPool":
                                        json_object['linkedServiceName']['parameters']['capabilityPool']['value'] = newpoolname
                                        #print("capabilityPool Updated: " + json_object['linkedServiceName']['parameters']['capabilityPool']['value'])
                            except AttributeError:
                                json_object['linkedServiceName']['parameters']['capabilityPool'] = {"value": newpoolname, "type": "Expression"}
                        else:
                            json_object['linkedServiceName']['parameters']['capabilityPool'] = {"value": newpoolname, "type": "Expression"}
                            #print("capabilityPool Added: " + json_object['linkedServiceName']['parameters']['capabilityPool']['value'])
                    else:
                        json_object['linkedServiceName']['parameters'] = {"capabilityPool": {"value": newpoolname, "type": "Expression"}}
                    
            parse_json_recursively(json_object[key], target_key)

    elif type(json_object) is list and json_object:
        for item in json_object:
            parse_json_recursively(item, target_key)



with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        #pipelinejson = path+row[1]+".json"
        pipelinejson = path+row[1]+".json"
        newpoolname = "@pipeline().globalParameters." + row[2]
        print(pipelinejson + "," + newpoolname)

        with open(pipelinejson, "r") as infile:
            data = json.load(infile)

        target_key = "linkedServiceName"
        parse_json_recursively(data, target_key)
        
        with open(pipelinejson, "w") as outfile:
            outfile.write(json.dumps(data,indent=4))

        newfile  = open(pipelinejson, 'r').read()
        dbr_linkedservice_count = newfile.count("B2BDP_DBR10")
        capabilitypool_parameter_count = newfile.count("capabilityPool")
        print("DBR Linked Service Count=" + str(dbr_linkedservice_count) + " capabilityPool Parameter Count=" + str(capabilitypool_parameter_count))

        if dbr_linkedservice_count != capabilitypool_parameter_count:
            print("********************MISMATCH in File - " + pipelinejson + " Please validate Manually ********************")
