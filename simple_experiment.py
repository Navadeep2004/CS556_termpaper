#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import time
import os
import argparse

def run_experiment(cc_scheme, scenario, rtt):
    """Run a simple TCP experiment with different congestion control algorithms"""
    info(f"*** Starting experiment with {cc_scheme} in scenario {scenario} with RTT {rtt}ms ***\n")
    
    # Create network
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch)
    
    # Add controller
    c0 = net.addController('c0')
    
    # Add switch
    s1 = net.addSwitch('s1')
    
    # Add hosts
    sender = net.addHost('sender')
    receiver = net.addHost('receiver')
    
    # Add links
    delay = rtt // 2  # half RTT for each direction
    
    # Configure link based on scenario
    if scenario == 'sc0':
        # No interference
        net.addLink(sender, s1, delay=f'{delay}ms')
    elif scenario == 'sc1':
        # Low interference (2% packet loss)
        net.addLink(sender, s1, delay=f'{delay}ms', loss=2)
    elif scenario == 'sc2':
        # High interference (5% packet loss)
        net.addLink(sender, s1, delay=f'{delay}ms', loss=5)
    else:
        # RTT scenarios (sc3-sc7)
        net.addLink(sender, s1, delay=f'{delay}ms')
    
    # Receiver link
    net.addLink(s1, receiver, delay=f'{delay}ms')
    
    # Start network
    net.start()
    
    # Set congestion control algorithm
    sender.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={cc_scheme}')
    receiver.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={cc_scheme}')
    
    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Start iperf server on receiver
    receiver.cmd('iperf -s -w 8m -i 1 > iperf_server.log &')
    
    # Wait for server to start
    time.sleep(1)
    
    # Run iperf client on sender
    info(f"*** Running iperf with {cc_scheme} from sender to receiver ***\n")
    
    # Create command to run iperf and save output to file
    iperf_cmd = f'iperf -c {receiver.IP()} -w 8m -t 30 -i 1 > results/iperf_{cc_scheme}_{scenario}.log'
    
    # Run iperf
    info(f"*** Executing: {iperf_cmd} ***\n")
    start_time = time.time()
    sender.cmd(iperf_cmd)
    end_time = time.time()
    
    # Calculate transfer time
    transfer_time = end_time - start_time
    info(f"*** Experiment completed in {transfer_time:.2f} seconds ***\n")
    
    # Parse iperf output to get average throughput
    with open(f"results/iperf_{cc_scheme}_{scenario}.log", "r") as f:
        lines = f.readlines()
    
    # Look for the line with the summary (usually the last line)
    throughput = 0
    for line in reversed(lines):
        if "0.0-30.0" in line and "sec" in line:
            parts = line.split()
            if len(parts) >= 8:
                throughput = float(parts[6])
                throughput_unit = parts[7]
                break
    
    # Create a simple CSV summary
    with open(f"results/summary_{cc_scheme}_{scenario}.csv", "w") as f:
        f.write("cc_scheme,scenario,avg_throughput,transfer_time,rtt\n")
        f.write(f"{cc_scheme},{scenario},{throughput},{transfer_time},{rtt}\n")
    
    # Stop network
    net.stop()
    
    return transfer_time, throughput

def main():
    parser = argparse.ArgumentParser(description='Run simple TCP experiment')
    parser.add_argument('--cc', default='cubic', choices=['reno', 'cubic', 'bbr', 'bbr2', 'vegas'],
                      help='TCP congestion control algorithm')
    parser.add_argument('--scenario', default='sc0', choices=['sc0', 'sc1', 'sc2', 'sc3', 'sc4', 'sc5', 'sc6', 'sc7'],
                      help='Test scenario')
    parser.add_argument('--rtt', type=int, default=50,
                      help='RTT in milliseconds')
    
    args = parser.parse_args()
    
    # Map RTT scenario to appropriate RTT value if needed
    if args.scenario == "sc3":
        args.rtt = 5
    elif args.scenario == "sc4":
        args.rtt = 10
    elif args.scenario == "sc5":
        args.rtt = 50
    elif args.scenario == "sc6":
        args.rtt = 100
    elif args.scenario == "sc7":
        args.rtt = 150
    
    # Set up logging
    setLogLevel('info')
    
    # Run experiment
    transfer_time, throughput = run_experiment(args.cc, args.scenario, args.rtt)
    
    print(f"Results for {args.cc} in scenario {args.scenario} with RTT {args.rtt}ms:")
    print(f"  - Transfer time: {transfer_time:.2f} seconds")
    print(f"  - Throughput: {throughput} Mbits/sec")

if __name__ == '__main__':
    main()
