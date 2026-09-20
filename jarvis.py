import os
import time
from gtts import gTTS
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "YOUR BOT TOKEN (@BotFather)"

ALLOWED_USER_ID = Your Telegram User ID
PIN_CODE = "1234"

jarvis_unlocked = False

#unauthjarvis.txt log
#Only use if you want to see whos trying to message your bot
def log_unauthorized(user, message):
    timestamp = datetime.now().strftime("[%S:%M:%H][%d/%m/%Y]")
    line = f"{timestamp} User @{user}: {message}\n"
    with open("/home/isaac/unauthjarvis.txt", "a") as f:
        f.write(line)

# -------------------------
# COMMAND FUNCTIONS
# -------------------------

async def cmd_ping(update):
    await update.message.reply_text("Pong.")

async def cmd_time(update):
    import datetime
    now = datetime.datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"The time is {now}")

async def cmd_shutdown(update):
    await update.message.reply_text("Shutting down system.")
    # Example: run a system command
    os.system("shutdown now")

async def cmd_sleep(update):
    await update.message.reply_text("Putting system to bed...")
    os.system("systemctl suspend")
    await update.message.reply_text("System Sleeping")

import psutil
import subprocess

async def cmd_battery(update):
    batt = psutil.sensors_battery()
    if batt is None:
        await update.message.reply_text("No battery detected.")
        return

    percent = batt.percent
    charging = "Charging" if batt.power_plugged else "Not charging"
    await update.message.reply_text(f"Battery: {percent}% ({charging})")

async def cmd_cpu(update):
    cpu = psutil.cpu_percent(interval=1)
    await update.message.reply_text(f"CPU Load: {cpu}%")

async def cmd_uptime(update):
    uptime_seconds = time.time() - psutil.boot_time()
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    await update.message.reply_text(f"Uptime: {hours}h {minutes}m")

async def cmd_wifi(update):
    try:
        ssid = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"]).decode()
        active = [line for line in ssid.split("\n") if line.startswith("yes:")]
        if active:
            ssid_name = active[0].split(":")[1]
            await update.message.reply_text(f"Connected to WiFi: {ssid_name}")
        else:
            await update.message.reply_text("Not connected to WiFi.")
    except Exception:
        await update.message.reply_text("Could not read WiFi status.")
        
async def cmd_roll(update):
    import random
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) == 1:
        await update.message.reply_text("Usage: /roll 1d20")
        return

    try:
        dice = parts[1].lower()
        amount, sides = dice.split("d")
        amount = int(amount)
        sides = int(sides)

        rolls = [random.randint(1, sides) for _ in range(amount)]
        await update.message.reply_text(f"Rolls: {rolls}  Total: {sum(rolls)}")
    except:
        await update.message.reply_text("Invalid format. Use /roll 1d20")

async def cmd_flip(update):
    import random
    result = random.choice(["Heads", "Tails"])
    await update.message.reply_text(f"Coin flip: {result}")

async def cmd_stats(update):
    import psutil

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    msg = f"CPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%"
    await update.message.reply_text(msg)


async def cmd_say(update):
    text = update.message.text.replace("/say", "").strip()
    if not text:
        await update.message.reply_text("Usage: /say hello world")
        return

    tts = gTTS(text=text, lang="en")
    filename = "/home/isaac/jarvis_tts.mp3"
    tts.save(filename)

    with open(filename, "rb") as f:
        await update.message.reply_voice(f)

async def cmd_brightness(update):
    import subprocess

    text = update.message.text.strip()
    parts = text.split()

    if len(parts) == 1:
        await update.message.reply_text("Usage: /brightness <value>\nExamples:\n/brightness 50\n/brightness +10\n/brightness -20")
        return

    value = parts[1]

    try:
        # brightnessctl handles +10, -10, 50%, etc.
        subprocess.run(["brightnessctl", "set", value], check=True)
        await update.message.reply_text(f"Brightness set to {value}")
    except Exception:
        await update.message.reply_text("Failed to set brightness.")

async def cmd_volume(update):
    import subprocess

    text = update.message.text.strip().split()
    if len(text) == 1:
        await update.message.reply_text("Usage: /volume <value>\nExamples:\n/volume 50\n/volume +10\n/volume -20")
        return

    value = text[1]

    try:
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", value], check=True)
        await update.message.reply_text(f"Volume set to {value}")
    except Exception:
        await update.message.reply_text("Failed to change volume.")

async def cmd_mute(update):
    import subprocess
    subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"])
    await update.message.reply_text("Muted.")

async def cmd_unmute(update):
    import subprocess
    subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"])
    await update.message.reply_text("Unmuted.")
    
async def cmd_play(update):
    import subprocess

    text = update.message.text.strip().split(maxsplit=1)
    if len(text) == 1:
        await update.message.reply_text("Usage: /play <path-to-audio-file>")
        return

    file = text[1]

    try:
        subprocess.Popen(["mpv", "--no-video", file])
        await update.message.reply_text(f"Playing: {file}")
    except Exception:
        await update.message.reply_text("Failed to play file.")

async def cmd_pause(update):
    import subprocess
    subprocess.run(["pkill", "-STOP", "mpv"])
    await update.message.reply_text("Paused.")

async def cmd_resume(update):
    import subprocess
    subprocess.run(["pkill", "-CONT", "mpv"])
    await update.message.reply_text("Resumed.")

async def cmd_stop(update):
    import subprocess
    subprocess.run(["pkill", "mpv"])
    await update.message.reply_text("Stopped playback.")

# Add new commands here
COMMANDS = {
    "ping": cmd_ping,
    "time": cmd_time,
    "shutdown": cmd_shutdown,
    "battery": cmd_battery,
    "cpu": cmd_cpu,
    "uptime": cmd_uptime,
    "wifi": cmd_wifi,
    "roll": cmd_roll,
    "flip": cmd_flip,
    "stats": cmd_stats,
    "say": cmd_say,
    "brightness": cmd_brightness,
    "volume": cmd_volume,
    "mute": cmd_mute,
    "unmute": cmd_unmute,
    "play": cmd_play,
    "pause": cmd_pause,
    "resume": cmd_resume,
    "stop": cmd_stop,
    "sleep": cmd_sleep,
}

# -------------------------
# MAIN HANDLER
# -------------------------

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global jarvis_unlocked

    user_id = update.message.from_user.id
    username = update.message.from_user.username or "unknown"
    text = update.message.text

    # Unauthorized user logging
    if user_id != ALLOWED_USER_ID:
        log_unauthorized(username, text)
        await update.message.reply_text("Access denied.")
        return



    # Locked mode
    if not jarvis_unlocked:
        if text == PIN_CODE:
            jarvis_unlocked = True
            await update.message.reply_text("Jarvis unlocked.")
        else:
            await update.message.reply_text("Jarvis is locked. Enter PIN.")
        return

    # Lock command
    if text.lower() == "/lock":
        jarvis_unlocked = False
        await update.message.reply_text("Jarvis locked.")
        return

    # Command parser
    if text.startswith("/"):
        cmd = text[1:].split(" ")[0].strip().lower()
        
        if cmd in COMMANDS:
            await COMMANDS[cmd](update)
        else:
            await update.message.reply_text("Unknown command.")
        return
        


    # Normal chat
    await update.message.reply_text(f"Jarvis online. You said: {text}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()

