# -*- coding: utf-8 -*-
__title__ = "Validate Extension JSON"
__doc__ = "Checks all .extension folders for valid extension.json files and offers to fix broken/missing ones."

import os
import json
from pyrevit import forms

# ------------------------------------------
# Config
# ------------------------------------------
EXTENSION_SCAN_PATH = os.path.expanduser("~\\CloneBuddyExtensions")
REPO_SUFFIX = ".extension"

# Custom template based on pyRevit sharing guide
TEMPLATE_JSON = {
    "builtin": "False",
    "default_enabled": "True",
    "type": "extension",
    "rocket_mode_compatible": "False",
    "name": "",  # will be set dynamically
    "description": "Auto-generated extension.json by CloneBuddy",
    "author": "",
    "author_profile": "",
    "url": "",
    "website": "",
    "image": "",
    "dependencies": []
}

# ------------------------------------------
# Logger
# ------------------------------------------
def log(msg):
    print("[CheckJson] " + str(msg))


# ------------------------------------------
# Validate single extension.json
# ------------------------------------------
def validate_json_file(json_path):
    try:
        with open(json_path, 'r') as f:
            json.load(f)
        return True
    except Exception as e:
        return False


# ------------------------------------------
# Auto-create extension.json if needed
# ------------------------------------------
def create_json(path, ext_name):
    template = TEMPLATE_JSON.copy()
    template["name"] = ext_name.replace(REPO_SUFFIX, "")
    json_path = os.path.join(path, "extension.json")

    try:
        with open(json_path, "w") as f:
            json.dump(template, f, indent=4)
        log("✅ Created extension.json at {}".format(json_path))
        return True
    except Exception as e:
        log("❌ Failed to write JSON: {}".format(e))
        return False


# ------------------------------------------
# Main workflow
# ------------------------------------------
def run_check_json_workflow():
    if not os.path.exists(EXTENSION_SCAN_PATH):
        forms.alert("Scan path does not exist:\n{}".format(EXTENSION_SCAN_PATH), title="CheckJson")
        return

    folders = [f for f in os.listdir(EXTENSION_SCAN_PATH)
               if f.endswith(REPO_SUFFIX) and
               os.path.isdir(os.path.join(EXTENSION_SCAN_PATH, f))]

    if not folders:
        forms.alert("No .extension folders found in:\n{}".format(EXTENSION_SCAN_PATH), title="CheckJson")
        return

    valid = []
    broken = []

    for folder in folders:
        full_path = os.path.join(EXTENSION_SCAN_PATH, folder)
        json_path = os.path.join(full_path, "extension.json")

        if os.path.isfile(json_path):
            if validate_json_file(json_path):
                valid.append(folder)
                log("✅ Valid: " + folder)
            else:
                broken.append((folder, full_path))
                log("⚠ Invalid JSON: " + folder)
        else:
            broken.append((folder, full_path))
            log("⚠ Missing JSON: " + folder)

    # Report summary
    summary = "Valid: {}\nBroken or Missing: {}".format(len(valid), len(broken))
    log("🔍 Scan complete.\n" + summary)

    if not broken:
        forms.alert("All extension.json files are valid!\n\n" + summary, title="CheckJson")
        return

    # Ask to fix
    fix = forms.alert("Found {} extension(s) with missing/invalid extension.json.\n\nDo you want to auto-generate valid ones?".format(len(broken)),
                      title="CheckJson",
                      options=["Yes", "No"])

    if fix == "Yes":
        for folder, path in broken:
            success = create_json(path, folder)
            if success:
                log("🛠 Fixed: " + folder)
        forms.alert("Auto-fix complete.\n\nYou may now reload pyRevit to see updated extensions.", title="CheckJson")



# Run it
run_check_json_workflow()
