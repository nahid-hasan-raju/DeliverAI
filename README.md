# QuikDel: A Novel & Scalable Q-learning Based Distributed Approach for Efficient Long-haul Delivery

**Master of Science in Computer Science Thesis Project**  
*Miami University, Oxford, OH - 2025*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-ongoing-grey.svg)]()

## Abstract

QuikDel introduces a novel distributed reinforcement learning framework that constructs a hierarchical, two-layer delivery graph from urban census and geographic data. Employing a Centralized Training and Decentralized Execution (CTDE) paradigm, QuikDel enables lightweight agents to make real-time routing decisions based on pre-trained Q-tables without online retraining overhead. Extensive experiments across Columbus, Chicago, Philadelphia, and New York demonstrate that QuikDel consistently reduces total travel distance by up to 13% compared to point-to-point baselines while maintaining competitive delivery success rates. The system reduces Q-table storage requirements by several orders of magnitude relative to fully connected reinforcement learning models, highlighting its scalability for large urban deployments.

## Table of Contents

- [Key Contributions](#key-contributions)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [QCense Data Extraction Tool](#qcense-data-extraction-tool)
- [Experimental Results](#experimental-results)
- [Research Artifacts](#research-artifacts)
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



## Research Artifacts

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
