# -*- coding: utf-8 -*-
__title__ = "Grouped View Selector"
__doc__ = "Select views grouped by discipline with checkboxes using Windows Forms"


import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import (
    Form, Button, Label, CheckBox, CheckedListBox, GroupBox,
    FormStartPosition, DialogResult, ScrollableControl, AnchorStyles
)

from System.Drawing import Size, Point, Font, FontStyle


# Revit & .NET Imports
from Autodesk.Revit.DB import *
from pyrevit import revit, script

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import (
    Application, Form, Button, CheckBox, Label, Panel,
    DialogResult, GroupBox, ScrollableControl, DockStyle
)
from System.Drawing import Point, Size, Font

# Get Revit document
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# -------------------------------
# GROUP VIEWS BY DISCIPLINE
# -------------------------------


discipline_map = {
    "Architectural": [ViewType.FloorPlan, ViewType.CeilingPlan],
    "Structural": [ViewType.FloorPlan, ViewType.Section],
    "MEP": [ViewType.EngineeringPlan, ViewType.Detail],
    "3D Views": [ViewType.ThreeD],
    "Sheets": [ViewType.DrawingSheet],
    "Other": []  # fallback group
}


def get_grouped_views(doc):
    all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
    grouped = {d: [] for d in discipline_map.keys()}
    for v in all_views:
        if v.IsTemplate or v.ViewType == ViewType.Internal:
            continue
        matched = False
        for d_name, vtypes in discipline_map.items():
            if v.ViewType in vtypes:
                grouped[d_name].append(v)
                matched = True
                break
        if not matched:
            grouped["Other"].append(v)
    return grouped

# -------------------------------
# UI Form: Grouped Checkbox List
# -------------------------------
class ViewSelectorForm(Form):
    def __init__(self, grouped_views):
        self.Text = "Grouped View Selector"
        self.Size = Size(500, 600)
        self.MinimumSize = Size(400, 400)
        self.StartPosition = FormStartPosition.CenterScreen
        self.selected_views = []

        # Scrollable Panel
        scroll = Panel()
        scroll.AutoScroll = True
        scroll.Dock = DockStyle.Top
        scroll.Height = 500
        self.Controls.Add(scroll)

        y = 10
        self.checkboxes = []

        for group_name, views in grouped_views.items():
            if not views:
                continue

            groupbox = GroupBox()
            groupbox.Text = group_name
            groupbox.Font = Font("Segoe UI", 9, FontStyle.Bold)
            groupbox.Location = Point(10, y)
            groupbox.Size = Size(450, 30 + len(views) * 25)
            groupbox.AutoSize = True

            inner_y = 20
            for v in sorted(views, key=lambda x: x.Name):
                cb = CheckBox()
                cb.Text = v.Name
                cb.Tag = v
                cb.Location = Point(10, inner_y)
                cb.Width = 400
                groupbox.Controls.Add(cb)
                self.checkboxes.append(cb)
                inner_y += 22

            scroll.Controls.Add(groupbox)
            y += groupbox.Height + 10

        # OK Button
        ok_btn = Button()
        ok_btn.Text = "OK"
        ok_btn.Location = Point(370, 510)
        ok_btn.Click += self._collect_checked
        self.Controls.Add(ok_btn)

    def _collect_checked(self, sender, args):
        self.selected_views = [cb.Tag for cb in self.checkboxes if cb.Checked]
        self.DialogResult = DialogResult.OK
        self.Close()

# -------------------------------
# Run the UI and return selected views
# -------------------------------
grouped_views = get_grouped_views(doc)
form = ViewSelectorForm(grouped_views)

if form.ShowDialog() == DialogResult.OK:
    selected = form.selected_views
    if not selected:
        script.exit("❌ No views selected.")
    else:
        for v in selected:
            print("✅", v.Name)
else:
    script.exit("⛔ Cancelled by user.")
