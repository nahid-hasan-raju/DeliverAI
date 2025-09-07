# QuikDel: A Novel & Scalable Q-learning Based Distributed Approach for Efficient Long-haul Delivery

**Master of Science in Computer Science Thesis Project**  
*Miami University, Oxford, OH - 2025*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-completed-brightgreen.svg)]()
[![Paper](https://img.shields.io/badge/paper-IEEE_TITS-blue)](docs/QuikDel_IEEE_TITS.pdf)

## Abstract

QuikDel introduces a novel distributed reinforcement learning framework that constructs a hierarchical, two-layer delivery graph from urban census and geographic data. Employing a Centralized Training and Decentralized Execution (CTDE) paradigm, QuikDel enables lightweight agents to make real-time routing decisions based on pre-trained Q-tables without online retraining overhead. Extensive experiments across Columbus, Chicago, Philadelphia, and New York demonstrate that QuikDel consistently reduces total travel distance by up to 13% compared to point-to-point baselines while maintaining competitive delivery success rates. The system reduces Q-table storage requirements by several orders of magnitude relative to fully connected reinforcement learning models, highlighting its scalability for large urban deployments.

## Table of Contents

- [Key Contributions](#key-contributions)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [QCense Data Extraction Tool](#qcense-data-extraction-tool)
- [Experimental Results](#experimental-results)
- [Repository Structure](#repository-structure)
- [Research Artifacts](#research-artifacts)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)

## Key Contributions

- **Hierarchical Network Architecture**: Two-layer system (hotspots → superspots) that reduces computational complexity from O(H³) to O(H_s³) where H_s ≈ H/r
- **CTDE Reinforcement Learning**: Centralized training with decentralized execution eliminates online retraining overhead
- **Dynamic Ride-Sharing**: Q-value based agent coordination enables path-sharing between deliveries
- **QCense Automation Tool**: Open-source tool for automated extraction of city-specific census and geographic data
- **Scalable Urban Deployment**: Successfully tested across cities with 278-2190 census tracts

### Performance Improvements

| Metric | Improvement vs Baseline |
|--------|------------------------|
| Total Distance | Up to 13% reduction |
| Q-table Storage | Orders of magnitude reduction |
| Scalability | Handles 13K+ deliveries/hour |
| Model Complexity | 627M → 377K parameters (Chicago) |

## System Architecture

QuikDel implements a multi-layered approach to urban delivery optimization:

### 1. Data Extraction Layer (QCense)
- Automated census tract identification for any U.S. city
- Consumer/producer location extraction from OpenStreetMap
- Real-time traffic data integration via GraphHopper

### 2. Network Construction Layer
- **Hotspot Placement**: One hotspot per census tract at consumer/producer centroid
- **Superspot Selection**: SES (Superspot Eligibility Score) with spacing-aware algorithm
- **Hierarchical Clustering**: Balanced grouping with configurable ratios (1:5, 1:10, 1:15, etc.)

### 3. Learning Layer
- **Q-Learning Agents**: Separate agents for hotspot and superspot navigation
- **Multi-MDP Decomposition**: Hotspot-level (MDP_h) and Superspot-level (MDP_s) policies
- **Boltzmann Exploration**: Temperature-based action selection during training

### 4. Execution Layer
- **Decentralized Routing**: Local Q-table fragments for autonomous decision-making
- **Dynamic Ride-Sharing**: PAS (Preferred Action Set) intersection for path coordination
- **Request Handling**: Priority queue system for ride-sharing approval/rejection

## Installation

### Prerequisites

```bash
# System requirements
Python 3.8+
Git
GDAL library (for geospatial operations)
```

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/quikdel.git
cd quikdel

# Create virtual environment
python -m venv quikdel-env
source quikdel-env/bin/activate  # On Windows: quikdel-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install GDAL (platform specific)
# Ubuntu/Debian: sudo apt-get install gdal-bin python3-gdal
# macOS: brew install gdal
# Windows: conda install -c conda-forge gdal

# Setup QCense
cd qcense
pip install -e .
cd ..

# Verify installation
python -m pytest tests/
```

## Usage

### Quick Start: Running a Complete Simulation

```bash
# Generate city data and run simulation for Columbus
python scripts/run_complete_simulation.py \
    --city "Columbus" \
    --state "Ohio" \
    --ratio 10 \
    --deliveries 300 \
    --output results/columbus_1_10/

# View results
python scripts/analyze_results.py results/columbus_1_10/simulation_results.json
```

### Step-by-Step Process

#### 1. Extract City Data with QCense

```bash
# Extract census tracts and locations for any U.S. city
python qcense/extract_city_data.py \
    --state "Ohio" \
    --city "Columbus" \
    --output data/columbus/

# This generates:
# - census_tracts.geojson
# - producers.json  
# - consumers.json
# - distance_matrix.json
```

#### 2. Generate Network Architecture

```bash
# Create hotspot placement and superspot selection
python src/network_construction/build_network.py \
    --data_dir data/columbus/ \
    --ratio 10 \
    --min_children 4 \
    --output networks/columbus_1_10/

# Visualize network structure
python src/visualization/plot_network.py \
    --network networks/columbus_1_10/ \
    --save_path figures/columbus_network.png
```

#### 3. Train Q-Learning Agents

```bash
# Train agents for all hotspots and superspots
python src/training/train_agents.py \
    --network networks/columbus_1_10/ \
    --episodes 10000 \
    --alpha 0.1 \
    --gamma 0.99 \
    --output models/columbus_1_10/

# Monitor training progress
tensorboard --logdir logs/training/
```

#### 4. Run Delivery Simulation

```bash
# Execute delivery simulation with trained agents
python src/simulation/run_simulation.py \
    --network networks/columbus_1_10/ \
    --agents models/columbus_1_10/ \
    --deliveries 300 \
    --time_window 60 \
    --ride_share_threshold 0.44 \
    --output results/columbus_1_10/
```

#### 5. Generate Baselines and Analysis

```bash
# Run point-to-point baseline
python src/baselines/run_p2p_baseline.py \
    --network networks/columbus_1_10/ \
    --deliveries 300 \
    --output results/columbus_1_10/p2p_baseline/

# Run ablation study (no ride-sharing)
python src/baselines/run_ablation_study.py \
    --network networks/columbus_1_10/ \
    --agents models/columbus_1_10/ \
    --deliveries 300 \
    --output results/columbus_1_10/ablation/

# Compare all methods
python src/analysis/comparative_analysis.py \
    --quikdel results/columbus_1_10/ \
    --p2p results/columbus_1_10/p2p_baseline/ \
    --ablation results/columbus_1_10/ablation/ \
    --output reports/columbus_comparison.html
```

### Configuration Files

```yaml
# config/columbus_default.yaml
city:
  name: "Columbus"
  state: "Ohio"
  
network:
  ratio: 10
  min_children: 4
  spacing_threshold: 1.0
  
training:
  episodes: 10000
  alpha: 0.1
  gamma: 0.99
  temperature_init: 1000
  decay_rate: 0.2
  
simulation:
  deliveries: 300
  time_multiplier: 1.5
  ride_share_threshold: 0.44
  bimodal_peaks: [15, 45]
```

## QCense Data Extraction Tool

QCense is our open-source tool for automated city data extraction:

### Features
- **Automated Census Tract Identification**: No manual boundary definition needed
- **Multi-source Data Integration**: Census Bureau + OpenStreetMap + GraphHopper
- **High Accuracy**: 96.03% F1-score validation against Chicago official data
- **GeoJSON Output**: Compatible with all major GIS tools

### Validation Results
- **Recall**: 99.75% (captures nearly all relevant tracts)
- **Precision**: 92.58% (modest over-selection prevents gaps)
- **Accuracy**: 92.37% (close overall correspondence)

### Usage Example

```python
from qcense import CityDataExtractor

# Initialize extractor
extractor = CityDataExtractor()

# Extract comprehensive city data
city_data = extractor.extract_city_data(
    state="Pennsylvania",
    city="Philadelphia"
)

# Access extracted components
census_tracts = city_data.census_tracts
producers = city_data.producers      # 1,055 locations
consumers = city_data.consumers      # 18,342 locations
distance_matrix = city_data.distances
```

## Experimental Results

### Cities Tested
- **Columbus, OH**: 278 census tracts
- **Philadelphia, PA**: 423 census tracts  
- **Chicago, IL**: 863 census tracts
- **New York City, NY**: 2,190 census tracts

### Performance Summary

| City | Best Ratio | Distance Reduction | Success Rate | Avg. Time Increase |
|------|------------|-------------------|--------------|-------------------|
| Columbus | 1:15 | 1.01% | 96% | 199s |
| Philadelphia | 1:10 | 6.94% | 92% | 444s |
| Chicago | 1:10 | 8.02% | 94% | 428s |
| NYC | 1:10 | 5.14% | 93% | 553s |

### Scalability Analysis

| Model | Columbus (278 tracts) | Chicago (863 tracts) | NYC (2,190 tracts) |
|-------|----------------------|---------------------|-------------------|
| DeliverAI | 21.4M parameters | 627.7M parameters | Infeasible |
| QuikDel | 25.8K parameters | 377.5K parameters | 2.4M parameters |
| **Reduction** | **829x smaller** | **1,663x smaller** | **>1000x smaller** |

## Repository Structure

```
quikdel/
│
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── setup.py                    # Package setup
├── LICENSE                     # MIT License
├── .gitignore                  # Python + data files
│
├── qcense/                     # QCense data extraction tool
│   ├── __init__.py
│   ├── extract_city_data.py    # Main extraction script
│   ├── census_utils.py         # Census API utilities
│   ├── osm_utils.py           # OpenStreetMap queries
│   ├── routing_utils.py       # GraphHopper integration
│   ├── validation.py          # Data validation tools
│   └── setup.py               # QCense package setup
│
├── src/                        # Core QuikDel implementation
│   ├── __init__.py
│   ├── network_construction/   # Hotspot/Superspot algorithms
│   │   ├── hotspot_placement.py
│   │   ├── superspot_selection.py
│   │   ├── clustering.py
│   │   └── ses_scoring.py
│   ├── training/              # Q-learning implementation
│   │   ├── q_learning.py
│   │   ├── mdp_formulation.py
│   │   ├── agent_training.py
│   │   └── boltzmann_exploration.py
│   ├── simulation/            # Delivery simulation engine
│   │   ├── delivery_engine.py
│   │   ├── ride_sharing.py
│   │   ├── agent_interaction.py
│   │   └── request_handler.py
│   ├── baselines/             # Baseline implementations
│   │   ├── point_to_point.py
│   │   ├── ablation_study.py
│   │   └── deliverAI_comparison.py
│   ├── utils/                 # Utility functions
│   │   ├── graph_utils.py
│   │   ├── distance_utils.py
│   │   ├── time_utils.py
│   │   └── visualization_utils.py
│   └── analysis/              # Results analysis
│       ├── metrics.py
│       ├── statistical_tests.py
│       └── comparative_analysis.py
│
├── data/                      # City datasets
│   ├── columbus/
│   ├── philadelphia/
│   ├── chicago/
│   └── new_york/
│
├── networks/                  # Generated network structures
│   ├── columbus_1_5/
│   ├── columbus_1_10/
│   ├── columbus_1_15/
│   └── ...
│
├── models/                    # Trained Q-tables
│   ├── columbus_1_10/
│   │   ├── hotspot_agents/
│   │   └── superspot_agents/
│   └── ...
│
├── results/                   # Simulation outputs
│   ├── columbus_1_10/
│   │   ├── simulation_results.json
│   │   ├── performance_metrics.json
│   │   └── delivery_paths.json
│   └── ...
│
├── config/                    # Configuration files
│   ├── default.yaml
│   ├── columbus.yaml
│   ├── philadelphia.yaml
│   └── parameter_tuning/
│
├── scripts/                   # Automation scripts
│   ├── run_complete_simulation.py
│   ├── batch_experiments.py
│   ├── parameter_sweep.py
│   └── generate_paper_figures.py
│
├── tests/                     # Unit tests
│   ├── test_qcense.py
│   ├── test_network_construction.py
│   ├── test_training.py
│   └── test_simulation.py
│
├── notebooks/                 # Jupyter analysis notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_network_analysis.ipynb
│   ├── 03_training_visualization.ipynb
│   ├── 04_results_analysis.ipynb
│   └── 05_paper_figures.ipynb
│
├── docs/                     # Documentation
│   ├── QuikDel_IEEE_TITS.pdf # Published paper
│   ├── thesis_defense.pdf    # Defense presentation
│   ├── api_reference.md      # Code documentation
│   ├── tutorial.md           # Getting started guide
│   ├── architecture.md       # System design details
│   └── supplementary/        # Additional materials
│       ├── complexity_analysis.md
│       ├── parameter_tuning.md
│       └── city_comparisons.md
│
├── figures/                  # Generated plots and visualizations
│   ├── network_structures/
│   ├── training_curves/
│   ├── performance_comparisons/
│   └── paper_figures/
│
└── logs/                     # Training and execution logs
    ├── training/
    ├── simulation/
    └── experiments/
```

## Research Artifacts

### Published Materials
- **IEEE TITS Paper**: [QuikDel_IEEE_TITS.pdf](docs/QuikDel_IEEE_TITS.pdf)
- **Thesis Defense**: [Defense Presentation](docs/thesis_defense.pdf)
- **Supplementary Materials**: [Additional Analysis](docs/supplementary/)

### Reproducible Experiments
All experiments from the paper can be reproduced using:

```bash
# Run all paper experiments
python scripts/reproduce_paper_results.py

# Generate all paper figures  
python scripts/generate_paper_figures.py

# Run parameter sensitivity analysis
python scripts/parameter_sweep.py --city all --ratios 5,10,15,20,30,40
```

### Key Algorithms Implemented

1. **Superspot Selection Algorithm** 
2. **Q-Learning Agent Training**  


## Acknowledgments

**Thesis Committee:**
- **Primary Advisor**: [Dr. Vaskar Raychoudhury](mailto:raychov@miamioh.edu) - Miami University

**Collaborators:**
- **Md Nahid Hasan** - Data Processing, Simulation , Experimental Validation  
- **Robert Kilgore** - Developer, Network Architecture, QCense Development
- **Yusuf Ozdemir** - Simulation Engine 
- **Ashman Mehra** - Algorithm Design, Performance Analysis


**Funding & Resources:**
- Department of Computer Science & Software Engineering, Miami University
- GraphHopper API for routing data
- U.S. Census Bureau and OpenStreetMap for geographic data
---

**Project Status**: Ongoing  
**Thesis Defense**: Estimated by May 2026 
**Degree Conferred**: Master of Science in Computer Science - Miami University

**Contact**: [Md Nahid Hasan](mailto:nahidhasanraju1999@gmail.com) | [LinkedIn](https://linkedin.com/in/nahid-hasan-raju/) | [Portfolio site](nahid-hasan-raju.github.io)
