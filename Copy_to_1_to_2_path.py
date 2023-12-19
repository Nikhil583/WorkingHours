import os
import shutil
import csv

filename = 'FilesToCopy.csv'
source_folder = "C:\\AzureDevOps\\B2BDP-ETL-Jobs\\pipeline\\"
destination_folder = "C:\\Users\\e013230\\Pictures\\New folder\\"


def copy_json_files(source_folder, destination_folder, file_list):
    count=1
    for row in file_list:
        source_path = os.path.join(source_folder, row[1] + ".json")
        # print(source_path)
        destination_path = os.path.join(destination_folder, row[1] + ".json")

        try:
            # Check if the file already exists in the destination folder
            if os.path.exists(destination_path):
                os.remove(destination_path)
                print(f"File '{row[1]}.json' in the destination folder already exists. It will be replaced.")

            shutil.copy2(source_path, destination_folder)
            print(f"{count} File '{row[1]}.json' copied successfully.")
            count=count+1
        except FileNotFoundError:
            print(f"Error: File '{row[1]}.json' not found in the source folder.")
        except PermissionError:
            print(f"Error: Permission denied for file '{row[1]}.json'.")
        except Exception as e:
            print(f"Error: {e}")

with open(filename, 'r') as csvfile:
    file_list = csv.reader(csvfile)
    next(file_list)  # Skip header row
    copy_json_files(source_folder, destination_folder, file_list)
