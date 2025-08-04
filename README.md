# fire-db
Fitness &amp; Evidence Repository Database(FIRE DB)

PubMed Fitness ETL with Relationship Extraction
This project implements a scalable ETL pipeline for ingesting, processing, and extracting structured knowledge from PubMed articles related to exercise modalities and fitness outcomes. It enriches biomedical abstracts with relationship triplets using a combination of SpaCy NLP and LLaMA 3 LLMs, and stores outputs in Delta Lake format using Apache Spark on Databricks.

Key features include:
Targeted Search: Extracts PubMed articles using MeSH terms related to physical fitness, exercise interventions, and training modalities.
Entity Extraction: Identifies known exercise types and outcome keywords using custom synonym maps.
Relationship Extraction: SpaCy-based pattern matching for fast, rule-based NLP parsing.
LLaMA 3 (70B) integration via Databricks Foundation Models API for semantic understanding and extraction of triplets.
Incremental Ingestion: Detects and loads only new records based on DOIs and last ETL run timestamp.
Delta Tables: Outputs are stored in two structured tables:
  - firedb_pubmed: Normalized publication metadata.
  - firedb_exercise_outcome_relationships: Extracted triplets (exercise modality → outcome).
Rich Metadata Logging: Tracks runtime statistics and ETL health in script_run_metadata.
Performance-aware Design: Built for lightweight serverless Databricks environments.

Project Structure

text pubmed_etl/ 

├── pubmed_etl.py # Main ETL driver 

├── modules/ │ 

├── meshmap.py # MeSH mapping tree + outcome keyword list 

│ └── pubmed_config.py # Central config 

├── firedb/ │ 

└── fire-db/ # Repos root 

├── pubmed_etl.log # Logging output 

└── README.md # You are here

Extracted Knowledge Format
Each PubMed article is transformed to include:
- Metadata: PMID, title, abstract, journal, MeSH terms, publication types, DOI, and sample size.
- Enriched Fields:
  - modalities: Exercise-related MeSH synonyms found in the abstract.
  - outcomes: Known fitness/clinical outcome terms matched.
  - relationships: List of structured triplets with:
  - exercise_modality
  - relationship_type (e.g., increases, decreases)
  - outcome
  - confidence_score (0.0–1.0)
  - source_sentence
  - extraction_method (spacy, llama, or spacy+llama)

Configuration
Defined in pubmed_config.py:

python
Copy
Edit
EMAIL = ""
INCREMENTAL = True               # Toggles full vs. incremental load
BATCH_SIZE = 500
TARGET_COUNT = 10000            # Articles to fetch per run

Sample Query Output:
Querying high-confidence relationships:

SELECT exercise_modality, relationship_type, outcome, confidence_score
FROM firedb_exercise_outcome_relationships
WHERE confidence_score > 0.8
ORDER BY confidence_score DESC
LIMIT 20;

Technologies Used:
Data Source:	PubMed (via NCBI Entrez + Biopython)
Orchestration:	PySpark on Databricks
Entity Extraction:	SpaCy (en_core_web_sm)
LLM Inference:	LLaMA 3 
Storage:	Delta Lake
Tracking:	MLflow, Spark Logging, Metadata Table

Development Notes
Designed for single-node Databricks environments.
Uses exponential backoff to gracefully handle PubMed rate limiting.
Configurable for full vs incremental loads depending on your data pipeline needs.
Relies on meshmap.py and outcome_keywords as primary domain ontologies.

Example ETL Run Summary
=== ETL COMPLETED ===
Status: SUCCESS
Total records: 9,872
New records: 489
Duration: 314.6 seconds

=== TOP CONFIDENCE RELATIONSHIPS ===
+---------------------+------------------+-------------------------+----------------+
|exercise_modality    |relationship_type |outcome                  |confidence_score|
+---------------------+------------------+-------------------------+----------------+
|Resistance Training  |improves          |Insulin Sensitivity      |0.95            |
|Aerobic Exercise     |reduces           |Systolic Blood Pressure  |0.92            |
+---------------------+------------------+-------------------------+----------------+

To Do / Future Enhancements
- Add unit and integration tests using pytest.
- Improve LLM prompting with few-shot examples.
- Add GUI/dashboard for real-time monitoring.
- Allow for user-specified MeSH filters via config or CLI.
- Integrate with additional datasets using Fuzzy Matching and semantic embeddings for relationship extrapolation

License
This project is for academic and research use only.

Author
Developed by Mike Andersen, leveraging scientific NLP and scalable data engineering for fitness informatics research.
