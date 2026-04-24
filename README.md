Tassouma Sales Analytics | Modern Data Stack (ELT)

**Yacouba DIALLO — INGÉNIEUR BIG DATA**

Pipeline de données haute performance conçu pour centraliser et analyser les flux de ventes multi-boutiques (Région AES). Cette solution automatise l'ingestion, le stockage en Data Lake, la modélisation en Warehouse et la restitution BI.

## 🏗️ Architecture du Pipeline

L'infrastructure repose sur une architecture **cloud-native** entièrement conteneurisée, orchestrée par Airflow.

```mermaid
graph LR
    subgraph "Sources (On-premise)"
        DB[(MySQL)]
    end

    subgraph "Orchestration"
        AF[Apache Airflow]
    end

    subgraph "Data Lake (S3)"
        MI[MinIO Storage]
    end

    subgraph "Data Warehouse"
        PG[(PostgreSQL)]
    end

    subgraph "Transformation & Viz"
        DBT[dbt Models]
        MB[Metabase Dashboards]
    end

    DB -->|Extraction| MI
    AF -.->|Orchestre| DB
    MI -->|Processing Spark| PG
    PG -->|Modélisation| DBT
    DBT --> PG
    PG --> MB
📸 Aperçu de la Solution⚙️ Orchestration & Monitoring (Apache Airflow)Visualisation du DAG de production assurant la synchronisation entre MySQL, MinIO et le Warehouse PostgreSQL.📊 Business Intelligence (Metabase)Dashboards interactifs permettant le pilotage des KPIs ventes, produits et performances par boutique.Vue d'ensemble (CA & Top Produits)Analyse Détaillée🛠️ Stack Technique & ExpertiseIngestion & Infras : Docker, Airflow, MinIO (S3-API).Processing : Python, Apache Spark (Lake-to-Warehouse).Data Modeling : dbt (Versioning SQL, tests de schémas, couches Bronze/Silver/Gold).Storage : PostgreSQL & MySQL.BI : Metabase (SQL interactif).🚀 Quick Start (Déploiement)Cloner le repository :Bashgit clone [https://github.com/yacoubadiallo/tassouma_bi.git](https://github.com/yacoubadiallo/tassouma_bi.git)
cd tassouma_bi
Lancer les services :Bashdocker-compose up -d
Points d'accès :| Service | URL | Rôle || :--- | :--- | :--- || Airflow | http://localhost:8080 | Orchestration & Logs || Metabase | http://localhost:3000 | Data Visualization || MinIO | http://localhost:9001 | Data Lake Storage |📁 Structure du Projet/dags : Workflows automatisés et scheduling./tassouma_dbt : Logique de transformation business (SQL versionné)./img : Captures d'écran et schémas techniques.ingestion_tassouma.py : Script d'extraction optimisé MySQL -> MinIO.lake_to_warehouse.py : Script de chargement structuré vers PostgreSQL.Contact : Yacouba Diallo | Ingénieur Big Data
