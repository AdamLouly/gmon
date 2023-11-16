import subprocess
import threading
import time
import argparse
from termcolor import colored
import sys

# Global variables to track the peak memory
peak_memory = 0.0
peak_memory_lock = threading.Lock()

# A global flag to indicate when to stop the GPU monitoring
stop_monitoring = False
def monitor_gpu():
    global peak_memory
    global peak_gpus_memory
    peak_gpus_memory = []  # Initialize an empty list to store GPU memory
    while not stop_monitoring:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv'],
                                capture_output=True, text=True)
        memory_usage = result.stdout.splitlines()
        if len(memory_usage) > 1:
            # Parse the memory usage of each GPU
            gpu_memory = [float(line.split(',')[0].strip().split(' ')[0]) for line in memory_usage[1:]]
            # Find the peak memory among all GPUs
            current_peak = max(gpu_memory)
            with peak_memory_lock:
                if(current_peak > peak_memory):
                    peak_memory = current_peak
                    peak_gpus_memory = gpu_memory
        # Sleep for 2 seconds
        time.sleep(0.1)

def run_script(script_name):
    subprocess.run(script_name, shell=True)

def main():
    global stop_monitoring, peak_memory  # Declare the global flags and variables

    # Get the script name from command-line arguments
    script_to_run = " ".join(sys.argv[1:])

    # Start GPU monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_gpu)
    monitor_thread.start()
    print(script_to_run)
    # Run the script
    run_script(script_to_run)

    # Set the flag to stop monitoring
    stop_monitoring = True

    # Wait for the monitoring thread to finish
    monitor_thread.join()

    # Print the peak GPU memory report in a colorful format
    print(colored("**************** GMON Peak GPU Memory Report ****************", "green"))
    print(colored(f"Peak Memory: {peak_memory} MiB", "cyan"))
    print(colored("---------------------- Peak GPUS Memory ---------------------", "yellow"))
    for i, memory in enumerate(peak_gpus_memory):
        if memory == peak_memory:
            print(colored(f"GPU {i} : {memory} MiB", "cyan"))
        else:
            print(colored(f"GPU {i} : {memory} MiB"))
    print(colored("**************************************************************", "green"))

if __name__ == "__main__":
    main()
