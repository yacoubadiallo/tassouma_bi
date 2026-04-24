Tassouma Sales Analytics | Modern Data Stack (ELT)

Pipeline de données haute performance conçu pour centraliser et analyser les flux de ventes multi-boutiques (Région AES). Cette solution automatise l'ingestion, le stockage en Data Lake, la modélisation en Warehouse et la restitution BI.

## Architecture & Stack Technique

L'infrastructure repose sur une architecture **cloud-native** entièrement conteneurisée :

- **Orchestration** : Apache Airflow (DAGs modulaires, monitoring des workflows).
- **Extraction (EL)** : Connecteurs Python personnalisés pour MySQL.
- **Data Lake** : MinIO (S3-Compatible) pour le stockage des objets bruts.
- **Data Warehouse** : PostgreSQL optimisé pour le requêtage analytique.
- **Transformation (T)** : **dbt** pour le versioning SQL, la modélisation en couches (Bronze/Silver/Gold) et les tests de qualité.
- **Analytics** : Metabase pour le dashboarding interactif et le pilotage des KPIs.

---

## Business Insights (Dashboard)

Le système fournit une visibilité temps réel sur les indicateurs clés de performance (KPIs) :
- **Revenue Monitoring** : Évolution mensuelle et annuelle du chiffre d'affaires.
- **Performance Géographique** : Analyse comparative par point de vente (Bamako, Niamey, Ouagadougou, etc.).
- **Product Analytics** : Top 15 des produits par contribution à la marge.

![Dashboard Overview](./stack/metabase/Capture%20d’écran%202026-04-24%20102305.png)

---

## Quick Start (Déploiement)

Le projet est entièrement piloté par Docker pour garantir la parité entre les environnements de développement et de production.

1. **Cloner le repository** :
   ```bash
   git clone [https://github.com/yacoubadiallo/tassouma_bi.git](https://github.com/yacoubadiallo/tassouma_bi.git)
   cd tassouma_bi
Lancer les services :

Bash
docker-compose up -d
Endpoints & Monitoring :
| Service | URL | Role |
| :--- | :--- | :--- |
| Airflow | http://localhost:8080 | Orchestration & Logs |
| Metabase | http://localhost:3000 | Data Visualization |
| MinIO | http://localhost:9001 | Data Lake Storage |

Caractéristiques Techniques
Modélisation dbt : Utilisation de modèles incrémentaux et de tests de contraintes (non-null, unique) pour garantir l'intégrité du Warehouse.

Scalabilité : Architecture prête pour le passage à Spark pour le traitement de volumes massifs (Big Data).

Isolation : Utilisation de réseaux Docker dédiés pour la communication inter-services.

Structure du Projet
/dags : Workflows automatisés (Scheduling & Ingestion).

/tassouma_dbt : Logique de transformation business (SQL versionné).

ingestion_tassouma.py : Script d'extraction optimisé.

lake_to_warehouse.py : Script de chargement structuré.

