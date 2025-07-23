import subprocess

def run_adb_command(command):
    full_cmd = ["adb", "shell"] + command.split()
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "⏱️ ADB command timed out"
    except Exception as e:
        return f"❌ ADB command failed: {e}"

def input_tap(x, y):
    return run_adb_command(f"input tap {x} {y}")

def input_swipe(x1, y1, x2, y2, duration=500):
    return run_adb_command(f"input swipe {x1} {y1} {x2} {y2} {duration}")

def input_text(text):
    safe_text = text.replace(" ", "%s")
    return run_adb_command(f"input text {safe_text}")

def key_event(keycode):
    return run_adb_command(f"input keyevent {keycode}")

def launch_app(package_name):
    return run_adb_command(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")

def get_foreground_activity():
    return run_adb_command("dumpsys window windows | grep mCurrentFocus")

def take_screenshot(save_path="screenshot.png"):
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/temp_screen.png"])
    subprocess.run(["adb", "pull", "/sdcard/temp_screen.png", save_path])
    subprocess.run(["adb", "shell", "rm", "/sdcard/temp_screen.png"])
    return f"📸 Screenshot saved to {save_path}"
