import winreg
import json
import datetime



# REGISTRY PATHS TO MONITOR
REGISTRY_PATHS = {
    "HKCU_Run": (
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    ),
    "HKCU_RunOnce": (
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    ),
    "HKLM_Run": (
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    ),
    "HKLM_RunOnce": (
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    ),
    "HKLM_Defender": (
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Policies\Microsoft\Windows Defender"
    )
}



# FUNCTION TO READ REGISTRY
def read_registry(root_key, subkey_path):
    entries = {}

    try:
        registry_key = winreg.OpenKey(root_key, subkey_path)
        index = 0

        while True:
            name, value, value_type = winreg.EnumValue(registry_key, index)
            entries[name] = value
            index += 1

    except OSError:
        # This error occurs when no more registry values are found
        pass

    return entries


# CREATE BASELINE
def create_baseline():
    baseline_data = {
        "timestamp": str(datetime.datetime.now()),
        "registry_entries": {}
    }

    for label, (root, path) in REGISTRY_PATHS.items():
        baseline_data["registry_entries"][label] = read_registry(root, path)

    with open("baseline.json", "w") as baseline_file:
        json.dump(baseline_data, baseline_file, indent=4)

    print("[+] Baseline created successfully as baseline.json")


# MAIN EXECUTION
if __name__ == "__main__":
    create_baseline()
