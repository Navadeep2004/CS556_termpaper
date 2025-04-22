#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob

def load_results():
    """Load results from all summary files"""
    data = []
    
    for file in glob.glob("results/summary_*.csv"):
        df = pd.read_csv(file)
        data.append(df)
    
    if not data:
        raise ValueError("No summary files found in results directory")
    
    return pd.concat(data, ignore_index=True)

def plot_throughput_comparison(df):
    """Plot throughput comparison across CC schemes for different scenarios"""
    plt.figure(figsize=(12, 8))
    
    cc_schemes = sorted(df['cc_scheme'].unique())
    scenarios = ['sc0', 'sc1', 'sc2']
    
    # Set width of bars
    width = 0.2
    x = np.arange(len(scenarios))
    
    # Plot bars for each CC scheme
    for i, cc in enumerate(cc_schemes):
        values = []
        for sc in scenarios:
            try:
                val = df[(df['cc_scheme'] == cc) & (df['scenario'] == sc)]['avg_throughput'].values[0]
                values.append(val)
            except:
                values.append(0)
        
        plt.bar(x + (i - len(cc_schemes)/2 + 0.5) * width, values, width, label=cc.upper())
    
    plt.xlabel('Scenario')
    plt.ylabel('Throughput (Mbits/sec)')
    plt.title('Throughput Comparison Across CC Schemes')
    plt.xticks(x, scenarios)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save plot
    plt.savefig("plots/throughput_comparison.png")
    plt.close()

def plot_transfer_time_comparison(df):
    """Plot transfer time comparison across CC schemes for different scenarios"""
    plt.figure(figsize=(12, 8))
    
    cc_schemes = sorted(df['cc_scheme'].unique())
    scenarios = ['sc0', 'sc1', 'sc2']
    
    # Set width of bars
    width = 0.2
    x = np.arange(len(scenarios))
    
    # Plot bars for each CC scheme
    for i, cc in enumerate(cc_schemes):
        values = []
        for sc in scenarios:
            try:
                val = df[(df['cc_scheme'] == cc) & (df['scenario'] == sc)]['transfer_time'].values[0]
                values.append(val)
            except:
                values.append(0)
        
        plt.bar(x + (i - len(cc_schemes)/2 + 0.5) * width, values, width, label=cc.upper())
    
    plt.xlabel('Scenario')
    plt.ylabel('Transfer Time (s)')
    plt.title('Transfer Time Comparison Across CC Schemes')
    plt.xticks(x, scenarios)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save plot
    plt.savefig("plots/transfer_time_comparison.png")
    plt.close()

def plot_rtt_analysis(df):
    """Plot RTT analysis for cubic"""
    # Filter for RTT scenarios with cubic
    df_rtt = df[df['scenario'].isin(['sc3', 'sc4', 'sc5', 'sc6', 'sc7']) & (df['cc_scheme'] == 'cubic')]
    
    if len(df_rtt) == 0:
        print("No RTT data found for cubic")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Plot throughput vs RTT
    plt.subplot(2, 1, 1)
    plt.plot(df_rtt['rtt'], df_rtt['avg_throughput'], 'o-', linewidth=2)
    plt.xlabel('RTT (ms)')
    plt.ylabel('Throughput (Mbits/sec)')
    plt.title('Throughput vs RTT for CUBIC')
    plt.grid(True)
    
    # Plot transfer time vs RTT
    plt.subplot(2, 1, 2)
    plt.plot(df_rtt['rtt'], df_rtt['transfer_time'], 'o-', linewidth=2)
    plt.xlabel('RTT (ms)')
    plt.ylabel('Transfer Time (s)')
    plt.title('Transfer Time vs RTT for CUBIC')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("plots/rtt_analysis.png")
    plt.close()

def plot_combined_results(df):
    """Create a combined plot similar to Figure 10 in the paper"""
    plt.figure(figsize=(15, 10))
    
    cc_schemes = sorted(df['cc_scheme'].unique())
    scenarios = ['sc0', 'sc1', 'sc2']
    
    # Set width of bars
    width = 0.2
    x = np.arange(len(scenarios))
    
    # Plot throughput
    plt.subplot(2, 1, 1)
    for i, cc in enumerate(cc_schemes):
        values = []
        for sc in scenarios:
            try:
                val = df[(df['cc_scheme'] == cc) & (df['scenario'] == sc)]['avg_throughput'].values[0]
                values.append(val)
            except:
                values.append(0)
        
        plt.bar(x + (i - len(cc_schemes)/2 + 0.5) * width, values, width, label=cc.upper())
    
    plt.xlabel('Scenario')
    plt.ylabel('Throughput (Mbits/sec)')
    plt.title('(a) Average Throughput')
    plt.xticks(x, scenarios)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Plot transfer time
    plt.subplot(2, 1, 2)
    for i, cc in enumerate(cc_schemes):
        values = []
        for sc in scenarios:
            try:
                val = df[(df['cc_scheme'] == cc) & (df['scenario'] == sc)]['transfer_time'].values[0]
                values.append(val)
            except:
                values.append(0)
        
        plt.bar(x + (i - len(cc_schemes)/2 + 0.5) * width, values, width, label=cc.upper())
    
    plt.xlabel('Scenario')
    plt.ylabel('Transfer Time (s)')
    plt.title('(b) Flow Completion Time')
    plt.xticks(x, scenarios)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig("plots/composite/fig10_composite.png")
    plt.close()

def main():
    try:
        # Load results
        df = load_results()
        
        # Print summary
        print("Loaded results:")
        print(df)
        
        # Create plots
        plot_throughput_comparison(df)
        plot_transfer_time_comparison(df)
        plot_rtt_analysis(df)
        plot_combined_results(df)
        
        print("Plots generated successfully in the 'plots' directory")
        
    except Exception as e:
        print(f"Error generating plots: {e}")

if __name__ == "__main__":
    main()
