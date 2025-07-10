# -*- coding: utf-8 -*-
__title__ = "Rename Views+"
__doc__ = """Safely rename Revit views with Find/Replace, Prefix, Suffix.
Includes preview grid, duplicate checking, and cancel/back options.
Author: Hani M Tartour | Version: 1.2 | Date: 2025-06-26
"""

# ================================
# Revit & pyRevit Imports
# ================================
from Autodesk.Revit.DB import *
from pyrevit import revit, forms

# ================================
# .NET & Windows Forms Imports
# ================================
import clr
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Collections.Generic import List
from System.Drawing import Size, Point, Font, Color
from System.Windows.Forms import (
    Form, Label, Button, DialogResult, FormStartPosition,
    CheckBox, DataGridView, DataGridViewAutoSizeColumnsMode, AnchorStyles
)

# Optional - for FlexForm rename input UI
from rpw.ui.forms import FlexForm, Label as FLabel, TextBox as FTextBox, Separator, Button as FButton

# ================================
# Revit Document Setup
# ================================
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# ================================
# Preview Rename Grid Form
# ================================
class PreviewRenameGridForm(Form):
    def __init__(self, rows):
        self.Text = "Preview Rename Grid"
        self.MinimumSize = Size(950, 600)
        self.Size = Size(950, 600)
        self.StartPosition = FormStartPosition.CenterScreen
        self.original_rows = rows

        # Show Duplicates Checkbox
        self.dup_checkbox = CheckBox()
        self.dup_checkbox.Text = "Show only duplicates"
        self.dup_checkbox.Location = Point(10, 15)
        self.dup_checkbox.Width = 180
        self.dup_checkbox.Anchor = AnchorStyles.Top | AnchorStyles.Left
        self.dup_checkbox.CheckedChanged += self.toggle_duplicates
        self.Controls.Add(self.dup_checkbox)

        # DataGridView
        self.grid = DataGridView()
        self.grid.Location = Point(10, 50)
        self.grid.Size = Size(910, 440)
        self.grid.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self.grid.ReadOnly = True
        self.grid.AllowUserToAddRows = False
        self.grid.AllowUserToDeleteRows = False
        self.grid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        self.grid.ColumnCount = 3
        self.grid.Columns[0].Name = "Original View Name"
        self.grid.Columns[1].Name = "Proposed View Name"
        self.grid.Columns[2].Name = "Status"
        self.Controls.Add(self.grid)

        # Buttons
        self.rename_btn = Button()
        self.rename_btn.Text = "Rename"
        self.rename_btn.Size = Size(100, 30)
        self.rename_btn.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self.rename_btn.Click += self.on_rename
        self.Controls.Add(self.rename_btn)

        self.back_btn = Button()
        self.back_btn.Text = "Back"
        self.back_btn.Size = Size(100, 30)
        self.back_btn.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self.back_btn.Click += self.on_back
        self.Controls.Add(self.back_btn)

        self.cancel_btn = Button()
        self.cancel_btn.Text = "Cancel"
        self.cancel_btn.Size = Size(100, 30)
        self.cancel_btn.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self.cancel_btn.Click += self.on_cancel
        self.Controls.Add(self.cancel_btn)

        # Layout buttons relative to form
        self.Layout += self.position_buttons

        self.result = None
        self.load_rows(self.original_rows)

    def position_buttons(self, sender, args):
        btn_spacing = 110
        btn_y = self.ClientSize.Height - 45
        base_x = self.ClientSize.Width - (btn_spacing * 3) - 20

        self.cancel_btn.Location = Point(base_x, btn_y)
        self.back_btn.Location = Point(base_x + btn_spacing, btn_y)
        self.rename_btn.Location = Point(base_x + (btn_spacing * 2), btn_y)

    def load_rows(self, rows):
        self.grid.Rows.Clear()
        for old_name, new_name, is_duplicate in rows:
            row_index = self.grid.Rows.Add(old_name, new_name, "⚠ Duplicate!" if is_duplicate else "")
            if is_duplicate:
                self.grid.Rows[row_index].DefaultCellStyle.ForeColor = Color.Red

    def toggle_duplicates(self, sender, args):
        if self.dup_checkbox.Checked:
            filtered = [row for row in self.original_rows if row[2]]  # Only duplicates
        else:
            filtered = self.original_rows
        self.load_rows(filtered)

    def on_rename(self, sender, args):
        self.result = "rename"
        self.DialogResult = DialogResult.OK
        self.Close()

    def on_back(self, sender, args):
        self.result = "back"
        self.DialogResult = DialogResult.Retry
        self.Close()

    def on_cancel(self, sender, args):
        self.result = "cancel"
        self.DialogResult = DialogResult.Cancel
        self.Close()

# ================================
# Step 1: View Selection
# ================================
selected_ids = uidoc.Selection.GetElementIds()
selected_elements = [doc.GetElement(id) for id in selected_ids]
selected_views = [v for v in selected_elements if isinstance(v, View) and not v.IsTemplate]

if not selected_views:
    selected_views = forms.select_views(multiple=True)
    if not selected_views:
        forms.alert("❌ No views selected.\nScript cancelled by user.", title="Cancelled")
        script.exit()
    selected_views = [v for v in selected_views if not v.IsTemplate]

if not selected_views:
    forms.alert("❌ No valid views selected.\nScript cancelled.", title="Cancelled")
    script.exit()

# ================================
# Rename + Preview Loop
# ================================
all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
existing_names = set(v.Name for v in all_views if not v.IsTemplate)

while True:
    components = [
        FLabel('Find:'),       FTextBox('find'),
        FLabel('Replace:'),    FTextBox('replace'),
        FLabel('Prefix:'),     FTextBox('prefix'),
        FLabel('Suffix:'),     FTextBox('suffix'),
        Separator(),           FButton('Preview & Rename')
    ]
    form = FlexForm('Rename Views+', components)
    form.show()

    user_input = form.values
    if not user_input:
        forms.alert("❌ Rename cancelled by user.", title="Cancelled")
        script.exit()

    prefix  = user_input.get("prefix", "").strip()
    find    = user_input.get("find", "").strip()
    replace = user_input.get("replace", "").strip()
    suffix  = user_input.get("suffix", "").strip()

    rows = []
    renamable_views = []
    temp_name_check = set(existing_names)

    for view in selected_views:
        original_name = view.Name
        new_name = original_name.replace(find, replace) if find else original_name
        new_name = prefix + new_name + suffix

        is_duplicate = new_name in temp_name_check and new_name != original_name
        if not is_duplicate:
            temp_name_check.add(new_name)
            renamable_views.append((view, new_name))
        rows.append((original_name, new_name, is_duplicate))

    preview_form = PreviewRenameGridForm(rows)
    result = preview_form.ShowDialog()

    if preview_form.result == "rename":
        break
    elif preview_form.result == "cancel":
        forms.alert("🚫 Rename operation cancelled by user.", title="Cancelled")
        script.exit()
    else:
        continue  # back to form

# ================================
# Final Rename Execution
# ================================
t = Transaction(doc, "Rename Views")
t.Start()

renamed_count = 0
skipped_count = 0

for view, new_name in renamable_views:
    try:
        if new_name in existing_names:
            skipped_count += 1
            continue
        view.Name = new_name
        existing_names.add(new_name)
        renamed_count += 1
    except Exception as e:
        print("⚠ Error renaming '{}': {}".format(view.Name, str(e)))
        skipped_count += 1

t.Commit()

forms.alert("✅ Renamed {} views.\n⚠ Skipped {} duplicate(s).".format(renamed_count, skipped_count), title="Done")


#