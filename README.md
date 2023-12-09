# gmon: GPU Memory Monitoring Tool

`gmon` is a lightweight, easy-to-use Python tool designed for monitoring GPU memory usage in real-time. It is particularly useful in optimizing and debugging machine learning and data processing applications, tracking peak GPU memory usage, and now features an HTML report for a detailed memory usage graph.

## Installation

To install `gmon`, use pip to install directly from the GitHub repository:

```bash
pip install git+https://github.com/adamlouly/gmon.git
```

Ensure `nvidia-smi` is installed on your system, as `gmon` relies on it to fetch GPU memory usage data.

## Usage

To monitor GPU memory usage of your script with `gmon`, prefix your command like this:

```bash
gmon python your_script.py
```

Replace `your_script.py` with the path to the Python script you want to monitor. `gmon` will execute your script, displaying peak GPU memory usage upon completion, and generate an HTML report if enabled.

### Enabling HTML Report

To enable the HTML report feature, set the environment variable `GMON_TRACE` to `1`. Here's how you can do it on different operating systems:

- **Linux:**
  ```bash
  export GMON_TRACE=1
  gmon python your_script.py
  ```
- **Windows (Command Prompt):**
  ```cmd
  set GMON_TRACE=1
  gmon python your_script.py
  ```

The HTML report (`gmon_gpu_memory_usage.html`) will be generated in the current working directory, providing a visual representation of GPU memory usage over time.

## Features

- **Real-time Monitoring:** Tracks GPU memory usage continuously during script runtime.
- **Peak Memory Reporting:** Reports peak memory usage across all GPUs.
- **HTML Report Generation:** Generates a detailed graph of GPU memory usage over time.
- **Easy Integration:** Seamlessly works with any Python script without script modifications.

## Requirements

- NVIDIA GPU with NVIDIA drivers installed.
- `nvidia-smi` command-line tool.

## License

`gmon` is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for more details.

---