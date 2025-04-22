#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os

def generate_signal_strength_plots():
    """Generate signal strength plots similar to Figure 8 in the paper"""
    
    # Create plots directory if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Set up time arrays for each scenario
    time_sc0 = np.arange(0, 1000)
    time_sc1 = np.arange(0, 640)
    time_sc2 = np.arange(0, 640)
    
    # SC0: No interference - moderate variations
    base_level_sc0 = -60
    noise_sc0 = np.random.normal(0, 8, len(time_sc0))
    slow_var_sc0 = 8 * np.sin(2 * np.pi * time_sc0 / 200)
    signal_sc0 = base_level_sc0 + noise_sc0 + slow_var_sc0
    signal_sc0 = savgol_filter(signal_sc0, 11, 3)  # Smooth the signal
    
    # SC1: Low interference - regular pattern
    base_level_sc1 = -65
    noise_sc1 = np.random.normal(0, 2, len(time_sc1))
    interference_sc1 = 15 * np.sin(2 * np.pi * time_sc1 / 20)
    slow_var_sc1 = 5 * np.sin(2 * np.pi * time_sc1 / 320)
    signal_sc1 = base_level_sc1 + noise_sc1 + interference_sc1 + slow_var_sc1
    
    # SC2: Strong interference - fewer but stronger variations
    base_level_sc2 = -70
    noise_sc2 = np.random.normal(0, 3, len(time_sc2))
    interference_sc2 = 12 * np.sin(2 * np.pi * time_sc2 / 160)
    signal_sc2 = base_level_sc2 + noise_sc2 + interference_sc2
    signal_sc2 = savgol_filter(signal_sc2, 31, 3)  # Stronger smoothing
    
    # Create the figure and subplots
    plt.figure(figsize=(8, 12))
    
    # SC0 plot
    plt.subplot(3, 1, 1)
    plt.plot(time_sc0, signal_sc0, 'r-')
    plt.ylim(-90, -30)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal Strength (dBm)')
    plt.title('(a) Signal strength behavior in SC0.')
    plt.grid(True, alpha=0.3)
    
    # SC1 plot
    plt.subplot(3, 1, 2)
    plt.plot(time_sc1, signal_sc1, 'r-')
    plt.ylim(-90, -30)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal Strength (dBm)')
    plt.title('(b) Signal strength behavior in SC1.')
    plt.grid(True, alpha=0.3)
    
    # SC2 plot
    plt.subplot(3, 1, 3)
    plt.plot(time_sc2, signal_sc2, 'r-')
    plt.ylim(-90, -30)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal Strength (dBm)')
    plt.title('(c) Signal strength behavior in SC2.')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.figtext(0.5, 0.01, 'FIGURE 8. Signal strength over time in scenario SC0 (with no\ninterference) and scenarios SC1 and SC2 (with interference).', 
                ha='center', fontsize=9)
    
    plt.savefig('plots/signal_strength.png', dpi=300, bbox_inches='tight')
    print("Signal strength plot saved to plots/signal_strength.png")

if __name__ == "__main__":
    generate_signal_strength_plots()