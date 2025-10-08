from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime

print("="*70)
print(f"Task 3: Uploading Dataset to Azurite Blob Storage")
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# Azurite connection string (default local emulator)
connect_str = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

print("\nConnecting to Azurite Blob Storage...")

# Create BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create container
container_name = "datasets"
print(f"\nCreating container: '{container_name}'...")

try:
    container_client = blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created successfully!")
except Exception as e:
    print(f"Container '{container_name}' already exists or error occurred")
    print(f"Details: {e}")
    container_client = blob_service_client.get_container_client(container_name)

# Upload file
blob_name = "All_Diets.csv"
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

print(f"\nUploading '{blob_name}' to Azurite Blob Storage...")
upload_start = datetime.now()

with open("All_Diets.csv", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
    
upload_end = datetime.now()
upload_time = (upload_end - upload_start).total_seconds()

print(f"File '{blob_name}' uploaded successfully!")
print(f"Upload time: {upload_time:.2f} seconds")
print(f"\nBlob URL: {blob_client.url}")

print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)