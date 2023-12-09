import subprocess
import threading
import time
from termcolor import colored
import sys
import shutil
import os
from .utils import generate_html
# Global variables to track the peak memory
peak_memory = 0.0
peak_memory_lock = threading.Lock()
gpu_memory_data = []
trace_memory = False  # Flag for tracing
stop_monitoring = False

def get_max_gb():
    # Execute the nvidia-smi command to get total memory for each GPU
    result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv'],
                            capture_output=True, text=True)
    memory_info = result.stdout.splitlines()

    # Initialize an empty list to store total memory for each GPU
    total_memories = []

    # Process the output to extract memory information
    if len(memory_info) > 1:
        # Parse the total memory of each GPU
        total_memories = [float(line.split()[0]) for line in memory_info[1:]]
    return int(total_memories[0]/1024)

def monitor_gpu():
    global peak_memory, peak_gpus_memory, gpu_memory_data

    peak_gpus_memory = []  # Initialize an empty list to store GPU memory
    while not stop_monitoring:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv'],
                                capture_output=True, text=True)
        memory_usage = result.stdout.splitlines()
        if len(memory_usage) > 1:
            # Parse the memory usage of each GPU
            gpu_memory = [float(line.split(',')[0].strip().split(' ')[0]) for line in memory_usage[1:]]
            gpu_memory_data.append(gpu_memory)
            # Find the peak memory among all GPUs
            current_peak = max(gpu_memory)
            with peak_memory_lock:
                if(current_peak > peak_memory):
                    peak_memory = current_peak
                    peak_gpus_memory = gpu_memory
        # Sleep for 0.1 seconds
        time.sleep(0.1)

def run_script(script_name):
    subprocess.run(script_name, shell=True)

def check_nvidia_smi():
    """Check if nvidia-smi is installed."""
    return shutil.which("nvidia-smi") is not None

def main():
    global stop_monitoring, peak_memory, gpu_memory_data  # Declare the global flags and variables

    # Check if nvidia-smi is installed
    if not check_nvidia_smi():
        print("Error: nvidia-smi is not installed. Please install it to use this tool.")
        sys.exit(1)
    
    # Get the script name from command-line arguments
    script_to_run = " ".join(sys.argv[1:])
    
    trace_memory = os.environ.get('GMON_TRACE', '0') == '1'

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

    if trace_memory:
        print(colored("GMON is Generating the HTML Graph Report...", "blue"))
        max_y = get_max_gb()
        generate_html(gpu_memory_data, max_y)
        print(colored("GMON HTML file generated: gmon_gpu_memory_usage.html", "blue"))

if __name__ == "__main__":
    main()
