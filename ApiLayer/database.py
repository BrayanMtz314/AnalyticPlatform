# src/database.py
import snowflake.connector
from typing import Generator
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from config import settings

logger = logging.getLogger(__name__)

def get_db_connection() -> Generator[snowflake.connector.SnowflakeConnection, None, None]:
    """
    Creates an RSA-authenticated Snowflake connection, yields it to the FastAPI route, 
    and ensures it is closed after the request is finished.
    """
    conn = None
    try:
        # 1. Read and decode the unencrypted private key
        with open(settings.snowflake_private_key_path, "rb") as key_file:
            p_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # 2. Convert to DER format required by the Snowflake connector
        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # 3. Establish the connection using the private_key
        conn = snowflake.connector.connect(
            user=settings.snowflake_user,
            account=settings.snowflake_account,
            private_key=pkb,
            role=settings.snowflake_role,
            warehouse=settings.snowflake_warehouse,
            database=settings.snowflake_database,
            schema=settings.snowflake_schema
        )
        
        yield conn
        
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {e}")
        raise
    finally:
        if conn:
            conn.close()