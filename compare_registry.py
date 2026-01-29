import winreg
import json
import datetime
import time


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

LOG_FILE = "registry_changes.log"


def log_change(change_type, location, name, value=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(
            f"{timestamp} | {change_type} | {location} | {name} | {value}\n"
        )


def read_registry(root_key, subkey_path):
    entries = {}
    try:
        registry_key = winreg.OpenKey(root_key, subkey_path)
        index = 0
        while True:
            name, value, _ = winreg.EnumValue(registry_key, index)
            entries[name] = value
            index += 1
    except OSError:
        pass
    return entries


def load_baseline():
    with open("baseline.json", "r") as file:
        return json.load(file)


def compare_registry():
    baseline = load_baseline()
    baseline_entries = baseline["registry_entries"]
    changes_found = False

    for label, (root, path) in REGISTRY_PATHS.items():
        print(f"\nChecking {label}...")
        current_entries = read_registry(root, path)
        old_entries = baseline_entries.get(label, {})

        # NEW
        for name in current_entries:
            if name not in old_entries:
                print(f"[NEW] {label} -> {name}")
                log_change("NEW", label, name, current_entries[name])
                changes_found = True

        # MODIFIED
        for name in current_entries:
            if name in old_entries:
                if current_entries[name] != old_entries[name]:
                    print(f"[MODIFIED] {label} -> {name}")
                    log_change("MODIFIED", label, name, current_entries[name])
                    changes_found = True

        # DELETED
        for name in old_entries:
            if name not in current_entries:
                print(f"[DELETED] {label} -> {name}")
                log_change("DELETED", label, name)
                changes_found = True

    if not changes_found:
        print("\nNo registry changes detected.")


if __name__ == "__main__":
    print("[*] Starting continuous registry monitoring (Ctrl+C to stop)")
    try:
        while True:
            compare_registry()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n[!] Monitoring stopped by user.")


