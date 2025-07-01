"""
-------- CloneBuddyCore.py --------
-------- Purpose: Clone a GitHub repo, validate and fix Folder structure--------
✅ Phase 1: CloneBuddyCore.py Blueprint
This core script will include 3 key features, built step-by-step:
Clone a GitHub repo to local path
Validate the folder structure
Fix the structure (auto-rename, generate missing extension.json)
"""

# -*- coding: utf-8 -*-

import os           #Interact with the operating system.
import subprocess   #Run external processes and shell commands.
import shutil       #File operations — high-level.
import json         #Parse and write JSON data (e.g., extension.json in PyRevit).
import sys          #Access Python runtime info and control system behavior.

# --- Settings  and varaibles ---
DEFAULT_CLONE_DIR = os.path.expanduser("~\\CloneBuddyExtensions")   #setting the default directory where GitHub extensions will be cloned.
PYREVIT_CLI = "pyrevit"                                             #This sets the command name to invoke the pyRevit CLI.
REPO_SUFFIX = ".extension"


# --- Utilities ---
"""
defining a simple logging function to prefix your messages with a recognizable tag — "[CloneBuddy]" 
 ,so that when your tool runs, the output is clear, branded, and easy to filter in the console.
"""
def log(msg):
    print("[CloneBuddy] " + msg)



def is_command_available(cmd):
    """Check if a command-line tool is available (e.g. git, pyrevit)."""
    return shutil.which(cmd) is not None


"""
checking whether a given extension is already registered in pyRevit, 
which is critical to avoid duplicate registrations or unnecessary operations.
"""
def is_registered(extension_name):
    """Check if the extension is already registered in pyRevit."""
    try:
        result = subprocess.run(
            [PYREVIT_CLI, "env"],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.lower()
        return extension_name.lower() in output
    except Exception as e:
        log(f"⚠ Could not check registration status: {e}")
        return False

#=========================================
# --- Step 1: Clone the GitHub Repo ---
#=========================================
"""
Clone a GitHub repo into the default pyRevit extensions folder,
 giving it a valid .extension suffix if it doesn’t have one.
"""

def clone_repo(repo_url, extension_name=None):
    """Clone a repo to the default pyRevit extensions folder."""
    if not extension_name:
        extension_name = repo_url.rstrip('/').split("/")[-1].replace(".git", "")

    if not extension_name.endswith(REPO_SUFFIX):
        extension_name += REPO_SUFFIX

    local_path = os.path.join(DEFAULT_CLONE_DIR, extension_name)

    if os.path.exists(local_path):
        log(f"Folder already exists: {local_path}. Skipping clone.")
        return local_path

    os.makedirs(DEFAULT_CLONE_DIR, exist_ok=True)
    log(f"Cloning into: {local_path}")

    try:
        subprocess.run(["git", "clone", repo_url, local_path], check=True)
        log("✅ Repo cloned successfully.")
        return local_path
    except subprocess.CalledProcessError as e:
        log(f"❌ Git clone failed: {e}")
        return None

#=================================================
# --- Step 2: Validate the Extension Structure ---
#=================================================

def validate_structure(extension_path):
    """Validate that the folder is a proper pyRevit extension."""
    log(f"🔍 Validating structure at: {extension_path}")

    issues = []

    # Check folder name
    if not extension_path.endswith(".extension"):
        issues.append("❌ Folder name must end with '.extension'")

    # Check extension.json
    json_path = os.path.join(extension_path, "extension.json")
    if not os.path.isfile(json_path):
        issues.append("❌ Missing extension.json file")
    else:
        try:
            with open(json_path, 'r') as f:
                json.load(f)
            log("✅ extension.json is valid JSON")
        except Exception as e:
            issues.append(f"❌ extension.json is invalid: {str(e)}")

    # Check at least one tab/panel/command:
    # Check for .pushbutton folder and .py file
    has_ui_tool = False
    for root, dirs, files in os.walk(extension_path):
        if root.endswith(".pushbutton") and any(f.endswith(".py") for f in files):
            has_ui_tool = True
            break

    if not has_ui_tool:
        issues.append("❌ No pushbutton UI found (missing .pushbutton folder with script)")

    if not issues:
        log("✅ Structure is valid")
    else:
        log("⚠ Structure issues found:")
        for issue in issues:
            log(issue)

    return issues


#=================================================
# --- Step 3: Auto-Fix the Extension Structure ---
#=================================================

def auto_fix_structure(extension_path):
    """Attempt to fix basic structural issues in a pyRevit extension."""
    log(f"🛠 Attempting to fix structure at: {extension_path}")
    changes_made = []

    # Rename folder if needed
    base_dir = os.path.dirname(extension_path)
    folder_name = os.path.basename(extension_path)
    if not folder_name.endswith(REPO_SUFFIX):
        fixed_name = folder_name + REPO_SUFFIX
        new_path = os.path.join(base_dir, fixed_name)
        os.rename(extension_path, new_path)
        extension_path = new_path
        folder_name = fixed_name
        changes_made.append(f"✅ Renamed folder to: {fixed_name}")

    # Create extension.json if missing
    json_path = os.path.join(extension_path, "extension.json")
    if not os.path.isfile(json_path):
        default_json = {
            "name": folder_name.replace(REPO_SUFFIX, ""),
            "author": "CloneBuddy",
            "description": "Auto-generated extension.json",
            "version": "1.0.0"
        }
        with open(json_path, "w") as f:
            json.dump(default_json, f, indent=4)
        changes_made.append("✅ Created default extension.json")

    # Add sample tab/panel if missing
    has_button = False
    for root, dirs, files in os.walk(extension_path):
        if root.endswith(".pushbutton") and any(f.endswith(".py") for f in files):
            has_button = True
            break

    if not has_button:
        sample_path = os.path.join(extension_path, "tab", "SamplePanel", "Sample.pushbutton")
        os.makedirs(sample_path, exist_ok=True)
        script_file = os.path.join(sample_path, "script.py")
        with open(script_file, "w") as f:
            f.write("# Sample pushbutton created by CloneBuddy\nprint('Hello from CloneBuddy!')\n")
        changes_made.append("✅ Created sample tab/panel/pushbutton structure")

    if changes_made:
        log("🧩 Auto-fix complete:")
        for msg in changes_made:
            log(msg)
    else:
        log("✅ No fixes needed — structure already valid")

    return extension_path



def run_clonebuddy_workflow(repo_url):
    if not is_command_available("git"):
        log("❌ Git is not available in your PATH. Please install Git CLI.")
        return
    elif not is_command_available(PYREVIT_CLI):
        log("❌ pyRevit CLI is not available in your PATH. Run 'pyrevit env' to verify.")
        return

    path = clone_repo(repo_url)
    if path:
        validate_structure(path)
        auto_fix_structure(path)






#============================
# Final Step - Test a repo_Url
#============================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_url = sys.argv[1]
    else:
        repo_url = "https://github.com/aussieBIMguru/guRoo.git"  # Default test repo

    if not is_command_available("git"):
        log("❌ Git is not available in your PATH. Please install Git CLI.")
    elif not is_command_available(PYREVIT_CLI):
        log("❌ pyRevit CLI is not available in your PATH. Run 'pyrevit env' to verify.")
    else:
        path = clone_repo(repo_url)
        if path:
            validate_structure(path)
            updated_path = auto_fix_structure(path)


