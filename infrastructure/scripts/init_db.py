import os
import pandas as pd
from pathlib import Path
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

# New imports for RSA Key parsing
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def main():
    # 1. Dynamically find paths
    current_dir = Path(__file__).parent
    infrastructure_dir = current_dir.parent 
    
    data_dir = infrastructure_dir / "Data"
    env_path = infrastructure_dir / ".env"
    
    # Point directly to the RSA key we made for Terraform
    private_key_path = infrastructure_dir / "rsa_key.p8"

    load_dotenv(dotenv_path=env_path)

    # 2. Read and decode the unencrypted private key
    with open(private_key_path, "rb") as key_file:
        p_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None, # We used -nocrypt, so there is no password
            backend=default_backend()
        )

    # Convert to DER format required by the Snowflake connector
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 3. Establish the connection using the private_key (no password)
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        private_key=pkb,
        role="ACCOUNTADMIN",
        warehouse="ANALYTICS_WH",
        database="ANALYTICS_PLATFORM_DB",
        schema="API_DATA"
    )

    # 4. Loop through all CSVs and upload them
    for csv_file in data_dir.glob("*.csv"):
        table_name = csv_file.stem.upper()
        print(f"Preparing to upload {csv_file.name} into table {table_name}...")
        
        df = pd.read_csv(csv_file)
        df.columns = [col.upper() for col in df.columns]
        
        success, nchunks, nrows, _ = write_pandas(
            conn=conn, 
            df=df, 
            table_name=table_name, 
            auto_create_table=True
        )
        
        if success:
            print(f"Successfully uploaded {nrows} rows to {table_name}.")
        else:
            print(f"Failed to upload {table_name}.")

    conn.close()

if __name__ == "__main__":
    main()