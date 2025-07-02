# -*- coding: utf-8 -*-
"""
-------- CloneBuddyCore.py --------
Purpose: Clone a GitHub repo, validate and fix folder structure for pyRevit.
✅ Phase 1 - Core Features:
- Clone a GitHub repo to a local path
- Validate the folder structure
- Auto-fix structure (rename, generate extension.json, add pushbutton)
"""

import os
import subprocess
import json

# -------------------------------
# Settings
# -------------------------------
DEFAULT_CLONE_DIR = os.path.expanduser("~\\CloneBuddyExtensions")
PYREVIT_CLI = "pyrevit"
REPO_SUFFIX = ".extension"

# -------------------------------
# Default JSON Template
# -------------------------------
TEMPLATE_JSON = {
    "type": "extension",
    "rocket_mode_compatible": "False",
    "author_profile": "",
    "author": "",
    "url": "",
    "image": "",
    "name": "",
    "builtin": "False",
    "default_enabled": "True",
    "description": "Auto-generated extension.json by CloneBuddy",
    "dependencies": [],
    "website": ""
}

# -------------------------------
# Logger
# -------------------------------
def log(msg):
    print("[CloneBuddy] " + str(msg))

# -------------------------------
# Command Checker (IronPython-safe)
# -------------------------------
def is_command_available(cmd):
    for path in os.environ["PATH"].split(os.pathsep):
        full_path = os.path.join(path.strip('"'), cmd)
        if os.path.isfile(full_path) or os.path.isfile(full_path + ".exe"):
            return True
    return False

# -------------------------------
# Clone GitHub Repo
# -------------------------------
def clone_repo(repo_url, extension_name=None):
    repo_url = repo_url.strip()
    if not extension_name:
        extension_name = repo_url.rstrip('/').split("/")[-1].replace(".git", "")
    if not extension_name.endswith(REPO_SUFFIX):
        extension_name += REPO_SUFFIX
    local_path = os.path.join(DEFAULT_CLONE_DIR, extension_name)
    if os.path.exists(local_path):
        log("Folder already exists: {}. Skipping clone.".format(local_path))
        return local_path
    if not os.path.exists(DEFAULT_CLONE_DIR):
        os.makedirs(DEFAULT_CLONE_DIR)
    log("Cloning into: {}".format(local_path))
    try:
        process = subprocess.Popen(["git", "clone", repo_url, local_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            err_msg = stderr.decode("utf-8", errors="ignore") if stderr else "Unknown error"
            log("❌ Git clone failed: {}".format(err_msg.strip()))
            return None
        log("✅ Repo cloned successfully.")
        return local_path
    except Exception as e:
        log("❌ Git clone exception: {}".format(e))
        return None

# -------------------------------
# Validate Extension Structure
# -------------------------------
def validate_structure(extension_path):
    log("🔍 Validating structure at: {}".format(extension_path))
    issues = []
    if not extension_path.endswith(REPO_SUFFIX):
        issues.append("❌ Folder name must end with '.extension'")
    json_path = os.path.join(extension_path, "extension.json")
    if not os.path.isfile(json_path):
        issues.append("❌ Missing extension.json file")
    else:
        try:
            with open(json_path, 'r') as f:
                json.load(f)
            log("✅ extension.json is valid JSON")
        except Exception as e:
            issues.append("❌ extension.json is invalid: {}".format(str(e)))
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

# -------------------------------
# Create extension.json file
# -------------------------------
def create_json(path, ext_name, repo_url):
    template = TEMPLATE_JSON.copy()
    template["name"] = ext_name.replace(REPO_SUFFIX, "")
    template["url"] = repo_url.strip()
    template["author"] = "Auto-Generated"
    template["author_profile"] = "Auto-Generated"
    json_path = os.path.join(path, "extension.json")
    try:
        with open(json_path, "w") as f:
            json.dump(template, f, indent=4)
        log("✅ Created extension.json at {}".format(json_path))
        return True
    except Exception as e:
        log("❌ Failed to write JSON: {}".format(e))
        return False

# -------------------------------
# Auto-Fix Extension Structure
# -------------------------------
def auto_fix_structure(extension_path, repo_url):
    log("🛠 Attempting to fix structure at: {}".format(extension_path))
    changes_made = []
    base_dir = os.path.dirname(extension_path)
    folder_name = os.path.basename(extension_path)
    if not folder_name.endswith(REPO_SUFFIX):
        fixed_name = folder_name + REPO_SUFFIX
        new_path = os.path.join(base_dir, fixed_name)
        os.rename(extension_path, new_path)
        extension_path = new_path
        folder_name = fixed_name
        changes_made.append("✅ Renamed folder to: {}".format(fixed_name))
    json_path = os.path.join(extension_path, "extension.json")
    if not os.path.isfile(json_path):
        success = create_json(extension_path, folder_name, repo_url)
        if success:
            changes_made.append("✅ Created extension.json")
    has_button = False
    for root, dirs, files in os.walk(extension_path):
        if root.endswith(".pushbutton") and any(f.endswith(".py") for f in files):
            has_button = True
            break
    if not has_button:
        sample_path = os.path.join(extension_path, "tab", "SamplePanel", "Sample.pushbutton")
        try:
            if not os.path.exists(sample_path):
                os.makedirs(sample_path)
            script_file = os.path.join(sample_path, "script.py")
            with open(script_file, "w") as f:
                f.write("# Sample pushbutton created by CloneBuddy\nprint('Hello from CloneBuddy!')\n")
            changes_made.append("✅ Created sample tab/panel/pushbutton structure")
        except Exception as e:
            log("❌ Failed to create sample structure: {}".format(e))
    if changes_made:
        log("🧩 Auto-fix complete:")
        for msg in changes_made:
            log(msg)
    else:
        log("✅ No fixes needed — structure already valid")
    return extension_path

# -------------------------------
# Run Workflow
# -------------------------------
def run_clonebuddy_workflow(repo_url):
    if not is_command_available("git"):
        log("❌ Git is not available in your PATH.")
        return
    if not is_command_available(PYREVIT_CLI):
        log("❌ pyRevit CLI is not available.")
        return
    path = clone_repo(repo_url)
    if path:
        validate_structure(path)
        auto_fix_structure(path, repo_url)
