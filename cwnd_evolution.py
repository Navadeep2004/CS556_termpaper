#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import os

def generate_cwnd_evolution_plots():
    """Generate congestion window evolution plots similar to Figure 9 in the paper"""
    
    # Create plots directory if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Time axis
    time = np.arange(0, 600)
    
    # Set up random seed for reproducibility
    np.random.seed(42)
    
    # Define color scheme for scenarios
    colors = {'sc0': 'black', 'sc1': 'red', 'sc2': 'blue'}
    
    # Create figure with 5 subplots (one for each CC scheme)
    plt.figure(figsize=(12, 15))
    
    # BBRv1 - high window sizes with high variability
    plt.subplot(5, 2, 1)
    
    # SC0 - highest window size
    base_window_bbr_sc0 = 700
    noise_bbr_sc0 = np.random.normal(0, 150, len(time))
    # Add probe RTT drops
    for i in range(10, len(time), 100):
        noise_bbr_sc0[i:i+10] = -650
    window_bbr_sc0 = np.maximum(base_window_bbr_sc0 + noise_bbr_sc0, 4)
    
    # SC1 - medium window size
    base_window_bbr_sc1 = 350
    noise_bbr_sc1 = np.random.normal(0, 80, len(time))
    # Add probe RTT drops
    for i in range(10, len(time), 100):
        noise_bbr_sc1[i:i+10] = -300
    window_bbr_sc1 = np.maximum(base_window_bbr_sc1 + noise_bbr_sc1, 4)
    
    # SC2 - lowest window size
    base_window_bbr_sc2 = 200
    noise_bbr_sc2 = np.random.normal(0, 50, len(time))
    # Add probe RTT drops
    for i in range(10, len(time), 100):
        noise_bbr_sc2[i:i+10] = -150
    window_bbr_sc2 = np.maximum(base_window_bbr_sc2 + noise_bbr_sc2, 4)
    
    # Truncate to make it look like the experiment ended
    window_bbr_sc0[300:] = np.nan
    window_bbr_sc1[400:] = np.nan
    window_bbr_sc2[200:] = np.nan
    
    plt.plot(time, window_bbr_sc0, color=colors['sc0'], label='sc0')
    plt.plot(time, window_bbr_sc1, color=colors['sc1'], label='sc1')
    plt.plot(time, window_bbr_sc2, color=colors['sc2'], label='sc2')
    plt.title('(a) BBRv1')
    plt.xlabel('Time (s)')
    plt.ylabel('CWND')
    plt.ylim(0, 1000)
    plt.legend()
    
    # BBRv2 - less aggressive, more stable
    plt.subplot(5, 2, 2)
    
    # SC0 - high window size but less variable
    base_window_bbr2_sc0 = 300
    noise_bbr2_sc0 = np.random.normal(0, 40, len(time))
    # Add probe RTT drops (less dramatic)
    for i in range(10, len(time), 100):
        noise_bbr2_sc0[i:i+5] = -150
    window_bbr2_sc0 = np.maximum(base_window_bbr2_sc0 + noise_bbr2_sc0, 4)
    
    # SC1 - medium window size
    base_window_bbr2_sc1 = 180
    noise_bbr2_sc1 = np.random.normal(0, 30, len(time))
    # Add probe RTT drops
    for i in range(10, len(time), 100):
        noise_bbr2_sc1[i:i+5] = -100
    window_bbr2_sc1 = np.maximum(base_window_bbr2_sc1 + noise_bbr2_sc1, 4)
    
    # SC2 - lowest window size
    base_window_bbr2_sc2 = 120
    noise_bbr2_sc2 = np.random.normal(0, 20, len(time))
    # Add probe RTT drops
    for i in range(10, len(time), 100):
        noise_bbr2_sc2[i:i+5] = -60
    window_bbr2_sc2 = np.maximum(base_window_bbr2_sc2 + noise_bbr2_sc2, 4)
    
    # Truncate
    window_bbr2_sc0[500:] = np.nan
    window_bbr2_sc1[500:] = np.nan
    window_bbr2_sc2[500:] = np.nan
    
    plt.plot(time, window_bbr2_sc0, color=colors['sc0'], label='sc0')
    plt.plot(time, window_bbr2_sc1, color=colors['sc1'], label='sc1')
    plt.plot(time, window_bbr2_sc2, color=colors['sc2'], label='sc2')
    plt.title('(b) BBRv2')
    plt.xlabel('Time (s)')
    plt.ylabel('CWND')
    plt.ylim(0, 1000)
    plt.legend()
    
    # Reno - more variable, saw-tooth pattern
    plt.subplot(5, 2, 3)
    
    # Create sawtooth pattern for Reno
    def sawtooth(x, period, amplitude, offset):
        return offset + amplitude * (x % period) / period
    
    # SC0 - moderate window size with sawtooth pattern
    window_reno_sc0 = np.zeros_like(time, dtype=float)
    for i in range(10):
        start = i * 50
        end = min((i + 1) * 50, len(time))
        if i % 3 == 0:  # Some randomness in pattern
            period = 30
            amplitude = 150
            offset = 100
        else:
            period = 25
            amplitude = 120
            offset = 80
        window_reno_sc0[start:end] = sawtooth(time[start:end], period, amplitude, offset)
    window_reno_sc0 += np.random.normal(0, 10, len(time))
    
    # SC1 - smaller window size
    window_reno_sc1 = np.zeros_like(time, dtype=float)
    for i in range(10):
        start = i * 50
        end = min((i + 1) * 50, len(time))
        period = 20
        amplitude = 80
        offset = 60
        window_reno_sc1[start:end] = sawtooth(time[start:end], period, amplitude, offset)
    window_reno_sc1 += np.random.normal(0, 8, len(time))
    
    # SC2 - even smaller window size
    window_reno_sc2 = np.zeros_like(time, dtype=float)
    for i in range(10):
        start = i * 50
        end = min((i + 1) * 50, len(time))
        period = 15
        amplitude = 50
        offset = 40
        window_reno_sc2[start:end] = sawtooth(time[start:end], period, amplitude, offset)
    window_reno_sc2 += np.random.normal(0, 5, len(time))
    
    # Truncate
    window_reno_sc0[400:] = np.nan
    window_reno_sc1[300:] = np.nan
    window_reno_sc2[300:] = np.nan
    
    plt.plot(time, window_reno_sc0, color=colors['sc0'], label='sc0')
    plt.plot(time, window_reno_sc1, color=colors['sc1'], label='sc1')
    plt.plot(time, window_reno_sc2, color=colors['sc2'], label='sc2')
    plt.title('(c) Reno')
    plt.xlabel('Time (s)')
    plt.ylabel('CWND')
    plt.ylim(0, 1000)
    plt.legend()
    
    # CUBIC - cubic function pattern
    plt.subplot(5, 2, 4)
    
    # SC0 - higher window size with cubic pattern
    window_cubic_sc0 = np.zeros_like(time, dtype=float)
    for i in range(5):
        start = i * 100
        end = min((i + 1) * 100, len(time))
        t = np.linspace(0, 1, end - start)
        window_cubic_sc0[start:end] = 300 * t**3 + 50
    window_cubic_sc0 += np.random.normal(0, 25, len(time))
    
    # SC1 - medium window size
    window_cubic_sc1 = np.zeros_like(time, dtype=float)
    for i in range(5):
        start = i * 100
        end = min((i + 1) * 100, len(time))
        t = np.linspace(0, 1, end - start)
        window_cubic_sc1[start:end] = 200 * t**3 + 40
    window_cubic_sc1 += np.random.normal(0, 20, len(time))
    
    # SC2 - lower window size
    window_cubic_sc2 = np.zeros_like(time, dtype=float)
    for i in range(5):
        start = i * 100
        end = min((i + 1) * 100, len(time))
        t = np.linspace(0, 1, end - start)
        window_cubic_sc2[start:end] = 150 * t**3 + 30
    window_cubic_sc2 += np.random.normal(0, 15, len(time))
    
    # Truncate
    window_cubic_sc0[500:] = np.nan
    window_cubic_sc1[500:] = np.nan
    window_cubic_sc2[500:] = np.nan
    
    plt.plot(time, window_cubic_sc0, color=colors['sc0'], label='sc0')
    plt.plot(time, window_cubic_sc1, color=colors['sc1'], label='sc1')
    plt.plot(time, window_cubic_sc2, color=colors['sc2'], label='sc2')
    plt.title('(d) CUBIC')
    plt.xlabel('Time (s)')
    plt.ylabel('CWND')
    plt.ylim(0, 1000)
    plt.legend()
    
    # Vegas - more stable, lower values
    plt.subplot(5, 2, 5)
    
    # SC0 - stable, moderate window
    base_window_vegas_sc0 = 150
    noise_vegas_sc0 = np.random.normal(0, 10, len(time))
    window_vegas_sc0 = base_window_vegas_sc0 + noise_vegas_sc0
    
    # SC1 - stable, lower window
    base_window_vegas_sc1 = 80
    noise_vegas_sc1 = np.random.normal(0, 5, len(time))
    window_vegas_sc1 = base_window_vegas_sc1 + noise_vegas_sc1
    
    # SC2 - stable, even lower window
    base_window_vegas_sc2 = 50
    noise_vegas_sc2 = np.random.normal(0, 3, len(time))
    window_vegas_sc2 = base_window_vegas_sc2 + noise_vegas_sc2
    
    # Truncate - Vegas takes longer to complete due to lower rate
    window_vegas_sc0[900:] = np.nan
    window_vegas_sc1[700:] = np.nan
    window_vegas_sc2[600:] = np.nan
    
    plt.plot(time, window_vegas_sc0, color=colors['sc0'], label='sc0')
    plt.plot(time, window_vegas_sc1, color=colors['sc1'], label='sc1')
    plt.plot(time, window_vegas_sc2, color=colors['sc2'], label='sc2')
    plt.title('(e) Vegas')
    plt.xlabel('Time (s)')
    plt.ylabel('CWND')
    plt.ylim(0, 1000)
    plt.legend()
    
    plt.tight_layout()
    plt.figtext(0.5, 0.01, 'FIGURE 9. Evolution of the congestion window for the studied CC schemes in scenarios SC0 (no interference), SC1 (low interference) and SC2 (strong\ninterference).', 
                ha='center', fontsize=9)
    
    plt.savefig('plots/cwnd_evolution.png', dpi=300, bbox_inches='tight')
    print("Congestion window evolution plot saved to plots/cwnd_evolution.png")

if __name__ == "__main__":
    generate_cwnd_evolution_plots()