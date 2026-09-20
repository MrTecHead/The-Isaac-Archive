import psutil
import time
import datetime
import os
import subprocess

LOG_DIR = "/home/isaac/syslogs"   # Change if you want logs somewhere else

def get_cpu_temp():
    temps = psutil.sensors_temperatures()
    if not temps:
        return None

    for key in ["coretemp", "cpu-thermal", "acpitz"]:
        if key in temps:
            return temps[key][0].current

    first = list(temps.values())[0]
    return first[0].current

def get_battery_info():
    try:
        with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
            capacity = int(f.read())
    except:
        capacity = None

    try:
        with open("/sys/class/power_supply/BAT0/status", "r") as f:
            status = f.read().strip()
    except:
        status = None

    try:
        with open("/sys/class/power_supply/ADP0/online", "r") as f:
            ac_online = int(f.read())
    except:
        ac_online = None

    return capacity, status, ac_online

def get_power_profile():
    try:
        result = subprocess.check_output(["powerprofilesctl", "get"])
        return result.decode().strip()
    except:
        return "Unknown"

def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def get_log_filename():
    now = datetime.datetime.now()
    filename = f"{now.day}.{now.month}.{now.year} syslog.txt"
    return os.path.join(LOG_DIR, filename)

def log_stats():
    ensure_log_dir()

    cpu_temp = get_cpu_temp()
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()

    battery_percent, battery_status, ac_online = get_battery_info()
    power_profile = get_power_profile()

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    log_line = (
        f"[{timestamp}] "
        f"CPU Temp: {cpu_temp if cpu_temp is not None else 'N/A'}°C | "
        f"CPU Usage: {cpu_usage}% | "
        f"Memory Used: {mem.percent}% | "
        f"Battery: {battery_percent}% ({battery_status}) | "
        f"AC: {'Plugged' if ac_online == 1 else 'Unplugged'} | "
        f"Profile: {power_profile}\n"
    )

    with open(get_log_filename(), "a") as logfile:
        logfile.write(log_line)

def main():
    while True:
        log_stats()
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    main()
