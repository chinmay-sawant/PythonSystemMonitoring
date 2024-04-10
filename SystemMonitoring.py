import psutil
import socket
import uuid
from datetime import datetime
import pytz
from tzlocal import get_localzone
import json
from loguru import logger
logger.add("PythonSystemMonitor.log", rotation="500 MB", level="INFO")

class SystemMonitoring:
    def __init__(self,config) -> None:
        logger.info(f"Monitoring Started For ... {config['serverName']}")

    def systemData(self) -> dict:
        # Get hostname
        hostname = socket.gethostname()
        # Get IP address
        ip_address = socket.gethostbyname(hostname)
        # Get MAC address
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)])
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
            "timestamp": self.getTimeZoneData(),
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
        #print(system_stats)
        return system_stats

    def getTimeZoneData(self) -> str:
        # Get the current date and time
        current_time = datetime.now()

        # Get the local timezone
        local_timezone = get_localzone()


      # Convert the current time to the local timezone
        localized_time = current_time.astimezone(local_timezone)

        # Convert the localized time to a string with timezone information
        time_with_timezone_string = localized_time.strftime('%Y-%m-%d %H:%M:%S %Z')
        return time_with_timezone_string
  
if __name__ == "__main__":

    with open("config.json", 'r') as f:
        config = json.load(f)
        SM = SystemMonitoring(config)
        print(SM.systemData())