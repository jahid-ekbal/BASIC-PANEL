import psutil



def check_process(processName):
    process_name = processName  # replace with the process name you want to check
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            # print(f"Process {process_name} exists")
            return True
    else:
        # print(f"Process {process_name} does not exist")
        return False