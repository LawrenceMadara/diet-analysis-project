from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
from datetime import datetime

def process_nutritional_data_from_azurite():
    """
    Serverless function to process nutritional data from Azurite Blob Storage
    Simulates Azure Function behavior locally
    """
    print("="*70)
    print(f"SERVERLESS FUNCTION - Task 3")
    print(f"Function invoked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Azurite connection string
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    container_name = 'datasets'
    blob_name = 'All_Diets.csv'
    
    # Step 1: Connect to Azurite Blob Storage
    print(f"\nStep 1: Connecting to Azurite Blob Storage...")
    print(f"Container: {container_name}")
    print(f"Blob: {blob_name}")
    
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    
    # Step 2: Download blob content
    print(f"\nStep 2: Downloading blob from Azurite...")
    download_start = datetime.now()
    
    stream = blob_client.download_blob().readall()
    
    download_end = datetime.now()
    download_time = (download_end - download_start).total_seconds()
    
    print(f"Download completed in {download_time:.2f} seconds")
    print(f"Downloaded {len(stream)} bytes")
    
    # Step 3: Load into pandas
    print(f"\nStep 3: Loading data into pandas DataFrame...")
    df = pd.read_csv(io.BytesIO(stream))
    
    print(f"Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")
    
    # Step 4: Process data
    print(f"\nStep 4: Processing nutritional data...")
    print(f"Calculating average macronutrients by diet type...")
    
    # Calculate averages
    numerical_columns = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
    avg_macros = df.groupby('Diet_type')[numerical_columns].mean()
    
    print("\nAverage Macronutrients by Diet Type:")
    print("="*70)
    print(avg_macros.round(2))
    print("="*70)
    
    # Step 5: Prepare results for NoSQL storage
    print(f"\nStep 5: Preparing results for NoSQL storage...")
    
    result = {
        'function_execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_source': f'Azurite Blob Storage: {blob_client.url}',
        'total_recipes': int(len(df)),
        'total_diet_types': int(len(df['Diet_type'].unique())),
        'diet_types': df['Diet_type'].unique().tolist(),
        'average_macronutrients': {
            diet: {
                'protein_g': float(avg_macros.loc[diet, 'Protein(g)']),
                'carbs_g': float(avg_macros.loc[diet, 'Carbs(g)']),
                'fat_g': float(avg_macros.loc[diet, 'Fat(g)'])
            }
            for diet in avg_macros.index
        },
        'processing_metadata': {
            'download_time_seconds': download_time,
            'blob_size_bytes': len(stream),
            'rows_processed': len(df)
        }
    }
    
    # Step 6: Save to simulated NoSQL storage (JSON file)
    output_file = 'simulated_nosql_results.json'
    print(f"\nStep 6: Saving results to simulated NoSQL storage...")
    print(f"Output file: {output_file}")
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Results saved successfully!")
    
    # Summary
    print("\n" + "="*70)
    print("FUNCTION EXECUTION SUMMARY")
    print("="*70)
    print(f"Status: SUCCESS")
    print(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data source: Azurite Blob Storage")
    print(f"Records processed: {len(df)}")
    print(f"Output: {output_file}")
    print("="*70)
    
    return "Data processed and stored successfully in NoSQL storage."

# Simulate function invocation
if __name__ == "__main__":
    print("\n" + "="*70)
    print("SIMULATING SERVERLESS FUNCTION INVOCATION")
    print("="*70)
    
    result = process_nutritional_data_from_azurite()
    
    print(f"\nFunction return value: {result}")
    print("\n" + "="*70)