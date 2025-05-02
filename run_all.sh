#!/bin/bash

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo "Virtual environment not activated. Please run: source ~/congestion-control-env/bin/activate"
  exit 1
fi

# Create directories
mkdir -p results plots/comparative plots/composite
chmod -R 777 results plots

# Compile kernel module if not already compiled
if [ ! -f "tcp_monitor.ko" ]; then
  echo "Compiling kernel module..."
  make
fi

# Clean any previous Mininet instances
sudo mn -c

# Run interference scenarios
for cc in reno cubic bbr bbr2 vegas; do
  for scenario in sc0 sc1 sc2; do
    echo "Running experiment: $cc - $scenario"
    sudo python network_topology.py --cc $cc --scenario $scenario --rtt 50
    sleep 2
  done
done

# Run RTT scenarios
for cc in reno cubic bbr bbr2 vegas; do
  for scenario in sc3 sc4 sc5 sc6 sc7; do
    echo "Running RTT experiment: $cc - $scenario"
    sudo python network_topology.py --cc $cc --scenario $scenario
    sleep 2
  done
done

# Generate plots
echo "Generating signal strength plots..."
python signal_strength_simulator.py

echo "Generating comparative analysis plots..."
python comparative_analysis.py || echo "Warning: Comparative analysis failed"

echo "Generating RTT analysis plots..."
python rtt_analyzer.py || echo "Warning: RTT analysis failed"

echo "All experiments completed. Results are in the 'results' and 'plots' directories."
