# -*- coding: utf-8 -*-
__title__ = "Check Extensions"
__doc__ = """Scan and report all extensions in CloneBuddyExtensions folder."""

import os
import json
import subprocess
from pyrevit import forms

# === SETTINGS ===
EXT_DIR = r"C:\Users\HaniTartour\CloneBuddyExtensions"
PYREVIT_CLI = "pyrevit"

# === UTILS ===
def log(msg):
    print("[CheckExtensions] " + msg)

def get_loaded_extensions():
    """Use pyrevit env CLI to detect loaded extensions."""
    try:
        result = subprocess.Popen([PYREVIT_CLI, "env"], stdout=subprocess.PIPE)
        stdout, _ = result.communicate()
        output = stdout.decode("utf-8")
        return output.lower()
    except:
        return ""

def analyze_extension_folder(path):
    """Check validity of a single .extension folder."""
    issues = []
    folder = os.path.basename(path)

    if not folder.endswith(".extension"):
        issues.append("❌ Name must end with '.extension'")

    ext_json = os.path.join(path, "extension.json")
    if not os.path.isfile(ext_json):
        issues.append("❌ Missing extension.json")
    else:
        try:
            with open(ext_json) as f:
                data = json.load(f)
            if "name" not in data:
                issues.append("❌ extension.json missing 'name'")
        except Exception as e:
            issues.append("❌ Invalid extension.json: {}".format(e))

    return issues

# === MAIN ===
loaded_env = get_loaded_extensions()
report = []

if not os.path.exists(EXT_DIR):
    forms.alert("CloneBuddyExtensions folder not found!", title="Error")
    raise Exception("Extension folder missing.")

for folder in os.listdir(EXT_DIR):
    full_path = os.path.join(EXT_DIR, folder)
    if not os.path.isdir(full_path):
        continue

    issues = analyze_extension_folder(full_path)
    is_loaded = folder.lower() in loaded_env
    status = "✅ Loaded" if is_loaded else "🚫 Not Loaded"
    if issues:
        status += " + Errors: " + ", ".join(issues)

    report.append("[{}] {}".format(folder, status))

# === SHOW RESULTS ===
if report:
    forms.alert("\n".join(report), title="CloneBuddy Extension Check")
else:
    forms.alert("No extensions found in the folder.", title="Nothing to check")
