# -*- coding: utf-8 -*-
__title__ = "Filter by Level"
__author__ = "Hani M Tartour"
__tooltip__ = "Filter picked elements by their Level"
__highlight__ = "orange"
__doc__ = """v1.0.0
-----------------------
Select elements, then filter them by the Level they are placed on.
Useful for organizing selections across floors or zones.
"""

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType
from RevitServices.Persistence import DocumentManager

from System.Windows.Forms import (
    Form, Label, Button, ComboBox, ListBox, PictureBox, FormStartPosition,
    FormBorderStyle, ComboBoxStyle, Application
)
from System.Drawing import Point, Size, Font, FontStyle, Image
from System.Collections.Generic import List
import os
import System
from System import Array, String

# Revit setup
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# ----------------------------
# STEP 1 – Select Elements
# ----------------------------
picked_refs = uidoc.Selection.PickObjects(ObjectType.Element, "Pick elements to filter by level")
elements = [doc.GetElement(ref) for ref in picked_refs]

# Get distinct levels from picked elements
level_dict = {}
for elem in elements:
    if hasattr(elem, "LevelId") and elem.LevelId != ElementId.InvalidElementId:
        level = doc.GetElement(elem.LevelId)
        if level:
            level_dict[level.Name] = level.Id

sorted_levels = sorted(level_dict.keys())

# ----------------------------
# STEP 2 – Show dropdown form to filter
# ----------------------------
class LevelFilterForm(Form):
    def __init__(self):
        self.Text = "Filter elements By Level"
        self.Size = Size(400, 350)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False

        # Branding Logo (optional)
        logo_path = os.path.join(os.path.dirname(__file__), "button.png")
        if os.path.exists(logo_path):
            logo = PictureBox()
            logo.Image = Image.FromFile(logo_path)
            logo.Size = Size(48, 48)
            logo.Location = Point(20, 20)
            self.Controls.Add(logo)

        # Title
        title = Label()
        title.Text = "Filter Elements By Level"
        title.Font = Font("Segoe UI", 12, FontStyle.Bold)
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

        # ComboBox label
        lbl = Label()
        lbl.Text = "Select a level:"
        lbl.Location = Point(30, 80)
        lbl.AutoSize = True
        self.Controls.Add(lbl)

        # Dropdown of levels
        self.level_combo = ComboBox()
        self.level_combo.Location = Point(30, 110)
        self.level_combo.Size = Size(320, 30)
        self.level_combo.DropDownStyle = ComboBoxStyle.DropDownList
        self.level_combo.Items.AddRange(Array[String](sorted_levels))

        if self.level_combo.Items.Count > 0:
            self.level_combo.SelectedIndex = 0
        self.Controls.Add(self.level_combo)

        # Filter Button
        filter_btn = Button()
        filter_btn.Text = "Filter"
        filter_btn.Size = Size(100, 30)
        filter_btn.Location = Point(30, 150)
        filter_btn.Click += self.apply_filter
        self.Controls.Add(filter_btn)

        # Results list
        self.result_list = ListBox()
        self.result_list.Location = Point(30, 200)
        self.result_list.Size = Size(320, 100)
        self.Controls.Add(self.result_list)

        # Store filtered elements
        self.filtered_elements = []
        
        # Divider line before OK
        divider = Label()
        divider.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        divider.Location = Point(30, 300)
        divider.Size = Size(320, 2)
        self.Controls.Add(divider)

        # OK Button (to finish professionally)
        ok_btn = Button()
        ok_btn.Text = "OK"
        ok_btn.Size = Size(100, 30)
        ok_btn.Location = Point(250, 150)
        ok_btn.Click += self.close_form
        self.Controls.Add(ok_btn)

        

    def apply_filter(self, sender, event):
        target_level_name = self.level_combo.SelectedItem
        target_level_id = level_dict.get(target_level_name)

        self.filtered_elements = [
            e for e in elements
            if hasattr(e, "LevelId") and e.LevelId == target_level_id
        ]

        # Update ListBox
        self.result_list.Items.Clear()
        for elem in self.filtered_elements:
            name = elem.Name if hasattr(elem, "Name") else elem.GetType().Name
            self.result_list.Items.Add("ID {} – {}".format(elem.Id, name))
            
           

        # Highlight in Revit
        if self.filtered_elements:
            elem_ids = List[ElementId]()
            for e in self.filtered_elements:
                elem_ids.Add(e.Id)
            uidoc.Selection.SetElementIds(elem_ids)
            
    def close_form(self, sender, event):
        self.Close()

# Run the form
Application.Run(LevelFilterForm())
