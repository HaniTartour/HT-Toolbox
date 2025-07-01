# -*- coding: utf-8 -*-
# About BIMBuddy pushbutton
# This script shows an About dialog with branding and a link to GitHub

from pyrevit import forms
import webbrowser

# Show a basic info alert
result = forms.alert(
    title="About BIMBuddy",
    msg=("👋 Welcome to BIMBuddy!\n\n"
         "This Revit toolkit is built to support beginners and professionals with friendly tools "
         "powered by Python, Dynamo, and pyRevit.\n\n"
         "📦 Version: 1.0.0\n"
         "🛠️ By: Hani Tartour\n\n"
         "Would you like to visit the GitHub page?"),
    options=["Open GitHub", "Close"],
    footer="✨ Your Revit Companion"
)



# Optional action
if result == "Open GitHub":
    webbrowser.open("https://github.com/HaniTartour/HT-Toolbox")
