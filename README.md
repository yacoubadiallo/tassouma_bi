# Tassouma Sales Analytics | Modern Data Stack (ELT)

**Yacouba DIALLO — INGÉNIEUR BIG DATA**

Pipeline de données haute performance conçu pour centraliser et analyser les flux de ventes multi-boutiques (Région AES). Cette solution automatise l'ingestion, le stockage en Data Lake, la modélisation en Warehouse et la restitution BI.

---

## Architecture du Pipeline

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
````
Aperçu de la Solution

Business Intelligence 
(Metabase) Dashboards interactifs permettant le pilotage des KPIs ventes, produits et performances par boutique.


Stack Technique & Expertise

Ingestion & Infras : Docker, Airflow, MinIO (S3-API).

Processing : Python, Apache Spark (Lake-to-Warehouse).

Data Modeling : dbt (Versioning SQL, tests de schémas, couches Bronze/Silver/Gold).

Storage : PostgreSQL & MySQL.BI : Metabase (SQL interactif).

Quick Start (Déploiement)

Cloner le repository :

Bash
git clone [https://github.com/yacoubadiallo/tassouma_bi.git](https://github.com/yacoubadiallo/tassouma_bi.git)

cd tassouma_bi

Lancer les services :Bash
docker-compose up -d


Contact : Yacouba Diallo | Ingénieur Big Data
