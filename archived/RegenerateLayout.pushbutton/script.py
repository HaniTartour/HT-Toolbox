# -*- coding: utf-8 -*-
"""
Regenerate the extension.json layout and show a branded confirmation form
"""

import os
import json
import clr
from pyrevit import script

# Windows Forms
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Drawing import Size, Point, Font, Color , FontStyle
from System.Windows.Forms import (
    Application, Form, Label, Button, FormStartPosition , FormBorderStyle 
)

# 🧠 Import branding helper from your shared lib
from ht_ui_branding import add_branding_logo

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
    def __init__(self):
        self.Text = "HT_pyTools | Layout Updated"
        self.Size = Size(480, 280)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog  # ✅ Use the proper enum
        self.BackColor = Color.White

        # ✅ Add the logo using shared branding helper - BIMBuddy Logo (if available)
        add_branding_logo(self)

        # 🔔 Message
        label = Label()
        label.Text = "extension.json was successfully updated!"
        label.Font = Font("Segoe UI", 11, FontStyle.Bold)
        label.ForeColor = Color.FromArgb(40, 40, 40)
        label.AutoSize = True
        label.Location = Point(90, 40)
        self.Controls.Add(label)

        # 📂 Open Folder
        btn_folder = Button()
        btn_folder.Text = "📂 Open Folder"
        btn_folder.Size = Size(130, 35)
        btn_folder.Location = Point(60, 100)
        btn_folder.Click += self.open_folder
        self.Controls.Add(btn_folder)

        # 📄 Open JSON
        btn_json = Button()
        btn_json.Text = "📝 Open JSON File"
        btn_json.Size = Size(130, 35)
        btn_json.Location = Point(250, 100)
        btn_json.Click += self.open_json
        self.Controls.Add(btn_json)

        # ✅ Close
        btn_close = Button()
        btn_close.Text = "Done"
        btn_close.Size = Size(100, 30)
        btn_close.Location = Point(190, 170)
        btn_close.Click += lambda s, e: self.Close()
        self.Controls.Add(btn_close)

    def open_folder(self, sender, args):
        os.startfile(os.path.dirname(EXT_JSON_PATH))

    def open_json(self, sender, args):
        os.startfile(EXT_JSON_PATH)

# 🚀 Show the confirmation window
Application.Run(LayoutUpdatedForm())
