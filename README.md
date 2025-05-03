# CS556_termpaper
# Congestion Control in Wi-Fi Networks—State of the Art, Performance Evaluation, and Key Research Directions

# Setup Environment
1. Use the Linux Ubuntu operating system.
2. Follow the commands below to install the required tools and dependencies successfully:
3. git clone https://github.com/intrig-unicamp/mininet-wifi
4. cd mininet-wifi
5. sudo util/install.sh -Wlnfv

These commands will:

1. Clone the mininet-wifi repository,

2. Navigate into the project directory, and

3. Install the Wi-Fi network emulation tools and necessary dependencies using the provided installation script.

# How to run
1. Run this command in the terminal "chmod +x run_simple.sh".
2. to activate virtual pythin environment "source ~/congestion-control-env/bin/activate".
3. to run the executable file "./run_simple.sh".
4. Run the "graphs.py" file. This file simulates and visualizes the performance of five congestion control schemes (BBRv1, BBRv2, CUBIC, Reno, and Vegas) under varying Wi-Fi interference scenarios. It computes key network metrics—such as CWND, RTT, sending rate, and flow completion time—and presents them as grouped bar charts for comparative analysis.
