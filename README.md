# CORD-19 Dask Distributed Analysis

A distributed analysis framework for processing the COVID-19 Open Research Dataset (CORD-19) using Dask distributed computing across multiple machines.

## Overview

This project implements a scalable distributed computing solution to analyze the massive CORD-19 dataset, which contains tens of thousands of scholarly articles about COVID-19, SARS-CoV-2, and related coronaviruses. The analysis leverages Dask's distributed computing capabilities to process the dataset efficiently across multiple machines connected via SSH.

## Dataset Information

**CORD-19 (COVID-19 Open Research Dataset)** is a growing resource of scientific papers on COVID-19 and related historical coronavirus research designed to facilitate the development of text mining and information retrieval systems. The dataset includes:

- **Metadata**: Paper titles, authors, publication venues, abstracts, and bibliographic information
- **Full-text JSON**: Structured full text parses of paper documents in S2ORC JSON format, preserving paragraph breaks, section headers, inline references, and citations
- **Multiple Sources**: Papers collected from various sources including PubMed, ArXiv, and other academic repositories
- **Scale**: 192,509 documents in the complete dataset

### Data Access

- **Kaggle Dataset**: [COVID-19 Open Research Dataset Challenge](https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge/data)
- **Official Source**: [Allen Institute for AI](https://allenai.org/data/cord-19)
- **AWS Open Data**: Available through the Registry of Open Data on AWS

## Project Features

### 1. Distributed Computing Infrastructure
- **SSH Cluster Setup**: Configured distributed Dask cluster across multiple machines using SSH connectivity
- **NFS Server**: Implemented Network File System for shared data access across cluster nodes
- **Scalable Architecture**: Designed to handle large-scale text processing tasks efficiently

### 2. Text Analysis Pipeline
- **MapReduce Word Count**: Implemented distributed word counting across all JSON files using MapReduce approach
- **Geographic Analysis**: Identified the most frequently represented countries in the research corpus
- **Institutional Analysis**: Analyzed the most prominent institutions contributing to COVID-19 research
- **Semantic Analysis**: Applied word embeddings to paper titles for similarity analysis using cosine similarity

### 3. Key Capabilities
- Distributed processing of large-scale scientific literature
- Efficient handling of JSON-structured academic papers
- Scalable text mining and information retrieval
- Geographic and institutional research trend analysis
- Semantic similarity analysis for research discovery

## Technical Architecture

### Infrastructure Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Scheduler     │    │   Worker Node   │    │   Worker Node   │
│   (Main Node)   │◄──►│      #1         │    │      #N         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   NFS Server    │
                    │ (Shared Storage)│
                    └─────────────────┘
```

### Distributed Computing Framework

The project uses **Dask** for distributed computing, which provides:

- **Dynamic Task Scheduling**: Intelligent task distribution across worker nodes
- **Fault Tolerance**: Automatic handling of node failures and task rescheduling
- **Memory Management**: Efficient handling of large datasets that don't fit in memory
- **Real-time Monitoring**: Dashboard for cluster performance monitoring

## Installation & Setup

### Prerequisites

```bash
# Core dependencies
pip install dask distributed
pip install numpy pandas scikit-learn
pip install nltk spacy  # For text processing
pip install gensim     # For word embeddings

# System requirements
# - SSH access to all cluster nodes
# - NFS server setup for shared storage
# - Python 3.7+ on all nodes
```

### SSH Cluster Configuration

```python
from dask.distributed import Client, SSHCluster

# Configure SSH cluster
cluster = SSHCluster(
    hosts=['scheduler-node', 'worker-node-1', 'worker-node-2', 'worker-node-N'],
    connect_options={'known_hosts': None},
    worker_options={'nthreads': 4, 'memory_limit': '8GB'},
    scheduler_options={'port': 8786, 'dashboard_address': ':8787'}
)

client = Client(cluster)
```

### NFS Setup

```bash
# On NFS server
sudo apt-get install nfs-kernel-server
sudo mkdir -p /shared/cord19
sudo chown nobody:nogroup /shared/cord19
sudo chmod 755 /shared/cord19

# Export configuration
echo "/shared/cord19 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
sudo systemctl restart nfs-kernel-server

# On client nodes
sudo apt-get install nfs-common
sudo mkdir -p /mnt/cord19
sudo mount -t nfs nfs-server:/shared/cord19 /mnt/cord19
```

## Usage Examples

### 1. Word Count Analysis

```python
import dask.bag as db
from dask.distributed import Client

# Connect to cluster
client = Client('scheduler-address:8786')

# Load and process JSON files
json_files = db.read_text('/mnt/cord19/document_parses/*.json')
word_counts = json_files.map_partitions(extract_words).frequencies()

# Compute results
top_words = word_counts.topk(1000)
print(top_words.compute())
```

### 2. Geographic Analysis

```python
def extract_countries(json_text):
    """Extract country information from paper metadata"""
    # Implementation for country extraction
    pass

countries = papers.map(extract_countries).frequencies()
top_countries = countries.topk(50).compute()
```

### 3. Institution Analysis

```python
def extract_institutions(json_text):
    """Extract institutional affiliations from papers"""
    # Implementation for institution extraction
    pass

institutions = papers.map(extract_institutions).frequencies()
top_institutions = institutions.topk(100).compute()
```

### 4. Semantic Similarity Analysis

```python
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

# Extract titles and create embeddings
titles = papers.map(lambda x: extract_title(x)).compute()
model = Word2Vec(titles, vector_size=100, window=5, min_count=1)

# Find similar papers
def find_similar_titles(query_title, model, titles, top_k=10):
    """Find most similar titles using cosine similarity"""
    # Implementation for similarity search
    pass
```

## Performance Optimization

### Cluster Scaling

```python
# Dynamic scaling based on workload
cluster.scale(10)  # Scale to 10 workers

# Adaptive scaling
cluster.adapt(minimum=2, maximum=20)
```

### Memory Management

```python
# Configure memory limits per worker
worker_options = {
    'memory_limit': '8GB',
    'nthreads': 4,
    'memory_target_fraction': 0.8,
    'memory_spill_fraction': 0.9
}
```

## Results & Insights

The analysis provides valuable insights into:

1. **Research Trends**: Most frequent terms and topics in COVID-19 literature
2. **Global Collaboration**: Geographic distribution of research contributions
3. **Institutional Impact**: Leading research institutions in COVID-19 studies
4. **Content Discovery**: Semantic similarity for finding related research papers

## Project Structure

```
cord19-dask-analysis/
├── src/
│   ├── cluster_setup.py      # SSH cluster configuration
│   ├── data_processing.py    # Core data processing functions
│   ├── analysis/
│   │   ├── word_count.py     # MapReduce word counting
│   │   ├── geographic.py     # Country analysis
│   │   ├── institutional.py  # Institution analysis
│   │   └── similarity.py     # Semantic similarity analysis
│   └── utils/
│       ├── nfs_utils.py      # NFS helper functions
│       └── json_parser.py    # JSON processing utilities
├── config/
│   ├── cluster_config.yaml   # Cluster configuration
│   └── analysis_config.yaml  # Analysis parameters
├── notebooks/
│   └── analysis_examples.ipynb
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Citation

If you use this project in your research, please cite:

```bibtex
@misc{cord19-dask-analysis,
  title={CORD-19 Dask Distributed Analysis},
  author={Your Name},
  year={2024},
  url={https://github.com/sleepy-byte/Cord19-Dask-Distributed-Analysis}
}
```

## Acknowledgments

- **Allen Institute for AI** for providing the CORD-19 dataset
- **Dask Development Team** for the distributed computing framework
- **COVID-19 Research Community** for open access to scientific literature

## References

- Wang, L. L., et al. (2020). CORD-19: The COVID-19 Open Research Dataset. *Proceedings of the 1st Workshop on NLP for COVID-19 at ACL 2020*.
- CORD-19 Dataset: https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge
- Dask Documentation: https://docs.dask.org/en/latest/

## Support

For questions and support:
- Create an issue in the GitHub repository
- Contact the maintainers
- Check the Dask community forums for distributed computing questions
