import importlib.util
import traceback
from device import adb_controller as adb  # Adjust the import if your file path is different
import os

def run_test_script(file_path):
    results = []

    filename = os.path.basename(file_path)
    if not (filename.startswith("test") and filename.endswith(".py")):
        results.append(("__filename_check__", "SKIPPED", "Script name must start with 'test' and end with '.py'"))
        return results

    try:
        # Load the test script dynamically
        spec = importlib.util.spec_from_file_location("dynamic_test", file_path)
        test_module = importlib.util.module_from_spec(spec)

        # Inject ADB utility functions into test module
        test_module.__dict__.update({
            "run_adb_command": adb.run_adb_command,
            "input_tap": adb.input_tap,
            "input_swipe": adb.input_swipe,
            "input_text": adb.input_text,
            "key_event": adb.key_event,
            "launch_app": adb.launch_app,
            "get_foreground_activity": adb.get_foreground_activity,
            "take_screenshot": adb.take_screenshot
        })

        # Execute script loading (can throw syntax error)
        spec.loader.exec_module(test_module)

        # Run all test functions starting with 'run'
        for attr in dir(test_module):
            if attr.startswith("run") and callable(getattr(test_module, attr)):
                try:
                    result = getattr(test_module, attr)()
                    if result is True:
                        status = "PASS"
                    elif result is False:
                        status = "FAIL"
                    else:
                        status = "FAIL"
                    log = f"{attr}() returned {result}"
                except Exception as e:
                    status = "ERROR"
                    log = f"{attr}() threw exception:\n{traceback.format_exc()}"
                results.append((attr, status, log))

    except Exception as e:
        results.append(("__load_error__", "ERROR", f"{e}\n{traceback.format_exc()}"))

    return results
