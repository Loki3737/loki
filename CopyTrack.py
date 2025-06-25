import pyperclip
import time
from datetime import datetime, timedelta
import re
import winreg
import os
import sys

# Define the log file path on the user's Desktop
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
LOG_FILE = os.path.abspath(os.path.join(desktop, "CopyTrack.txt"))
print(f"Log file path: {LOG_FILE}")

CHECK_INTERVAL = 1  # seconds between clipboard checks
MIN_LENGTH = 3      # ignore very short clipboard entries

def is_valid(content, last_clip):
    # Skip empty, repeated or too short content
    content = content.strip()
    if not content or content == last_clip:
        return False
    if len(content) < MIN_LENGTH:
        return False
    return True

def save_clip(content):
    now = datetime.now()
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            text = f.read()
            # Extract all entries with timestamp and content
            entries = re.findall(r"=== (.*?) ===\n(.*?)(?=\n===|\Z)", text, re.DOTALL)
            for timestamp_str, saved_content in entries:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                saved_content = saved_content.strip()
                if saved_content == content.strip():
                    # If duplicate saved within 1 day, skip saving
                    if now - timestamp < timedelta(days=1):
                        print("Skipped duplicate content saved within 1 day.")
                        return
    except FileNotFoundError:
        pass  # No file yet, proceed to save
    except Exception as e:
        print(f"Error opening log file: {e}")

    # Save new unique content
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n=== {timestamp} ===\n{content}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"Saved: {content[:40]}{'...' if len(content) > 40 else ''}")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def add_to_startup():
    # Add this program to Windows startup
    exe_path = os.path.abspath(sys.argv[0])
    key = winreg.HKEY_CURRENT_USER
    regpath = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(key, regpath, 0, winreg.KEY_SET_VALUE) as reg:
            winreg.SetValueEx(reg, "CopyTrack", 0, winreg.REG_SZ, exe_path)
            print("Added to startup.")
    except Exception as e:
        print(f"Failed to add to startup: {e}")

def main():
    print("CopyTrack started. Press CTRL+C to exit.")
    last_clip = ""

    while True:
        try:
            current_clip = pyperclip.paste().strip()
            if is_valid(current_clip, last_clip):
                last_clip = current_clip
                save_clip(current_clip)
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\nTerminated.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    add_to_startup()
    main()