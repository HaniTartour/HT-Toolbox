# -*- coding: utf-8 -*-
"""
Pick a Revit element and display info in a custom Windows Form (BIMBuddy style)
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
    Form, Label, Button, PictureBox, FormStartPosition, FormBorderStyle , GroupBox, Label
)
from System.Drawing import Point, Size, Font, FontStyle, Color, Image

import os
import System


# Revit doc refs
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# ----------------------------
# STEP 1: Pick one element
# ----------------------------
picked_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick an element")
element = doc.GetElement(picked_ref)

# Extract info
elem_id = str(element.Id)
elem_name = element.Name if hasattr(element, "Name") else element.GetType().Name
elem_cat = element.Category.Name if element.Category else "No Category"
level_name = "N/A"

# Try get Level if hosted
if hasattr(element, "LevelId") and element.LevelId != ElementId.InvalidElementId:
    level_elem = doc.GetElement(element.LevelId)
    if level_elem:
        level_name = level_elem.Name


# ----------------------------
# STEP 2: Show Windows Form
# ----------------------------
class PickedElementForm(Form):
    def __init__(self):
        self.Text = "Picked Element Info"
        self.Size = Size(400, 300)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "button.png")
        if os.path.exists(logo_path):
            logo = PictureBox()
            logo.Image = Image.FromFile(logo_path)
            logo.Size = Size(48, 48)
            logo.Location = Point(20, 20)
            self.Controls.Add(logo)

        # Title
        title = Label()
        title.Text = "Picked Revit Element"
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
        
        
        
        # Create the GroupBox
        group_box = GroupBox()
        group_box.Text = "Element Info"
        group_box.Font = Font("Segoe UI", 9, FontStyle.Bold)
        group_box.Size = Size(350, 110)
        group_box.Location = Point(20, 90)

        # Add labels inside the group box
        labels = {
            "ID": elem_id,
            "Name": elem_name,
            "Category": elem_cat,
            "Level": level_name
        }

        y = 20
        for label_text, value in labels.items():
            lbl = Label()
            lbl.Text = "{}: {}".format(label_text, value)
            lbl.Font = Font("Segoe UI", 9)
            lbl.AutoSize = True
            lbl.Location = Point(10, y)
            group_box.Controls.Add(lbl)
            y += 20

        # Add the group box to the form
        self.Controls.Add(group_box)

        
       

        # close Button
        btn = Button()
        btn.Text = "Close"
        btn.Size = Size(100, 30)
        btn.Location = Point(150, 220)
        btn.Click += lambda s, e: self.Close()
        self.Controls.Add(btn)


        #dd divider line before the buttons for layout clarity
        divider = Label()
        divider.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        divider.Location = Point(20, 210)
        divider.Size = Size(350, 2)
        self.Controls.Add(divider)


# Run it
from System.Windows.Forms import Application
form = PickedElementForm()
Application.Run(form)
