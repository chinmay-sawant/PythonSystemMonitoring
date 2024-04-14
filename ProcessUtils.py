import psutil
import time

# Function to get CPU utilization for each process
def get_process_utilization():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            process_info = proc.info
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

# Function to display process information
def display_process_info(processes):
    print("PID\tName\t\tCPU Utilization")
    for proc in processes:
        print(f"{proc['pid']}\t{proc['name']}\t\t{proc['cpu_percent']}%")

# Main function
def main():
    while True:
        processes = get_process_utilization()
        display_process_info(processes)
        time.sleep(1)  # Refresh every second

if __name__ == "__main__":
    main()
