# FIRE-DB: Fitness & Evidence Repository Database

> A Generative AI-Enabled Data Product for Fitness, Exercise, and Supplement Ranking and Lifestyle Planning

---

## Project Overview

FIRE-DB implements a scalable ETL pipeline that extracts, processes, and structures biomedical knowledge from PubMed literature related to exercise modalities and fitness outcomes. The system combines natural language processing with large language models to automatically identify and extract relationships between exercise interventions and their physiological outcomes, creating a queryable knowledge base for evidence-based fitness research.

By integrating SpaCy NLP with LLaMA 3 (70B) via the Databricks Foundation Models API, FIRE-DB transforms unstructured scientific abstracts into structured relationship triplets that link specific exercise modalities to measurable health and fitness outcomes with associated confidence scores.

---

## Research Motivation

The fitness and exercise science literature contains decades of rigorous research on the relationships between specific training modalities and health outcomes. However, this knowledge is scattered across thousands of publications, making it difficult for researchers, clinicians, and fitness professionals to:

- Identify which exercise interventions produce specific outcomes
- Compare the strength of evidence across different training modalities
- Make evidence-based recommendations for training program design
- Track emerging research trends in exercise physiology

FIRE-DB addresses these challenges by creating a structured, queryable database that makes this knowledge accessible and actionable.

---

## System Architecture

### Data Flow Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    DATA ACQUISITION LAYER                        │
│                                                                  │
│  PubMed/NCBI Entrez API                                         │
│    → Query with MeSH terms (exercise, fitness, training)        │
│    → Retrieve article metadata and abstracts                    │
│    → Apply filters (publication types, date ranges)             │
└────────────────────────────┬─────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────────┐
│                   EXTRACTION & ENRICHMENT LAYER                  │
│                                                                  │
│  SpaCy NLP Pipeline (en_core_web_sm)                            │
│    → Named entity recognition                                   │
│    → Dependency parsing for relationship extraction             │
│    → Pattern matching for exercise modalities                   │
│                                                                  │
│  LLaMA 3 (70B) - Databricks Foundation Models                   │
│    → Semantic understanding of exercise-outcome relationships   │
│    → Confidence scoring for extracted triplets                  │
│    → Relationship type classification                           │
│                                                                  │
│  Hybrid Approach (SpaCy + LLaMA)                                │
│    → Combines rule-based and LLM extraction                     │
│    → Cross-validation of relationships                          │
│    → Enhanced confidence scoring                                │
└────────────────────────────┬─────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────────┐
│                    TRANSFORMATION LAYER                          │
│                                                                  │
│  Apache Spark (PySpark) on Databricks                           │
│    → Distributed processing of article batches                  │
│    → Parallel entity extraction across abstracts                │
│    → Deduplication and normalization                            │
│    → Metadata enrichment and validation                         │
└────────────────────────────┬─────────────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                               │
│                                                                  │
│  Delta Lake Format                                              │
│    → firedb_pubmed: Normalized publication metadata            │
│    → firedb_exercise_outcome_relationships: Extracted triplets  │
│    → ACID transactions for data consistency                     │
│    → Time travel for versioning                                 │
└────────────────────────────┬─────────────────────────────────────┘
                             ↓
                   QUERY & ANALYTICS LAYER
                   (SQL, Spark DataFrames, MLflow)
```

---

## Core Features

### Targeted Literature Search

**MeSH Term-Based Querying**:
- Utilizes Medical Subject Headings (MeSH) vocabulary for precise literature retrieval
- Focuses on terms related to physical fitness, exercise interventions, and training modalities
- Configurable search strategies defined in `meshmap.py`
- Supports both broad and specific exercise modality searches

**Search Optimization**:
- Implements exponential backoff to handle PubMed API rate limiting gracefully
- Configurable batch sizes for efficient data retrieval
- Target article counts adjustable via configuration
- Incremental loading capability to avoid re-processing existing articles

### Relationship Extraction

**Triple Extraction Format**:
Each identified relationship is structured as:
- **exercise_modality**: Specific training type (e.g., "Resistance Training", "High-Intensity Interval Training")
- **relationship_type**: Nature of the relationship (e.g., "increases", "decreases", "improves", "reduces")
- **outcome**: Measured physiological or fitness outcome (e.g., "VO2 Max", "Insulin Sensitivity", "Muscle Strength")
- **confidence_score**: Probability score (0.0-1.0) indicating extraction certainty
- **source_sentence**: Original text supporting the relationship
- **extraction_method**: Methodology used ("spacy", "llama", "spacy+llama")

**Multi-Method Extraction Strategy**:

1. **SpaCy NLP Extraction**:
   - Rule-based pattern matching for common relationship structures
   - Fast processing for high-throughput scenarios
   - Deterministic results for reproducibility

2. **LLaMA 3 LLM Extraction**:
   - Semantic understanding of complex sentence structures
   - Handles nuanced language and contextual relationships
   - Higher accuracy for ambiguous cases

3. **Hybrid Approach**:
   - Combines strengths of both methods
   - Cross-validation increases confidence scores
   - Reduces false positives through consensus

### Data Enrichment

Each PubMed article is transformed to include:

**Publication Metadata**:
- PMID (PubMed Identifier)
- Title and abstract text
- Journal name and publication date
- MeSH terms assigned by NCBI indexers
- Publication types (Clinical Trial, Review, Meta-Analysis, etc.)
- DOI for citation tracking
- Sample size (when reported)

**Extracted Knowledge Fields**:
- **modalities**: List of exercise-related MeSH synonyms identified in abstract
- **outcomes**: Known fitness and clinical outcome terms matched from ontology
- **relationships**: Complete set of extracted triplets with metadata

---

## Technical Implementation

### Project Structure

```
fire-db/
├── pubmed_etl/
│   ├── pubmed_etl.py              # Main ETL orchestration script
│   └── modules/
│       ├── meshmap.py             # MeSH term hierarchy and mappings
│       └── pubmed_config.py       # Central configuration parameters
├── firedb/                         # Output data directory (Delta tables)
├── pubmed_etl.log                 # Execution logs
└── README.md                       # Project documentation
```

### Module Descriptions

#### `pubmed_etl.py`

**Purpose**: Main ETL driver coordinating all pipeline stages

**Key Functions**:
- Orchestrates PubMed API queries using Biopython's Entrez interface
- Manages batch processing of articles for scalability
- Coordinates SpaCy and LLaMA extraction workflows
- Implements error handling and retry logic
- Writes processed data to Delta Lake tables
- Tracks pipeline metrics and logging

**Integration Role**: Central orchestrator that invokes modules for extraction, transformation, and loading. Manages the complete data flow from PubMed API to Delta Lake storage.

#### `modules/meshmap.py`

**Purpose**: Domain ontology and vocabulary management

**Key Components**:
- **MeSH Term Hierarchy**: Structured tree of exercise-related medical subject headings
- **Synonym Mappings**: Alternative terms for exercise modalities (e.g., "aerobic exercise", "cardio", "endurance training")
- **Outcome Keyword List**: Curated vocabulary of fitness and clinical outcomes
- **Relationship Type Taxonomy**: Standardized verbs describing exercise-outcome relationships

**Integration Role**: Provides controlled vocabularies used by extraction algorithms to identify relevant terms in abstracts. Acts as the domain knowledge layer that ensures consistent terminology across the database.

#### `modules/pubmed_config.py`

**Purpose**: Centralized configuration management

**Configuration Parameters**:
```python
EMAIL = ""                    # NCBI requires email for API access
INCREMENTAL = True            # Toggle between full and incremental loads
BATCH_SIZE = 500              # Articles processed per batch
TARGET_COUNT = 10000          # Articles to retrieve per execution
```

**Additional Configuration**:
- PubMed API rate limits and retry settings
- SpaCy model specifications
- LLaMA API endpoints and authentication
- Delta Lake table paths and schemas
- Logging levels and output formats

**Integration Role**: Single source of truth for pipeline behavior. Enables easy adjustment of processing parameters without code modifications.

---

## Data Model

### Table: `firedb_pubmed`

**Purpose**: Normalized storage of PubMed article metadata

| Column | Type | Description |
|--------|------|-------------|
| pmid | STRING (Primary Key) | PubMed unique identifier |
| title | STRING | Article title |
| abstract | STRING | Full abstract text |
| journal | STRING | Publication venue |
| publication_date | DATE | Date of publication |
| mesh_terms | ARRAY<STRING> | MeSH terms assigned by indexers |
| publication_types | ARRAY<STRING> | Article classification types |
| doi | STRING | Digital Object Identifier |
| sample_size | INTEGER | Study sample size (when reported) |
| modalities | ARRAY<STRING> | Exercise modalities identified in abstract |
| outcomes | ARRAY<STRING> | Fitness outcomes identified in abstract |
| etl_timestamp | TIMESTAMP | When record was processed |

### Table: `firedb_exercise_outcome_relationships`

**Purpose**: Structured relationship triplets with confidence scores

| Column | Type | Description |
|--------|------|-------------|
| relationship_id | STRING (Primary Key) | Unique identifier for relationship |
| pmid | STRING (Foreign Key) | Links to source article |
| exercise_modality | STRING | Specific training intervention |
| relationship_type | STRING | Nature of relationship (increases, decreases, etc.) |
| outcome | STRING | Measured fitness or health outcome |
| confidence_score | FLOAT | Extraction confidence (0.0-1.0) |
| source_sentence | STRING | Original text supporting relationship |
| extraction_method | STRING | Method used (spacy, llama, spacy+llama) |
| etl_timestamp | TIMESTAMP | When relationship was extracted |

---

## Configuration and Execution

### Environment Setup

**Prerequisites**:
- Databricks workspace with access to Foundation Models API
- Python 3.8+
- Apache Spark configured on Databricks
- NCBI E-utilities API access (free registration)

**Required Libraries**:
- `biopython`: PubMed API interaction
- `spacy`: NLP processing
- `pyspark`: Distributed data processing
- `delta-spark`: Delta Lake integration
- `mlflow`: Experiment tracking

### Configuration Parameters

**In `pubmed_config.py`**:

```python
# NCBI API Configuration
EMAIL = "your.email@domain.com"  # Required by NCBI

# Pipeline Behavior
INCREMENTAL = True    # True: Only process new articles
                      # False: Full reprocessing of all articles

# Processing Parameters
BATCH_SIZE = 500      # Articles per processing batch
                      # Larger batches = better throughput
                      # Smaller batches = better fault tolerance

TARGET_COUNT = 10000  # Articles to fetch per execution
                      # Adjust based on compute resources
```

### Execution

**Standard Run**:
```bash
python pubmed_etl/pubmed_etl.py
```

**Full Refresh**:
```python
# In pubmed_config.py, set:
INCREMENTAL = False
```

**Custom Target Count**:
```python
# In pubmed_config.py, adjust:
TARGET_COUNT = 50000  # For larger data pulls
```

---

## Sample Queries and Use Cases

### Query 1: High-Confidence Exercise-Outcome Relationships

**Use Case**: A fitness professional wants evidence-based recommendations for improving cardiovascular health.

**Query**:
```sql
SELECT 
    exercise_modality, 
    relationship_type, 
    outcome, 
    confidence_score,
    COUNT(*) as evidence_count
FROM firedb_exercise_outcome_relationships
WHERE confidence_score > 0.8
    AND outcome LIKE '%cardiovascular%'
GROUP BY exercise_modality, relationship_type, outcome, confidence_score
ORDER BY confidence_score DESC, evidence_count DESC
LIMIT 20;
```

**Expected Output**:
```
+---------------------+------------------+-------------------------+----------------+---------------+
|exercise_modality    |relationship_type |outcome                  |confidence_score|evidence_count |
+---------------------+------------------+-------------------------+----------------+---------------+
|Aerobic Exercise     |reduces           |Systolic Blood Pressure  |0.92            |47             |
|HIIT                 |improves          |VO2 Max                  |0.90            |31             |
|Resistance Training  |improves          |Insulin Sensitivity      |0.95            |28             |
+---------------------+------------------+-------------------------+----------------+---------------+
```

### Query 2: Evidence for Specific Training Modality

**Use Case**: A researcher investigating the effects of resistance training on metabolic health.

**Query**:
```sql
SELECT 
    outcome,
    relationship_type,
    AVG(confidence_score) as avg_confidence,
    COUNT(*) as study_count,
    COLLECT_LIST(pmid) as supporting_studies
FROM firedb_exercise_outcome_relationships
WHERE exercise_modality = 'Resistance Training'
    AND (outcome LIKE '%glucose%' 
         OR outcome LIKE '%insulin%' 
         OR outcome LIKE '%metabolic%')
GROUP BY outcome, relationship_type
HAVING COUNT(*) >= 3
ORDER BY avg_confidence DESC;
```

### Query 3: Extraction Method Comparison

**Use Case**: Evaluating the performance of different extraction methods.

**Query**:
```sql
SELECT 
    extraction_method,
    COUNT(*) as total_relationships,
    AVG(confidence_score) as avg_confidence,
    MIN(confidence_score) as min_confidence,
    MAX(confidence_score) as max_confidence
FROM firedb_exercise_outcome_relationships
GROUP BY extraction_method
ORDER BY avg_confidence DESC;
```

### Query 4: Publication Trend Analysis

**Use Case**: Understanding research trends in exercise science over time.

**Query**:
```sql
SELECT 
    YEAR(p.publication_date) as year,
    r.exercise_modality,
    COUNT(DISTINCT r.pmid) as article_count,
    COUNT(*) as relationship_count
FROM firedb_pubmed p
JOIN firedb_exercise_outcome_relationships r ON p.pmid = r.pmid
WHERE YEAR(p.publication_date) >= 2015
GROUP BY YEAR(p.publication_date), r.exercise_modality
ORDER BY year DESC, article_count DESC;
```

### Query 5: Conflicting Evidence Detection

**Use Case**: Identifying exercise-outcome pairs with conflicting evidence.

**Query**:
```sql
SELECT 
    exercise_modality,
    outcome,
    COUNT(DISTINCT relationship_type) as different_relationships,
    COLLECT_SET(relationship_type) as relationship_types,
    AVG(confidence_score) as avg_confidence
FROM firedb_exercise_outcome_relationships
GROUP BY exercise_modality, outcome
HAVING COUNT(DISTINCT relationship_type) > 1
ORDER BY different_relationships DESC, avg_confidence DESC;
```

---

## Pipeline Performance and Monitoring

### Typical Execution Metrics

```
=== ETL COMPLETED ===
Status: SUCCESS
Total records: 9,872
New records: 489
Duration: 314.6 seconds
Processing rate: ~31 articles/second

=== TOP CONFIDENCE RELATIONSHIPS ===
+---------------------+------------------+-------------------------+----------------+
|exercise_modality    |relationship_type |outcome                  |confidence_score|
+---------------------+------------------+-------------------------+----------------+
|Resistance Training  |improves          |Insulin Sensitivity      |0.95            |
|Aerobic Exercise     |reduces           |Systolic Blood Pressure  |0.92            |
|HIIT                 |increases         |VO2 Max                  |0.90            |
+---------------------+------------------+-------------------------+----------------+
```

### Monitoring Capabilities

**Logging**:
- Execution logs written to `pubmed_etl.log`
- Timestamped entries for all pipeline stages
- Error tracking with stack traces
- Performance metrics per batch

**MLflow Integration**:
- Experiment tracking for extraction runs
- Parameter logging (batch sizes, target counts)
- Metric tracking (articles processed, relationships extracted)
- Artifact storage (extracted relationship samples)

**Spark Monitoring**:
- Native Spark UI for job tracking
- Stage-level performance metrics
- Resource utilization monitoring
- Task failure analysis

---

## System Design Considerations

### Scalability

**Current Architecture**:
- Designed for single-node Databricks environments
- Batch processing enables horizontal scaling potential
- Delta Lake supports concurrent reads/writes

**Scaling Strategies**:
- Increase `BATCH_SIZE` for higher throughput
- Deploy on multi-node Spark clusters for parallel processing
- Implement distributed LLM inference for faster extraction
- Partition Delta tables by publication year for query optimization

### Fault Tolerance

**Implemented Safeguards**:
- Exponential backoff for PubMed API rate limiting
- Incremental loading prevents data loss on failures
- Delta Lake ACID transactions ensure consistency
- Comprehensive error logging for debugging

**Recovery Mechanisms**:
- Checkpoint system tracks processed articles
- Failed batches can be re-run independently
- Delta table versioning enables rollback if needed

### Data Quality

**Quality Assurance**:
- Confidence scoring for all extracted relationships
- Source sentence preservation for manual validation
- Multi-method extraction for cross-validation
- MeSH term validation against NCBI ontology

**Validation Queries**:
```sql
-- Check for low-confidence extractions
SELECT COUNT(*) FROM firedb_exercise_outcome_relationships
WHERE confidence_score < 0.5;

-- Identify missing metadata
SELECT COUNT(*) FROM firedb_pubmed
WHERE abstract IS NULL OR mesh_terms IS NULL;
```

---

## Future Enhancements

### Planned Features

**Testing Infrastructure**:
- Unit tests for extraction functions (pytest framework)
- Integration tests for end-to-end pipeline validation
- Regression tests for relationship extraction accuracy
- Performance benchmarking suite

**Improved Extraction**:
- Few-shot prompting for LLaMA 3 to improve accuracy
- Fine-tuning SpaCy models on exercise science corpus
- Multi-sentence relationship detection
- Temporal relationship extraction (short-term vs long-term effects)

**User Interface**:
- Real-time monitoring dashboard for pipeline execution
- Interactive query builder for non-technical users
- Visualization of exercise-outcome relationship networks
- Evidence summary generation for specific queries

**Enhanced Configurability**:
- CLI interface for dynamic MeSH term filtering
- User-specified outcome ontologies
- Custom confidence threshold adjustments
- Export formats (JSON, CSV, RDF)

**Dataset Integration**:
- WGER exercise database integration
- Web of Science literature expansion
- Clinical trial registries (ClinicalTrials.gov)
- Fuzzy matching for cross-database entity linking
- Semantic embeddings for relationship extrapolation across datasets

---

## Technical Stack

**Data Engineering**:
- Apache Spark (PySpark) - Distributed processing
- Delta Lake - Storage layer with ACID guarantees
- Databricks - Cloud platform and orchestration

**NLP & Machine Learning**:
- SpaCy (en_core_web_sm) - Entity extraction and NLP
- LLaMA 3 (70B) - Large language model via Databricks Foundation Models API
- MLflow - Experiment tracking and model management

**Data Sources**:
- PubMed/NCBI Entrez - Biomedical literature
- Biopython - PubMed API client library
- MeSH - Medical Subject Headings ontology

**Development Tools**:
- Python 3.8+
- Git version control
- Jupyter notebooks for exploratory analysis

---

## Usage Restrictions

This project is intended for **academic and research use only**. The data extracted from PubMed is subject to NCBI's terms of service. Any commercial applications require appropriate licensing and compliance with PubMed redistribution policies.

---

## License

MIT License

Copyright (c) 2025 Mike Andersen

---

## Contact

**Developer**: Mike Andersen

For questions, collaboration opportunities, or data access requests:

**Email**: mikeandersen622@gmail.com
**GitHub**: https://github.com/salamandersen93  

---

## Acknowledgements

**Data Sources**:
- National Library of Medicine (NLM) / National Center for Biotechnology Information (NCBI)
- PubMed database of biomedical literature
- Medical Subject Headings (MeSH) vocabulary

**Technology Providers**:
- Databricks for cloud platform and Foundation Models API
- Meta AI for LLaMA 3 language model
- Explosion AI for SpaCy NLP library
