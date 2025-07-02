# -*- coding: utf-8 -*-
"""
Regenerate the extension.json layout and show a branded confirmation form
"""

import os
import json
import clr
from pyrevit import script

import os
import System

# Windows Forms
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (
    Form, Label, Button, PictureBox, DialogResult, LinkLabel, FormStartPosition , FormBorderStyle , ToolTip
)

from System.Drawing import Point, Size, Font, FontStyle, Color, Image

# --- CONFIG ---
EXT_DIR = r"C:\Users\HaniTartour\AppData\Roaming\GitHub\HT-Toolbox\pyRevit\HT-ToolBoxExtension\HT.extension"
TAB_NAME = "HT_pyTools.tab"
EXT_JSON_PATH = os.path.join(EXT_DIR, TAB_NAME, "extension.json")

# --- STEP 1: Regenerate extension.json ---
layout = {}
tab_path = os.path.join(EXT_DIR, TAB_NAME)
layout[TAB_NAME] = {}

for item in os.listdir(tab_path):
    if item.endswith(".panel"):
        panel_name = item.replace(".panel", "")
        panel_path = os.path.join(tab_path, item)
        buttons = [b for b in os.listdir(panel_path) if b.endswith(".pushbutton")]
        layout[TAB_NAME][panel_name] = {"col1.stack": buttons}

with open(EXT_JSON_PATH, "w") as f:
    json.dump(layout, f, indent=2)

# --- STEP 2: Show Success UI ---

class LayoutUpdatedForm(Form):
    def __init__(self, success, error_msg=""):
        self.Text = "HT_pyTools | Layout Updated"
        self.Size = Size(480, 300)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog  # ✅ Use the proper enum
        self.MaximizeBox = False

        # BIMBuddy Logo (if available)
        logo_path = os.path.join(os.path.dirname(__file__), "button.png")
        if os.path.exists(logo_path):
            logo = PictureBox()
            logo.Image = Image.FromFile(logo_path)
            logo.Size = Size(48, 48)
            logo.Location = Point(20, 20)
            self.Controls.Add(logo)

        # Title
        title = Label()
        title.Text = "BIMBuddy Toolkit"
        title.Font = Font("Segoe UI", 14, FontStyle.Bold)
        title.Location = Point(80, 25)
        title.AutoSize = True
        self.Controls.Add(title)
        
        # Subtitle
        subtitle = Label()
        subtitle.Text = "✨ Your Revit Companion"
        subtitle.Font = Font("Segoe UI", 10)
        subtitle.Location = Point(80, 55)
        subtitle.AutoSize = True
        self.Controls.Add(subtitle)


        # 🔔 Message
        label = Label()
        if success:
            label.Text = "✅ extension.json was successfully updated!"
            label.ForeColor = Color.Green
        else:
            label.Text = "⚠️ Failed to update extension.json"
            label.ForeColor = Color.Red
            
        label.Font = Font("Segoe UI", 11, FontStyle.Bold)
        label.AutoSize = True
        label.Location = Point(90, 80)
        self.Controls.Add(label)

        # Show detailed error if any
        if not success and error_msg:
            error_label = Label()
            error_label.Text = error_msg
            error_label.Font = Font("Segoe UI", 8)
            error_label.ForeColor = Color.DarkRed
            error_label.Location = Point(90, 110)
            error_label.Size = Size(350, 40)
            self.Controls.Add(error_label)
 
        # 📂 Open Folder
        btn_folder = Button()
        btn_folder.Text = "Open Folder"
        btn_folder.Size = Size(130, 35)
        btn_folder.Location = Point(60, 150)
        btn_folder.Click += self.open_folder
        self.Controls.Add(btn_folder)

        # 📄 Open JSON
        btn_json = Button()
        btn_json.Text = "Open JSON File"
        btn_json.Size = Size(130, 35)
        btn_json.Location = Point(250, 150)
        btn_json.Click += self.open_json
        self.Controls.Add(btn_json)

        # ✅ Close
        btn_close = Button()
        btn_close.Text = "Close"
        btn_close.Size = Size(100, 30)
        btn_close.Location = Point(170, 200)
        btn_close.Click += lambda s, e: self.Close()
        self.Controls.Add(btn_close)

        #dd ToolTip to the buttons for consistency
        tooltip = ToolTip()
        tooltip.SetToolTip(btn_folder, "Open folder containing extension.json")
        tooltip.SetToolTip(btn_json, "Open the extension.json file")
        tooltip.SetToolTip(btn_close, "Close this window")
        
        #dd divider line before the buttons for layout clarity
        divider = Label()
        divider.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        divider.Location = Point(20, 140)
        divider.Size = Size(430, 2)
        self.Controls.Add(divider)



    def open_folder(self, sender, args):
        os.startfile(os.path.dirname(EXT_JSON_PATH))

    def open_json(self, sender, args):
        os.startfile(EXT_JSON_PATH)
 

success = False
error_msg = ""

try:
    with open(EXT_JSON_PATH, "w") as f:
        json.dump(layout, f, indent=2)
    success = True
except Exception as e:
    success = False
    error_msg = str(e)

 
# --- STEP 3: Show the Form ---
from System.Windows.Forms import Application

form = LayoutUpdatedForm(success, error_msg)
Application.Run(form)

