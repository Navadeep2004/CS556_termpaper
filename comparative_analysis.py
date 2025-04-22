#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

class ComparativeAnalysis:
    def __init__(self, results_dir="./results"):
        self.results_dir = results_dir
        self.cc_schemes = ["reno", "cubic", "bbr", "bbr2", "vegas"]
        self.scenarios = ["sc0", "sc1", "sc2"]
        self.metrics = ["avg_cwnd", "avg_rtt", "std_rtt", "avg_sending_rate", "total_retrans", "retrans_rate"]
        self.colors = {"reno": "black", "cubic": "blue", "bbr": "red", "bbr2": "orange", "vegas": "green"}
        
    def load_summary_data(self):
        """Load summary data from CSV files"""
        data = []
        for file in glob.glob(f"{self.results_dir}/summary_*.csv"):
            df = pd.read_csv(file)
            data.append(df)
        
        if not data:
            raise ValueError(f"No summary files found in {self.results_dir}")
        
        return pd.concat(data, ignore_index=True)
    
    def plot_metric_by_scenario(self, df, metric, output_dir="./plots/comparative"):
        """Plot metric comparison across CC schemes for each scenario"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        plt.figure(figsize=(12, 8))
        
        # Group by CC scheme and scenario
        grouped = df.groupby(['cc_scheme', 'scenario'])
        
        width = 0.15
        indices = np.arange(len(self.scenarios))
        
        for i, cc in enumerate(self.cc_schemes):
            values = []
            for sc in self.scenarios:
                try:
                    val = grouped.get_group((cc, sc))[metric].values[0]
                    values.append(val)
                except:
                    values.append(0)
            
            plt.bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
        
        plt.xlabel('Scenario')
        plt.ylabel(self.get_metric_label(metric))
        plt.title(f'Comparison of {self.get_metric_label(metric)} Across CC Schemes')
        plt.xticks(indices + width*2, self.scenarios)
        plt.legend()
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        plt.savefig(f"{output_dir}/{metric}_comparison.png")
        plt.close()
    
    def get_metric_label(self, metric):
        """Return a readable label for each metric"""
        labels = {
            "avg_cwnd": "Average Window Size",
            "std_cwnd": "Window Size Std. Dev.",
            "avg_rtt": "Average RTT (ms)",
            "std_rtt": "RTT Standard Deviation (ms)",
            "avg_sending_rate": "Average Sending Rate (Mbps)",
            "std_sending_rate": "Sending Rate Std. Dev. (Mbps)",
            "total_retrans": "Total Retransmissions",
            "retrans_rate": "Retransmission Rate (%)"
        }
        return labels.get(metric, metric)
    
    def plot_all_comparative_metrics(self):
        """Generate all comparative plots"""
        df = self.load_summary_data()
        
        for metric in self.metrics:
            self.plot_metric_by_scenario(df, metric)
        
        # Generate Fig. 10 style composite figure
        self.generate_composite_figure(df)
    
    def generate_composite_figure(self, df):
        """Generate a composite figure similar to Fig. 10 in the paper"""
        output_dir = "./plots/composite"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        fig, axs = plt.subplots(3, 2, figsize=(15, 15))
        
        # Define metrics to plot
        plot_metrics = [
            ("avg_cwnd", "Average Window Size", axs[0, 0]),
            ("avg_sending_rate", "Average Sending Rate (Mbps)", axs[0, 1]),
            ("avg_rtt", "Average RTT (ms)", axs[1, 0]),
            ("std_rtt", "RTT Standard Deviation (ms)", axs[1, 1]),
            ("total_retrans", "Flow Completion Time (s)", axs[2, 0]),
            ("retrans_rate", "Retransmission Rate (%)", axs[2, 1])
        ]
        
        # Group by CC scheme and scenario
        grouped = df.groupby(['cc_scheme', 'scenario'])
        
        width = 0.15
        indices = np.arange(len(self.scenarios))
        
        for metric, title, ax in plot_metrics:
            for i, cc in enumerate(self.cc_schemes):
                values = []
                for sc in self.scenarios:
                    try:
                        val = grouped.get_group((cc, sc))[metric].values[0]
                        values.append(val)
                    except:
                        values.append(0)
                
                ax.bar(indices + i*width, values, width, label=cc.upper(), color=self.colors[cc])
            
            ax.set_xlabel('Scenario')
            ax.set_ylabel(title)
            ax.set_title(title)
            ax.set_xticks(indices + width*2)
            ax.set_xticklabels(self.scenarios)
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Add common legend
        handles, labels = axs[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=5)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for the legend
        plt.savefig(f"{output_dir}/fig10_composite.png")
        plt.close()

def main():
    analyzer = ComparativeAnalysis()
    analyzer.plot_all_comparative_metrics()
    print("Generated comparative analysis plots")

if __name__ == "__main__":
    main()
