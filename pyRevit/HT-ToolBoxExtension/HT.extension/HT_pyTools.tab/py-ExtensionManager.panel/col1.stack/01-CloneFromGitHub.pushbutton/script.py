# -*- coding: utf-8 -*-
__title__ = "Clone From GitHub"
__doc__ = """Version = 1.0.0
Release Date = 26.06.2025
_______________________________________________________________
Description:
This is the pyRevit button entry script to:
1. Ask the user for a GitHub repo URL.
2. Run the CloneBuddy workflow.
_______________________________________________________________
Purpose: Clone a GitHub repo, validate and fix folder structure.
_______________________________________________________________
Author: Hani M Tartour
"""

# ----------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------
import os
import sys
from pyrevit import forms

# ----------------------------------------------------------
# LOAD CORE MODULE (CloneBuddyCore.py)
# ----------------------------------------------------------
# This assumes CloneBuddyCore.py is two levels up, under core script folder
core_path = os.path.abspath(os.path.join(__file__, "..", "..", "CloneBuddyCore.py"))
core_dir = os.path.dirname(core_path)

if core_dir not in sys.path:
    sys.path.append(core_dir)

try:
    from CloneBuddyCore import run_clonebuddy_workflow
except ImportError as e:
    forms.alert(
        title="CloneBuddy",
        msg="❌ Failed to load CloneBuddyCore.\n\nError:\n{}".format(str(e)),
        warn_icon=True
    )
    raise

# ----------------------------------------------------------
# ASK USER FOR GITHUB REPO URL
# ----------------------------------------------------------
repo_url = forms.ask_for_string(
    default="https://github.com/your-username/your-extension.git",
    prompt="Paste the GitHub repo URL to clone the extension:",
    title="CloneBuddy - GitHub Extension Cloner"
)

# ----------------------------------------------------------
# RUN WORKFLOW OR CANCEL
# ----------------------------------------------------------
if repo_url:
    try:
        run_clonebuddy_workflow(repo_url)
        forms.alert("✅ Clone complete.\nCheck your extensions folder.", title="CloneBuddy")
    except Exception as ex:
        forms.alert(
            title="CloneBuddy - Error",
            msg="❌ An error occurred while cloning:\n{}".format(str(ex)),
            warn_icon=True
        )
        raise
else:
    forms.alert("No URL entered. Clone cancelled.", title="CloneBuddy")
