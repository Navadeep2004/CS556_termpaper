#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import argparse

class RTTAnalyzer:
    def __init__(self, results_dir="./results"):
        self.results_dir = results_dir
        self.cc_schemes = ["reno", "cubic", "bbr", "bbr2", "vegas"]
        self.scenarios = ["sc3", "sc4", "sc5", "sc6", "sc7"]  # RTT test scenarios
        self.rtts = [5, 10, 50, 100, 150]  # Corresponding minimum RTTs
        self.colors = {"reno": "black", "cubic": "blue", "bbr": "red", "bbr2": "orange", "vegas": "green"}
    
    def load_data(self):
        """Load data from all summary files"""
        data = []
        
        for file in glob.glob(f"{self.results_dir}/summary_*_sc*.csv"):
            df = pd.read_csv(file)
            
            # Extract scenario from filename
            if "_sc3" in file:
                df["min_rtt"] = 5
            elif "_sc4" in file:
                df["min_rtt"] = 10
            elif "_sc5" in file:
                df["min_rtt"] = 50
            elif "_sc6" in file:
                df["min_rtt"] = 100
            elif "_sc7" in file:
                df["min_rtt"] = 150
            
            data.append(df)
        
        if not data:
            raise ValueError(f"No summary files found in {self.results_dir}")
        
        return pd.concat(data, ignore_index=True)
    
    def plot_rtt_analysis(self, df, output_dir="./plots"):
        """Generate plots for RTT analysis (similar to Figure 11)"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Filter by RTT scenarios only
        df_rtt = df[df['scenario'].isin(self.scenarios)]
        
        # Generate Figure 11a: Average RTT
        plt.figure(figsize=(12, 8))
        width = 0.15
        indices = np.arange(len(self.scenarios))
        
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['avg_rtt'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            plt.bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        # Add a line for minimum RTT values
        plt.plot(indices, self.rtts, 'k--', label='RTTmin')
        
        plt.xlabel('Scenario')
        plt.ylabel('Average RTT (ms)')
        plt.title('(a) Average RTT')
        plt.xticks(indices + width*2, self.scenarios)
        plt.legend()
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.savefig(f"{output_dir}/rtt_analysis_avg_rtt.png")
        plt.close()
        
        # Generate Figure 11b: RTT Standard Deviation
        plt.figure(figsize=(12, 8))
        
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['std_rtt'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            plt.bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        plt.xlabel('Scenario')
        plt.ylabel('RTT Standard Deviation (ms)')
        plt.title('(b) RTT Standard Deviation')
        plt.xticks(indices + width*2, self.scenarios)
        plt.legend()
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.savefig(f"{output_dir}/rtt_analysis_std_rtt.png")
        plt.close()
        
        # Generate Figure 11c: Average Sending Rate
        plt.figure(figsize=(12, 8))
        
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['avg_sending_rate'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            plt.bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        plt.xlabel('Scenario')
        plt.ylabel('Average Sending Rate (Mbps)')
        plt.title('(c) Average Sending Rate')
        plt.xticks(indices + width*2, self.scenarios)
        plt.legend()
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.savefig(f"{output_dir}/rtt_analysis_sending_rate.png")
        plt.close()
        
        # Generate Figure 11d: Flow Completion Time
        plt.figure(figsize=(12, 8))
        
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    # Use the total transfer time as a proxy for flow completion time
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['transfer_time'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            plt.bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        plt.xlabel('Scenario')
        plt.ylabel('Flow Completion Time (s)')
        plt.title('(d) Average Flow Completion Time')
        plt.xticks(indices + width*2, self.scenarios)
        plt.legend()
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.savefig(f"{output_dir}/rtt_analysis_completion_time.png")
        plt.close()
        
        # Generate combined Figure 11
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))
        
        # Figure 11a: Average RTT
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['avg_rtt'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            axs[0, 0].bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        axs[0, 0].plot(indices, self.rtts, 'k--', label='RTTmin')
        axs[0, 0].set_xlabel('Scenario')
        axs[0, 0].set_ylabel('Average RTT (ms)')
        axs[0, 0].set_title('(a) Average RTT')
        axs[0, 0].set_xticks(indices + width*2)
        axs[0, 0].set_xticklabels(self.scenarios)
        axs[0, 0].grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Figure 11b: RTT Standard Deviation
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['std_rtt'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            axs[0, 1].bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        axs[0, 1].set_xlabel('Scenario')
        axs[0, 1].set_ylabel('RTT Standard Deviation (ms)')
        axs[0, 1].set_title('(b) RTT Standard Deviation')
        axs[0, 1].set_xticks(indices + width*2)
        axs[0, 1].set_xticklabels(self.scenarios)
        axs[0, 1].grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Figure 11c: Average Sending Rate
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['avg_sending_rate'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            axs[1, 0].bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        axs[1, 0].set_xlabel('Scenario')
        axs[1, 0].set_ylabel('Average Sending Rate (Mbps)')
        axs[1, 0].set_title('(c) Average Sending Rate')
        axs[1, 0].set_xticks(indices + width*2)
        axs[1, 0].set_xticklabels(self.scenarios)
        axs[1, 0].grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Figure 11d: Flow Completion Time
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = df_rtt[(df_rtt['cc_scheme'] == cc) & (df_rtt['scenario'] == sc)]['transfer_time'].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            axs[1, 1].bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        axs[1, 1].set_xlabel('Scenario')
        axs[1, 1].set_ylabel('Flow Completion Time (s)')
        axs[1, 1].set_title('(d) Average Flow Completion Time')
        axs[1, 1].set_xticks(indices + width*2)
        axs[1, 1].set_xticklabels(self.scenarios)
        axs[1, 1].grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Add legend
        handles, labels = axs[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=6)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f"{output_dir}/rtt_analysis_combined.png")
        plt.close()

def main():
    parser = argparse.ArgumentParser(description='Analyze RTT for different e2e latencies')
    parser.add_argument('--results', default='./results',
                       help='Directory containing results')
    parser.add_argument('--output', default='./plots',
                       help='Output directory for plots')
    
    args = parser.parse_args()
    
    analyzer = RTTAnalyzer(args.results)
    df = analyzer.load_data()
    analyzer.plot_rtt_analysis(df, args.output)
    
    print("RTT analysis plots generated successfully")

if __name__ == "__main__":
    main()
