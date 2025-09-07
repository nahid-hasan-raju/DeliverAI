#!/usr/bin/env python3
"""
QuikDel Quick Start Script

This script demonstrates the complete QuikDel pipeline:
1. Extract city data using QCense
2. Build hierarchical network structure  
3. Train Q-learning agents
4. Run delivery simulation
5. Compare with baselines

Usage:
    python scripts/quick_start.py --city Columbus --state Ohio
    python scripts/quick_start.py --help
"""

import argparse
import os
import sys
import time
from pathlib import Path
import yaml
import json

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent / "qcense"))

def setup_directories(base_dir: str, city: str, ratio: int):
    """Create necessary directory structure for the experiment."""
    dirs = {
        'data': f"{base_dir}/data/{city.lower()}",
        'networks': f"{base_dir}/networks/{city.lower()}_1_{ratio}",
        'models': f"{base_dir}/models/{city.lower()}_1_{ratio}",
        'results': f"{base_dir}/results/{city.lower()}_1_{ratio}",
        'figures': f"{base_dir}/figures/{city.lower()}"
    }
    
    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    
    return dirs

def load_config(config_path: str = None):
    """Load configuration file."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "default.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

def extract_city_data(city: str, state: str, output_dir: str, config: dict):
    """Step 1: Extract city data using QCense."""
    print(f"\n🌍 Step 1: Extracting data for {city}, {state}")
    
    try:
        from qcense.extract_city_data import CityDataExtractor
        
        extractor = CityDataExtractor(
            cache_dir=f"{output_dir}/cache",
            timeout=config['data_extraction']['osm_timeout']
        )
        
        city_data = extractor.extract_city_data(
            state=state,
            city=city,
            output_dir=output_dir
        )
        
        print(f"✅ Successfully extracted data for {len(city_data.census_tracts)} census tracts")
        print(f"   - Producers: {len(city_data.producers)}")
        print(f"   - Consumers: {len(city_data.consumers)}")
        return city_data
        
    except ImportError:
        print("❌ QCense module not found. Please install qcense package.")
        return None
    except Exception as e:
        print(f"❌ Error extracting city data: {e}")
        return None

def build_network(data_dir: str, output_dir: str, config: dict):
    """Step 2: Build hierarchical network structure."""
    print(f"\n🏗️  Step 2: Building network structure")
    
    try:
        from src.network_construction.build_network import NetworkBuilder
        
        builder = NetworkBuilder(
            ratio=config['network']['superspot_ratio'],
            min_children=config['network']['min_children'],
            spacing_threshold=config['network']['spacing_threshold']
        )
        
        network = builder.build_from_data(
            data_dir=data_dir,
            output_dir=output_dir
        )
        
        print(f"✅ Network built successfully")
        print(f"   - Hotspots: {len(network.hotspots)}")
        print(f"   - Superspots: {len(network.superspots)}")
        print(f"   - Ratio: 1:{config['network']['superspot_ratio']}")
        return network
        
    except ImportError:
        print("❌ Network construction module not found.")
        return None
    except Exception as e:
        print(f"❌ Error building network: {e}")
        return None

def train_agents(network_dir: str, output_dir: str, config: dict):
    """Step 3: Train Q-learning agents."""
    print(f"\n🧠 Step 3: Training Q-learning agents")
    
    try:
        from src.training.agent_training import AgentTrainer
        
        trainer = AgentTrainer(
            alpha=config['training']['alpha'],
            gamma=config['training']['gamma'],
            episodes=config['training']['episodes'],
            temperature_init=config['training']['temperature_init']
        )
        
        agents = trainer.train_all_agents(
            network_dir=network_dir,
            output_dir=output_dir
        )
        
        print(f"✅ Training completed")
        print(f"   - Episodes: {config['training']['episodes']}")
        print(f"   - Agents trained: {len(agents)}")
        return agents
        
    except ImportError:
        print("❌ Training module not found.")
        return None
    except Exception as e:
        print(f"❌ Error training agents: {e}")
        return None

def run_simulation(network_dir: str, agents_dir: str, output_dir: str, config: dict):
    """Step 4: Run delivery simulation."""
    print(f"\n🚚 Step 4: Running delivery simulation")
    
    try:
        from src.simulation.delivery_engine import DeliverySimulator
        
        simulator = DeliverySimulator(
            total_deliveries=config['simulation']['total_deliveries'],
            simulation_time=config['simulation']['simulation_time'],
            enable_ride_sharing=config['simulation']['enable_ride_sharing'],
            ride_share_threshold=config['simulation']['ride_share_threshold']
        )
        
        results = simulator.run_simulation(
            network_dir=network_dir,
            agents_dir=agents_dir,
            output_dir=output_dir
        )
        
        print(f"✅ Simulation completed")
        print(f"   - Deliveries: {results['total_deliveries']}")
        print(f"   - Success rate: {results['success_rate']:.2%}")
        print(f"   - Total distance: {results['total_distance']:.1f} km")
        print(f"   - Avg delivery time: {results['avg_delivery_time']:.0f} seconds")
        return results
        
    except ImportError:
        print("❌ Simulation module not found.")
        return None
    except Exception as e:
        print(f"❌ Error running simulation: {e}")
        return None

def run_baselines(network_dir: str, output_dir: str, config: dict):
    """Step 5: Run baseline comparisons."""
    print(f"\n📊 Step 5: Running baseline comparisons")
    
    results = {}
    
    # Point-to-Point baseline
    try:
        from src.baselines.point_to_point import P2PBaseline
        
        p2p = P2PBaseline(
            total_deliveries=config['simulation']['total_deliveries']
        )
        
        p2p_results = p2p.run_simulation(
            network_dir=network_dir,
            output_dir=f"{output_dir}/p2p_baseline"
        )
        
        results['p2p'] = p2p_results
        print(f"✅ P2P baseline completed - Distance: {p2p_results['total_distance']:.1f} km")
        
    except Exception as e:
        print(f"❌ P2P baseline failed: {e}")
    
    # Ablation study (no ride-sharing)
    try:
        from src.baselines.ablation_study import AblationStudy
        
        ablation = AblationStudy(
            total_deliveries=config['simulation']['total_deliveries'],
            enable_ride_sharing=False
        )
        
        ablation_results = ablation.run_simulation(
            network_dir=network_dir,
            output_dir=f"{output_dir}/ablation_study"
        )
        
        results['ablation'] = ablation_results
        print(f"✅ Ablation study completed - Distance: {ablation_results['total_distance']:.1f} km")
        
    except Exception as e:
        print(f"❌ Ablation study failed: {e}")
    
    return results

def generate_summary(quikdel_results: dict, baseline_results: dict, output_dir: str):
    """Generate summary report."""
    print(f"\n📈 Step 6: Generating summary report")
    
    summary = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'quikdel': quikdel_results,
        'baselines': baseline_results,
        'comparisons': {}
    }
    
    # Calculate improvements
    if 'p2p' in baseline_results:
        p2p_distance = baseline_results['p2p']['total_distance']
        quikdel_distance = quikdel_results['total_distance']
        distance_improvement = (p2p_distance - quikdel_distance) / p2p_distance * 100
        
        summary['comparisons']['vs_p2p'] = {
            'distance_improvement_percent': distance_improvement,
            'success_rate_diff': quikdel_results['success_rate'] - baseline_results['p2p']['success_rate'],
            'time_increase': quikdel_results['avg_delivery_time'] - baseline_results['p2p']['avg_delivery_time']
        }
        
        print(f"📊 QuikDel vs P2P Baseline:")
        print(f"   - Distance reduction: {distance_improvement:.2f}%")
        print(f"   - Success rate change: {summary['comparisons']['vs_p2p']['success_rate_diff']:.2%}")
    
    # Save summary
    summary_path = f"{output_dir}/experiment_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Summary saved to {summary_path}")
    return summary

def main():
    parser = argparse.ArgumentParser(description="QuikDel Quick Start Demo")
    parser.add_argument('--city', required=True, help='City name (e.g., Columbus)')
    parser.add_argument('--state', required=True, help='State name (e.g., Ohio)')
    parser.add_argument('--ratio', type=int, default=10, help='Superspot ratio (default: 10)')
    parser.add_argument('--config', help='Path to config file (optional)')
    parser.add_argument('--output', default='quickstart_output', help='Output directory')
    parser.add_argument('--skip-data', action='store_true', help='Skip data extraction (use existing)')
    parser.add_argument('--skip-training', action='store_true', help='Skip training (use existing models)')
    
    args = parser.parse_args()
    
    print("🚀 QuikDel Quick Start")
    print("=" * 50)
    print(f"City: {args.city}, {args.state}")
    print(f"Ratio: 1:{args.ratio}")
    print(f"Output: {args.output}")
    print("=" * 50)
    
    # Setup
    config = load_config(args.config)
    config['network']['superspot_ratio'] = args.ratio
    dirs = setup_directories(args.output, args.city, args.ratio)
    
    # Pipeline execution
    start_time = time.time()
    
    # Step 1: Data extraction
    if not args.skip_data:
        city_data = extract_city_data(args.city, args.state, dirs['data'], config)
        if city_data is None:
            print("❌ Data extraction failed. Exiting.")
            return
    else:
        print("⏭️  Skipping data extraction")
    
    # Step 2: Network construction
    network = build_network(dirs['data'], dirs['networks'], config)
    if network is None:
        print("❌ Network construction failed. Exiting.")
        return
    
    # Step 3: Agent training
    if not args.skip_training:
        agents = train_agents(dirs['networks'], dirs['models'], config)
        if agents is None:
            print("❌ Agent training failed. Exiting.")
            return
    else:
        print("⏭️  Skipping agent training")
    
    # Step 4: QuikDel simulation
    quikdel_results = run_simulation(dirs['networks'], dirs['models'], dirs['results'], config)
    if quikdel_results is None:
        print("❌ QuikDel simulation failed. Exiting.")
        return
    
    # Step 5: Baseline comparisons
    baseline_results = run_baselines(dirs['networks'], dirs['results'], config)
    
    # Step 6: Summary report
    summary = generate_summary(quikdel_results, baseline_results, dirs['results'])
    
    total_time = time.time() - start_time
    print(f"\n🎉 QuikDel pipeline completed in {total_time/60:.1f} minutes!")
    print(f"📁 Results saved in: {dirs['results']}")

if __name__ == "__main__":
    main()
