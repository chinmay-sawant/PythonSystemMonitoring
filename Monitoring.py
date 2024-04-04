import psutil
import json
import time
import socket
import uuid

class Monitoring:
    def __init__(self) -> None:
        print(f"Monitoring Started For ...")

while True:
    # Get hostname
    hostname = socket.gethostname()

    # Get IP address
    ip_address = socket.gethostbyname(hostname)

    # Get MAC address
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)])

    time.sleep(5)
    # Get CPU utilization
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()

    # Get RAM utilization
    ram = psutil.virtual_memory()
    ram_total = ram.total
    ram_used = ram.used
    ram_percent = ram.percent

    # Get disk utilization
    disk_partitions = psutil.disk_partitions()
    disk_info = []
    for partition in disk_partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "total": partition_usage.total,
            "used": partition_usage.used,
            "free": partition_usage.free,
            "percent": partition_usage.percent
        })

    # Construct JSON object
    system_stats = {
        "hostname": hostname,
        "ipaddress" : ip_address,
        "macaddress": mac_address,
        "health":
        {
        "cpu": {
            "count": cpu_count,
            "percent": cpu_percent
        },
        "ram": {
            "total": ram_total,
            "used": ram_used,
            "percent": ram_percent
        },
        "disk": disk_info
    }
        
    }

    # Convert to JSON format
    # system_stats_json = json.dumps(system_stats, indent=4)

    # Print JSON object
    print(system_stats)
