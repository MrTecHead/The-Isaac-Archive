import psutil
import time
import datetime
import os

LOG_DIR = "/home/gaming/syslogs"   # Change if you want logs somewhere else

def get_cpu_temp():
    # Raspberry Pi exposes temp here
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000.0
        return temp
    except:
        return None

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

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    log_line = (
        f"[{timestamp}] "
        f"CPU Temp: {cpu_temp:.2f}°C | "
        f"CPU Usage: {cpu_usage}% | "
        f"Memory Used: {mem.percent}%\n"
    )

    with open(get_log_filename(), "a") as logfile:
        logfile.write(log_line)

def main():
    while True:
        log_stats()
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    main()
