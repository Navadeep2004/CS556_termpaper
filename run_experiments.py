#!/usr/bin/env python3

import os
import time
import subprocess
import argparse
from datetime import datetime

def run_command(command):
    """Run shell command and print output"""
    print(f"Executing: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
    
    return process.returncode

def setup_environment():
    """Set up the environment for experiments"""
    print("Setting up the environment...")
    
    # Compile the kernel module
    run_command("make")
    
    # Create necessary directories
    os.makedirs("results", exist_ok=True)
    os.makedirs("plots/comparative", exist_ok=True)
    os.makedirs("plots/composite", exist_ok=True)
    
    # Ensure the scripts are executable
    run_command("chmod +x network_topology.py metrics_processor.py comparative_analysis.py")
    
    print("Environment setup completed")

def run_experiment(cc_scheme, scenario, rtt):
    """Run a single experiment"""
    print(f"\n{'='*80}")
    print(f"Running experiment: CC={cc_scheme}, Scenario={scenario}, RTT={rtt}ms")
    print(f"{'='*80}\n")
    
    # Log start time
    start_time = time.time()
    
    # Run the experiment
    command = f"sudo python3 network_topology.py --cc {cc_scheme} --scenario {scenario} --rtt {rtt}"
    ret_code = run_command(command)
    
    # Log end time and duration
    end_time = time.time()
    duration = end_time - start_time
    
    if ret_code == 0:
        print(f"Experiment completed successfully in {duration:.2f} seconds")
    else:
        print(f"Experiment failed with return code {ret_code}")
    
    # Wait a bit to ensure everything is cleaned up
    time.sleep(5)
    
    return ret_code == 0

def run_all_experiments(cc_schemes, scenarios, rtts):
    """Run all combinations of experiments"""
    results = []
    
    # Start time of all experiments
    start_all = time.time()
    
    for cc in cc_schemes:
        for sc in scenarios:
            for rtt in rtts:
                success = run_experiment(cc, sc, rtt)
                results.append({
                    'cc_scheme': cc,
                    'scenario': sc,
                    'rtt': rtt,
                    'success': success
                })
    
    # End time of all experiments
    end_all = time.time()
    total_duration = end_all - start_all
    
    # Print summary
    print("\n" + "="*80)
    print(f"Experiment Summary (Total time: {total_duration:.2f} seconds)")
    print("="*80)
    
    success_count = sum(1 for r in results if r['success'])
    print(f"Total experiments: {len(results)}")
    print(f"Successful experiments: {success_count}")
    print(f"Failed experiments: {len(results) - success_count}")
    
    # Print failures if any
    if success_count < len(results):
        print("\nFailed experiments:")
        for r in results:
            if not r['success']:
                print(f"  - CC={r['cc_scheme']}, Scenario={r['scenario']}, RTT={r['rtt']}")
    
    return success_count == len(results)

def generate_comparative_analysis():
    """Generate comparative analysis plots"""
    print("\n" + "="*80)
    print("Generating comparative analysis plots")
    print("="*80)
    
    ret_code = run_command("python3 comparative_analysis.py")
    
    if ret_code == 0:
        print("Comparative analysis plots generated successfully")
    else:
        print(f"Comparative analysis failed with return code {ret_code}")
    
    return ret_code == 0

def main():
    parser = argparse.ArgumentParser(description='Run all wireless network experiments')
    parser.add_argument('--cc', nargs='+', default=['reno', 'cubic', 'bbr', 'bbr2', 'vegas'],
                       help='TCP congestion control algorithms to test')
    parser.add_argument('--scenario', nargs='+', default=['sc0', 'sc1', 'sc2'],
                       help='Test scenarios')
    parser.add_argument('--rtt', nargs='+', type=int, default=[170],
                       help='RTT values to test in milliseconds')
    parser.add_argument('--skip-setup', action='store_true',
                       help='Skip environment setup')
    
    args = parser.parse_args()
    
    # Print experiment configuration
    print("\n" + "="*80)
    print("Wireless Network Congestion Control Experiments")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print(f"Congestion Control Schemes: {args.cc}")
    print(f"Scenarios: {args.scenario}")
    print(f"RTT Values: {args.rtt}")
    print("="*80 + "\n")
    
    # Set up environment
    if not args.skip_setup:
        setup_environment()
    
    # Run all experiments
    all_success = run_all_experiments(args.cc, args.scenario, args.rtt)
    
    # Generate comparative analysis
    if all_success:
        generate_comparative_analysis()
    else:
        print("\nSkipping comparative analysis due to failed experiments")
    
    print("\nAll tasks completed!")

if __name__ == '__main__':
    main()
