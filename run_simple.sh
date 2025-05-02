#!/bin/bash

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo "Virtual environment not activated. Please run: source ~/congestion-control-env/bin/activate"
  exit 1
fi

# Create directories
mkdir -p results plots/comparative plots/composite
chmod -R 777 results plots

# Clean any previous Mininet instances
sudo mn -c

# Test the script with one example
echo "Running test: cubic - sc0"
sudo python simple_experiment.py --cc cubic --scenario sc0 --rtt 50

# If the test is successful, run more experiments
echo "Test completed successfully. Running all experiments..."

# Run all experiments
for cc in reno cubic bbr; do
  for scenario in sc0 sc1 sc2; do
    echo "Running: $cc - $scenario"
    sudo python simple_experiment.py --cc $cc --scenario $scenario --rtt 50
    sleep 2
  done
done

# Run RTT scenarios with cubic
for scenario in sc3 sc4 sc5 sc6 sc7; do
  echo "Running RTT experiment: cubic - $scenario"
  sudo python simple_experiment.py --cc cubic --scenario $scenario
  sleep 2
done

echo "All experiments completed. Results are in the results directory."
