# -*- coding: utf-8 -*-
__title__ = "Pick Revit Objects"
__author__ = "Hani M Tartour"
__highlight__ = "orange"
__tooltip__ = "Pick multiple Revit elements and view their info in a ListView"
__doc__ = """v1.1.0
---------------------------------------
Pick some Revit elements and view their details
(ID, Name, Category, Level) in a scrollable table.
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
    Form, Label, Button, PictureBox, FormStartPosition, FormBorderStyle,
    ListView, ColumnHeader, View, DockStyle
)
from System.Drawing import Point, Size, Font, FontStyle, Image
import os

# Revit API setup
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Pick multiple elements
picked_refs = uidoc.Selection.PickObjects(ObjectType.Element, "Pick some elements")
elements = [doc.GetElement(ref) for ref in picked_refs]

# ----------------------------
# Windows Form with ListView
# ----------------------------
class PickedElementsForm(Form):
    def __init__(self):
        self.Text = "Picked Revit Elements"
        self.Size = Size(600, 400)
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
        title.Text = "Picked Revit Elements"
        title.Font = Font("Segoe UI", 12, FontStyle.Bold)
        title.Location = Point(80, 25)
        title.AutoSize = True
        self.Controls.Add(title)

        # Subtitle
        subtitle = Label()
        subtitle.Text = "✨ Multi-element Viewer"
        subtitle.Font = Font("Segoe UI", 10)
        subtitle.Location = Point(80, 55)
        subtitle.AutoSize = True
        self.Controls.Add(subtitle)

        # ListView setup
        list_view = ListView()
        list_view.View = View.Details
        list_view.FullRowSelect = True
        list_view.GridLines = True
        list_view.Size = Size(540, 220)
        list_view.Location = Point(20, 100)

        # Define columns
        columns = ["ID", "Name/Type", "Category", "Level"]
        widths = [80, 160, 140, 120]
        for i, col in enumerate(columns):
            list_view.Columns.Add(col, widths[i])

        # Populate list with element info
        for elem in elements:
            eid = str(elem.Id)
            ename = elem.Name if hasattr(elem, "Name") else elem.GetType().Name
            ecat = elem.Category.Name if elem.Category else "No Category"
            level_name = "N/A"
            if hasattr(elem, "LevelId") and elem.LevelId != ElementId.InvalidElementId:
                level_elem = doc.GetElement(elem.LevelId)
                if level_elem: level_name = level_elem.Name

            item = list_view.Items.Add(eid)
            item.SubItems.Add(ename)
            item.SubItems.Add(ecat)
            item.SubItems.Add(level_name)

        self.Controls.Add(list_view)

        # Close button
        close_btn = Button()
        close_btn.Text = "Close"
        close_btn.Size = Size(100, 30)
        close_btn.Location = Point(250, 330)
        close_btn.Click += lambda s, e: self.Close()
        self.Controls.Add(close_btn)

# Launch
from System.Windows.Forms import Application
Application.Run(PickedElementsForm())
