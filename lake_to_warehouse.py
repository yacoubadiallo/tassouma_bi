import polars as pl
import boto3
from io import BytesIO
from botocore.client import Config
from sqlalchemy import create_engine

# --- CONFIGURATION RÉSEAU DOCKER ---
# On utilise les noms des services définis dans le docker-compose
PG_URL = "postgresql://bi_user:bi_password@db_warehouse:5432/warehouse"

MINIO_PARAMS = {
    "endpoint_url": "http://minio:9000", # Correction localhost -> minio
    "aws_access_key_id": "admin",
    "aws_secret_access_key": "admin_password",
    "config": Config(signature_version='s3v4', s3={'addressing_style': 'path'})
}

s3 = boto3.client("s3", **MINIO_PARAMS)

def get_latest_file(bucket, table_name):
    prefix = f"bronze/{table_name}/"
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' not in response:
            return None
        latest = max(response['Contents'], key=lambda x: x['LastModified'])
        return latest['Key']
    except Exception as e:
        print(f"Erreur lors de la recherche du fichier pour {table_name}: {e}")
        return None

def transfer_data():
    tables = ['core_vente', 'core_lignevente', 'core_produit', 'core_boutique', 'core_categorie', 'core_marque']
    
    print("Lancement du transfert Lake -> Warehouse")
    
    for table in tables:
        key = get_latest_file("tassouma-lake", table)
        
        if key:
            try:
                print(f"Chargement de : {table} (fichier: {key})...")
                response = s3.get_object(Bucket="tassouma-lake", Key=key)
                df = pl.read_parquet(BytesIO(response['Body'].read()))
                
                # On prépare le nom avec le schéma bronze
                full_table_name = f"bronze.{table}"
                
                # Injection dans PostgreSQL
                df.write_database(
                    table_name=full_table_name, 
                    connection=PG_URL,
                    if_table_exists="replace"
                )
                print(f"{full_table_name} injectée avec succès.")
            except Exception as e:
                print(f"Erreur sur la table {table}: {e}")
        else:
            print(f"Aucun fichier trouvé pour {table}")

if __name__ == "__main__":
    transfer_data()