# -*- coding: utf-8 -*-
__title__ = "Refresh Extensions"
__doc__ = """Version = 1.2.0
Author: Hani M Tartour
-----------------------------------------
Refreshes the pyRevit ribbon by:
- Scanning CloneBuddyExtensions folder
- Registering unregistered .extension folders
- Reloading pyRevit
"""

import os
import subprocess
from pyrevit import forms

# ---------------------
# Configuration
# ---------------------
EXT_FOLDER = os.path.expanduser("~\\CloneBuddyExtensions")
PYREVIT_CLI = "pyrevit"
REPO_SUFFIX = ".extension"

# ---------------------
# Log helper
# ---------------------
def log(msg):
    print("[RefreshExtensions] " + str(msg))

# ---------------------
# Load pyRevit env output
# ---------------------
def get_loaded_extension_paths():
    try:
        proc = subprocess.Popen([PYREVIT_CLI, "env"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, _ = proc.communicate()
        return os.path.normcase(stdout.decode("utf-8", errors="ignore"))
    except Exception as e:
        log("❌ Failed to get pyRevit env: {}".format(e))
        return ""

# ---------------------
# Get .extension folders in the local directory
# ---------------------
def get_local_extensions():
    if not os.path.exists(EXT_FOLDER):
        return []
    return [name for name in os.listdir(EXT_FOLDER)
            if name.endswith(REPO_SUFFIX)
            and os.path.isdir(os.path.join(EXT_FOLDER, name))]

# ---------------------
# Register extension
# ---------------------
def register_extension(ext_path):
    try:
        subprocess.call([PYREVIT_CLI, "extend", "extensions", ext_path])
        log("📌 Registered: {}".format(ext_path))
    except Exception as e:
        log("❌ Failed to register extension: {}".format(e))

# ---------------------
# Reload pyRevit
# ---------------------
def reload_pyrevit():
    try:
        subprocess.call([PYREVIT_CLI, "reload"])
        log("🔁 pyRevit reloaded.")
    except Exception as e:
        log("❌ pyRevit reload failed: {}".format(e))

# ---------------------
# Main Logic
# ---------------------
def refresh_extensions():
    log("📡 Scanning CloneBuddyExtensions folder...")
    local = get_local_extensions()
    if not local:
        forms.alert("No .extension folders found in CloneBuddyExtensions.",
                    title="Refresh Extensions")
        log("📭 Nothing to register.")
        return

    env_output = get_loaded_extension_paths()
    missing = []

    for ext in local:
        ext_path = os.path.normpath(os.path.join(EXT_FOLDER, ext))
        if ext_path.lower() not in env_output:
            missing.append(ext_path)

    if not missing:
        forms.alert("All extensions are already registered and visible in pyRevit.",
                    title="Refresh Extensions")
        log("✅ No missing extensions.")
        return

    # Log what will be added
    log("🧩 Unregistered extensions found:")
    for ext in missing:
        log("   - {}".format(ext))

    user_choice = forms.alert(
        msg="{} new extension(s) found.\nRegister and reload now?".format(len(missing)),
        title="Refresh Extensions",
        options=["Yes", "No"]
    )

    if user_choice == "Yes":
        for ext_path in missing:
            register_extension(ext_path)
        reload_pyrevit()
    else:
        log("❎ User cancelled registration and reload.")

# ---------------------
# Run it
# ---------------------
refresh_extensions()



