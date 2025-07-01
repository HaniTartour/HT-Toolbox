# -*- coding: utf-8 -*-
"""
This is the pyRevit button entry script to:
1. Ask the user for a GitHub repo URL.
2. Run the CloneBuddy workflow.
"""

import os
import sys
import pyRevit

from pyrevit import forms

# Dynamically import the core module (adjust path if needed)
core_path = os.path.join(os.path.dirname(__file__), "..", "..", "CloneBuddyCore.py")
core_path = os.path.abspath(core_path)

if core_path not in sys.path:
    sys.path.append(os.path.dirname(core_path))

# Import your workflow function
from CloneBuddyCore import run_clonebuddy_workflow

# Ask the user for a GitHub repo URL
repo_url = forms.ask_for_string(
    default="https://github.com/your-username/your-extension.git",
    prompt="Paste the GitHub repo URL to clone the extension:",
    title="CloneBuddy - GitHub Extension Cloner"
)

if repo_url:
    run_clonebuddy_workflow(repo_url)
else:
    forms.alert("No URL entered. Clone cancelled.", title="CloneBuddy")
