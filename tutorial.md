# QuikDel Tutorial: Complete Walkthrough

This tutorial walks you through using QuikDel to optimize food delivery routes in any U.S. city using distributed Q-learning and hierarchical network construction.

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- GDAL library installed system-wide
- At least 4GB RAM for medium cities (Columbus, Philadelphia)
- 8GB+ RAM recommended for large cities (Chicago, NYC)

## Installation

### 1. System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev python3-gdal
```

**macOS:**
```bash
brew install gdal
```

**Windows:**
```bash
# Using conda (recommended)
conda install -c conda-forge gdal
```

### 2. QuikDel Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/quikdel.git
cd quikdel

# Create virtual environment
python -m venv quikdel-env
source quikdel-env/bin/activate  # Windows: quikdel-env\Scripts\activate

# Install QuikDel
pip install -e .
```

## Quick Start (5 minutes)

Run QuikDel on Columbus, Ohio with default settings:

```bash
python scripts/quick_start.py --city Columbus --state Ohio
```

This command will:
1. Extract Columbus census and business data
2. Build a hierarchical delivery network
3. Train Q-learning agents
4. Run delivery simulations
5. Compare against baselines

## Step-by-Step Tutorial

### Step 1: Data Extraction with QCense

QCense automatically extracts census tracts, producer/consumer locations, and routing data for any U.S. city.

```python
from qcense import CityDataExtractor

# Initialize extractor
extractor = CityDataExtractor()

# Extract data for your city
city_data = extractor.extract_city_data(
    state="Pennsylvania", 
    city="Philadelphia"
)

print(f"Extracted {len(city_data.census_tracts)} census tracts")
print(f"Found {len(city_data.producers)} producers")
print(f"Found {len(city_data.consumers)} consumers")
```

#### What QCense Extracts:

- **Census tracts**: Official boundaries from U.S. Census Bureau
- **Producers**: Restaurants, cafes, food courts from OpenStreetMap
- **Consumers**: Residential areas, apartments, offices
- **Routing data**: Travel times and distances via GraphHopper

### Step 2: Network Construction

Build the hierarchical hotspot-superspot network:

```python
from src.network_construction import NetworkBuilder

# Configure network parameters
builder = NetworkBuilder(
    ratio=10,           # 1:10 hotspot to superspot ratio
    min_children=4,     # minimum hotspots per superspot
    spacing_threshold=1.0  # prevent superspot clustering
)

# Build network from extracted data
network = builder.build_from_data(
    data_dir="data/philadelphia/",
    output_dir="networks/philadelphia_1_10/"
)

print(f"Created {len(network.hotspots)} hotspots")
print(f"Selected {len(network.superspots)} superspots")
```

#### Network Structure:

- **Hotspots**: One per census tract, placed at consumer/producer centroid
- **Superspots**: Selected using SES (Superspot Eligibility Score)
- **Clusters**: Balanced groupings with spacing constraints

### Step 3: Agent Training

Train Q-learning agents for each hotspot and superspot:

```python
from src.training import AgentTrainer

# Configure training parameters
trainer = AgentTrainer(
    alpha=0.1,              # learning rate
    gamma=0.99,             # discount factor
    episodes=10000,         # training episodes
    temperature_init=1000   # initial exploration temperature
)

# Train all agents
agents = trainer.train_all_agents(
    network_dir="networks/philadelphia_1_10/",
    output_dir="models/philadelphia_1_10/"
)

print(f"Trained {len(agents)} agents")
```

#### Training Process:

- **Hotspot agents**: Learn navigation within superspot clusters
- **Superspot agents**: Learn inter-cluster routing
- **Q-learning**: Model-free reinforcement learning with Boltzmann exploration
- **Decentralized**: Each agent stores only relevant Q-table fragment

### Step 4: Delivery Simulation

Run the complete delivery simulation with ride-sharing:

```python
from src.simulation import DeliverySimulator

# Configure simulation
simulator = DeliverySimulator(
    total_deliveries=300,
    simulation_time=60,     # minutes
    enable_ride_sharing=True,
    ride_share_threshold=0.32  # city-specific parameter
)

# Run simulation
results = simulator.run_simulation(
    network_dir="networks/philadelphia_1_10/",
    agents_dir="models/philadelphia_1_10/",
    output_dir="results/philadelphia_1_10/"
)

print(f"Success rate: {results['success_rate']:.2%}")
print(f"Total distance: {results['total_distance']:.1f} km")
print(f"Average delivery time: {results['avg_delivery_time']:.0f} seconds")
```

#### Simulation Features:

- **Bimodal demand**: Realistic delivery load with peak periods
- **Dynamic ride-sharing**: Q-value based path coordination
- **Time windows**: Distance-dependent delivery deadlines
- **Real-time decisions**: No online retraining required

## Advanced Usage

### Custom City Configuration

Create city-specific configuration:

```yaml
# config/philadelphia.yaml
city:
  name: "Philadelphia"
  state: "Pennsylvania"

network:
  superspot_ratio: 15
  min_children: 6
  
simulation:
  ride_share_threshold: 0.32
  total_deliveries: 400
  
training:
  episodes: 15000
  alpha: 0.05
```

Use custom config:

```bash
python scripts/quick_start.py \
    --city Philadelphia \
    --state Pennsylvania \
    --config config/philadelphia.yaml
```

### Parameter Sweeps

Test multiple configurations:

```python
from src.experiments import ParameterSweep

sweep = ParameterSweep(
    city="Columbus",
    state="Ohio",
    ratios=[5, 10, 15, 20],
    loads=[300, 350, 400, 450, 500],
    thresholds=[0.1, 0.2, 0.3, 0.4, 0.5]
)

results = sweep.run_all_combinations(
    output_dir="experiments/columbus_sweep/"
)
```

### Baseline Comparisons

Compare against different methods:

```python
from src.baselines import BaselineComparison

comparison = BaselineComparison(
    network_dir="networks/philadelphia_1_10/",
    deliveries=300
)

# Point-to-point baseline
p2p_results = comparison.run_p2p_baseline()

# Ablation study (no ride-sharing)
ablation_results = comparison.run_ablation_study()

# DeliverAI comparison (small areas only)
deliverAI_results = comparison.run_deliverAI_comparison()

# Generate comparison report
comparison.generate_report(
    quikdel_results=results,
    output_path="reports/philadelphia_comparison.html"
)
```

## Interpreting Results

### Key Metrics

**Success Rate**: Percentage of deliveries completed within time windows
- Higher is better
- QuikDel typically 85-96% vs 95-100% for baselines

**Total Distance**: Cumulative kilometers traveled by all vehicles
- Lower is better  
- QuikDel reduces distance by 1-13% vs point-to-point

**Average Delivery Time**: Mean seconds per delivery
- Lower is better
- QuikDel has 200-800s increase due to network routing

**Vehicle Utilization**: Total vehicles needed
- Lower is better through ride-sharing
- Varies by city density and demand patterns

### Performance Trade-offs

QuikDel optimizes for distance reduction at the cost of increased delivery times. This trade-off is beneficial when:

- Fuel costs are significant
- Environmental impact is a concern  
- Fleet size needs to be minimized
- Delivery time flexibility exists

### City-Specific Patterns

**Dense cities** (NYC, Chicago): Higher ride-sharing opportunities
**Sprawling cities** (Columbus): Lower but still meaningful improvements  
**Medium cities** (Philadelphia): Balanced performance across metrics

## Troubleshooting

### Common Issues

**GDAL Installation Problems:**
```bash
# Check GDAL installation
python -c "from osgeo import gdal; print('GDAL OK')"

# Set environment variables if needed
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
```

**Memory Issues:**
- Reduce training episodes for large cities
- Use smaller superspot ratios (1:20 instead of 1:10)
- Process cities in smaller chunks

**API Rate Limits:**
- QCense includes automatic retry logic
- Add delays between requests if needed
- Cache results to avoid re-downloading

**Convergence Problems:**
- Adjust learning rate (alpha) and temperature decay
- Increase training episodes
- Verify network connectivity

### Performance Optimization

**For Large Cities:**
```python
# Use efficient settings for cities >1000 census tracts
config = {
    'network': {'superspot_ratio': 20},
    'training': {'episodes': 5000},
    'simulation': {'enable_ride_sharing': True}
}
```

**For Small Cities:**
```python
# Use detailed settings for cities <200 census tracts  
config = {
    'network': {'superspot_ratio': 5},
    'training': {'episodes': 15000},
    'simulation': {'ride_share_threshold': 0.1}
}
```

## Visualization

### Network Structure
```python
from src.visualization import NetworkVisualizer

viz = NetworkVisualizer()
viz.plot_network_structure(
    network_dir="networks/philadelphia_1_10/",
    save_path="figures/philadelphia_network.png"
)
```

### Results Analysis
```python
from src.visualization import ResultsVisualizer

viz = ResultsVisualizer()
viz.plot_performance_comparison(
    results_dir="results/philadelphia_1_10/",
    save_path="figures/philadelphia_results.png"
)
```

### Delivery Paths
```python
viz.plot_delivery_paths(
    results_dir="results/philadelphia_1_10/",
    max_paths=50,  # limit for clarity
    save_path="figures/philadelphia_paths.png"
)
```

## Next Steps

### Research Extensions

1. **Algorithm improvements**: Try different RL algorithms (DQN, A3C)
2. **Multi-objective optimization**: Balance distance, time, and success rate
3. **Dynamic environments**: Handle real-time traffic and demand changes
4. **Larger capacity**: Extend beyond 2 deliveries per vehicle

### Production Deployment

1. **Real-time integration**: Connect to actual delivery APIs
2. **Scalability testing**: Validate on full metro areas
3. **Performance monitoring**: Track system metrics in production
4. **A/B testing**: Compare against existing routing systems

### Academic Research

1. **Theoretical analysis**: Convergence guarantees and complexity bounds
2. **Comparative studies**: Systematic comparison with other methods
3. **Sensitivity analysis**: Robustness to parameter changes
4. **Real-world validation**: Partner with delivery companies

## Getting Help

- **Documentation**: Check `docs/` directory for detailed guides
- **Examples**: See `notebooks/` for interactive tutorials  
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions on GitHub Discussions
- **Email**: Contact maintainers for research collaboration

## Citation

If you use QuikDel in research, please cite:

```bibtex
@article{kilgore2024quikdel,
  title={QuikDel: A Novel \& Scalable Q-learning based Distributed Approach for Efficient Long-haul Delivery},
  author={Kilgore, Robert and Ozdemir, Yusuf and Mehra, Ashman and Hasan, Md Mahid and Raychoudhury, Vaskar and Saha, Snehanshu and Mathur, Archana},
  journal={IEEE Transactions on Intelligent Transportation Systems},  
  year={2024},
  publisher={IEEE}
}
```
