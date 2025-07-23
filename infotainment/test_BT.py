from device.adb_controller import input_tap, input_text

def run_toggle_bluetooth():
    print("Running Bluetooth Toggle Test")
    input_tap(500, 300)  # Tap Bluetooth icon (example coordinates)
    return True

def run_type_text():
    print("Running Type Test")
    input_text("hello from automation")
    return True
