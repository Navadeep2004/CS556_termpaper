#!/usr/bin/env python3

import re
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

class TCPMetricsProcessor:
    def __init__(self, log_file="/var/log/kern.log"):
        self.log_file = log_file
        self.data = {
            'timestamp': [],
            'socket': [],
            'cwnd': [],
            'rtt': [],
            'bytes_in_flight': [],
            'retrans': []
        }
    
    def parse_log(self):
        """Parse the kernel log file to extract TCP metrics"""
        pattern = r"TCP_MONITOR: sock=(\S+) cwnd=(\d+) rtt=(\d+) bytes_in_flight=(\d+) retrans=(\d+)"
        
        with open(self.log_file, 'r') as f:
            for line in f:
                if "TCP_MONITOR" in line:
                    match = re.search(pattern, line)
                    if match:
                        timestamp = time.time()
                        socket, cwnd, rtt, bytes_in_flight, retrans = match.groups()
                        
                        self.data['timestamp'].append(timestamp)
                        self.data['socket'].append(socket)
                        self.data['cwnd'].append(int(cwnd))
                        self.data['rtt'].append(int(rtt))
                        self.data['bytes_in_flight'].append(int(bytes_in_flight))
                        self.data['retrans'].append(int(retrans))
    
    def to_dataframe(self):
        """Convert collected data to a pandas DataFrame"""
        return pd.DataFrame(self.data)
    
    def calculate_sending_rate(self, df, window_size=5):
        """Calculate sending rate based on bytes_in_flight and RTT"""
        if len(df) < 2:
            return df
        
        # Calculate sending rate in Mbps
        df['sending_rate'] = (df['bytes_in_flight'] * 8) / (df['rtt'] * 1000)  # Convert to Mbps
        
        # Apply rolling window to smooth the data
        df['sending_rate'] = df['sending_rate'].rolling(window=window_size, min_periods=1).mean()
        
        return df
    
    def plot_metrics(self, df, cc_scheme, scenario, output_dir="./plots"):
        """Generate plots for the metrics"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set time relative to the start
        df['rel_time'] = df['timestamp'] - df['timestamp'].iloc[0]
        
        # Plot congestion window
        plt.figure(figsize=(10, 6))
        plt.plot(df['rel_time'], df['cwnd'], 'b-')
        plt.title(f'Congestion Window Evolution - {cc_scheme} - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('CWND (packets)')
        plt.grid(True)
        plt.savefig(f"{output_dir}/cwnd_{cc_scheme}_{scenario}.png")
        plt.close()
        
        # Plot RTT
        plt.figure(figsize=(10, 6))
        plt.plot(df['rel_time'], df['rtt'], 'r-')
        plt.title(f'Round Trip Time - {cc_scheme} - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('RTT (ms)')
        plt.grid(True)
        plt.savefig(f"{output_dir}/rtt_{cc_scheme}_{scenario}.png")
        plt.close()
        
        # Plot sending rate
        plt.figure(figsize=(10, 6))
        plt.plot(df['rel_time'], df['sending_rate'], 'g-')
        plt.title(f'Sending Rate - {cc_scheme} - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('Sending Rate (Mbps)')
        plt.grid(True)
        plt.savefig(f"{output_dir}/sending_rate_{cc_scheme}_{scenario}.png")
        plt.close()
        
        # Plot retransmissions
        plt.figure(figsize=(10, 6))
        plt.plot(df['rel_time'], df['retrans'], 'm-')
        plt.title(f'Packet Retransmissions - {cc_scheme} - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('Retransmissions')
        plt.grid(True)
        plt.savefig(f"{output_dir}/retrans_{cc_scheme}_{scenario}.png")
        plt.close()
    
    def generate_summary(self, df, cc_scheme, scenario, output_dir="./results"):
        """Generate summary statistics for the metrics"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        summary = {
            'cc_scheme': cc_scheme,
            'scenario': scenario,
            'avg_cwnd': df['cwnd'].mean(),
            'std_cwnd': df['cwnd'].std(),
            'avg_rtt': df['rtt'].mean(),
            'std_rtt': df['rtt'].std(),
            'avg_sending_rate': df['sending_rate'].mean(),
            'std_sending_rate': df['sending_rate'].std(),
            'total_retrans': df['retrans'].iloc[-1] - df['retrans'].iloc[0] if len(df) > 1 else 0,
            'retrans_rate': (df['retrans'].iloc[-1] - df['retrans'].iloc[0]) / len(df) if len(df) > 1 else 0
        }
        
        # Save to CSV
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv(f"{output_dir}/summary_{cc_scheme}_{scenario}.csv", index=False)
        
        return summary

def main():
    parser = argparse.ArgumentParser(description='Process TCP metrics from kernel logs')
    parser.add_argument('--log', default='/var/log/kern.log', help='Path to kernel log file')
    parser.add_argument('--cc', required=True, help='Congestion control scheme')
    parser.add_argument('--scenario', required=True, help='Test scenario (SC0, SC1, SC2)')
    parser.add_argument('--output', default='./results', help='Output directory for results')
    
    args = parser.parse_args()
    
    processor = TCPMetricsProcessor(args.log)
    processor.parse_log()
    df = processor.to_dataframe()
    df = processor.calculate_sending_rate(df)
    
    processor.plot_metrics(df, args.cc, args.scenario, f"{args.output}/plots")
    summary = processor.generate_summary(df, args.cc, args.scenario, args.output)
    
    print(f"Processed metrics for {args.cc} in scenario {args.scenario}")
    print(f"Average CWND: {summary['avg_cwnd']:.2f}")
    print(f"Average RTT: {summary['avg_rtt']:.2f} ms")
    print(f"Average Sending Rate: {summary['avg_sending_rate']:.2f} Mbps")
    print(f"Total Retransmissions: {summary['total_retrans']}")

if __name__ == "__main__":
    main()
