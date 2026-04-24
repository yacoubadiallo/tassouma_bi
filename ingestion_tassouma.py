import os
import sys
import logging
from datetime import datetime
from io import BytesIO
from typing import List, Optional
import polars as pl
import boto3
from sqlalchemy import create_engine
from botocore.exceptions import ClientError
from botocore.client import Config

# --- CONFIGURATION RÉSEAU DOCKER ---
# On utilise 'db_prod' et le port 3306 car le script tourne à l'intérieur du réseau Docker
MYSQL_URL = "mysql+pymysql://root:root_password@db_prod:3306/projetbi"
MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "admin_password" 
BUCKET_NAME = "tassouma-lake"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("Ingestor-Senior")

class DataLakeIngestor:
    def __init__(self):
        # Correction : suppression du type explicite 'Engine' pour éviter l'ImportError
        self.mysql_engine = create_engine(
            MYSQL_URL, 
            pool_recycle=3600, 
            pool_pre_ping=True
        )
        
        # Configuration S3 optimisée pour le réseau interne de MinIO
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name="us-east-1",
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'} 
            )
        )
        self._bootstrap_environment()

    def _bootstrap_environment(self) -> None:
        """Vérification et création automatique du bucket au démarrage."""
        try:
            self.s3_client.head_bucket(Bucket=BUCKET_NAME)
            logger.info(f"Connexion établie au bucket : {BUCKET_NAME}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ['NoSuchBucket', '404']:
                logger.info(f"Création du bucket {BUCKET_NAME}...")
                self.s3_client.create_bucket(Bucket=BUCKET_NAME)
            else:
                logger.warning(f"Erreur check bucket ({error_code}). Tentative d'upload direct.")

    def extract_table(self, table_name: str) -> Optional[pl.DataFrame]:
        """Extraction des données MySQL vers Polars."""
        try:
            logger.info(f"Extraction MySQL -> Polars : {table_name}")
            df = pl.read_database(
                query=f"SELECT * FROM {table_name}",
                connection=self.mysql_engine
            )
            return df
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction de {table_name}: {str(e)}")
            return None

    def transform_to_serialized_parquet(self, df: pl.DataFrame) -> BytesIO:
        """Conversion du DataFrame en format Parquet en mémoire."""
        buffer = BytesIO()
        df.write_parquet(buffer, compression="snappy")
        buffer.seek(0)
        return buffer

    def upload_to_lake(self, buffer: BytesIO, table_name: str, row_count: int) -> None:
        """Upload vers MinIO avec structure de dossiers (Bronze Layer)."""
        now = datetime.now()
        partition_path = (
            f"bronze/{table_name}/"
            f"year={now.year}/month={now.month:02d}/day={now.day:02d}"
        )
        file_name = f"load_{now.strftime('%H%M%S')}.parquet"
        s3_key = f"{partition_path}/{file_name}"

        try:
            self.s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=buffer.getvalue(),
                Metadata={
                    "row_count": str(row_count),
                    "ingestion_timestamp": now.isoformat()
                }
            )
            logger.info(f"Succès : {table_name} envoyé ({row_count} lignes)")
        except Exception as e:
            logger.error(f"Échec upload {table_name}: {str(e)}")

    def run(self, tables: List[str]) -> None:
        """Point d'entrée du pipeline pour la liste des tables."""
        logger.info("Lancement du pipeline d'ingestion")
        for table in tables:
            df = self.extract_table(table)
            if df is not None and not df.is_empty():
                parquet_data = self.transform_to_serialized_parquet(df)
                self.upload_to_lake(parquet_data, table, df.height)
            else:
                logger.warning(f"Table {table} vide ou introuvable.")

if __name__ == "__main__":
    # Liste des tables de ton projet 'projetbi'
    TABLES_TO_INGEST = [
        'core_vente', 'core_lignevente', 'core_produit', 
        'core_boutique', 'core_categorie', 'core_marque'
    ]
    ingestor = DataLakeIngestor()
    ingestor.run(TABLES_TO_INGEST)