import psutil
import json

def get_process_list_json():
    process_list = []
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'username', 'memory_percent'])
            process_info['cpu_percent'] = process.cpu_percent()
            process_info['memory_percent'] = process.memory_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        process_list.append(process_info)
    
    # Sort the process list by memory_percent
    sorted_process_list = sorted(process_list, key=lambda x: x['memory_percent'], reverse=True)
    
    return json.dumps(sorted_process_list)

if __name__ == "__main__":
    process_list_json = get_process_list_json()
    print(process_list_json)
