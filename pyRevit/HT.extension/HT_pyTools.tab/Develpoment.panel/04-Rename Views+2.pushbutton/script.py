# -*- coding: utf-8 -*-
__title__ = "Rename Views+2"
__doc__ = """Version = 1.1.2
Release Date = 26.06.2025
_______________________________________________________________
Description:
Safely rename selected Revit views using Find/Replace, Prefix, and Suffix.
Includes Preview Mode with colored warnings, proper cancel handling,
and retry loop for safer user interaction.
_______________________________________________________________
Author: Hani M Tartour
"""

# ================================
# Revit & pyRevit Imports
# ================================
from Autodesk.Revit.DB import *
from pyrevit import revit, forms

# ================================
# .NET & UI Imports
# ================================
import clr
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Collections.Generic import List
from System.Drawing import Size, Point, Font, Color
from System.Windows.Forms import (
    Form, Label, Button, DialogResult, FormStartPosition,
    RichTextBox, AnchorStyles, RichTextBoxScrollBars
)

# ================================
# UI: Preview Rename Form
# ================================
class PreviewRenameForm(Form):
    def __init__(self, preview_lines):
        self.Text = "Preview Rename Actions"
        self.MinimumSize = Size(900, 600)
        self.Size = Size(900, 600)
        self.StartPosition = FormStartPosition.CenterScreen
        self.result = None

        # Label
        self.label = Label()
        self.label.Text = "Preview of the renamed views:"
        self.label.Location = Point(10, 10)
        self.label.Size = Size(860, 20)
        self.Controls.Add(self.label)

        # RichTextBox
        self.textbox = RichTextBox()
        self.textbox.ScrollBars = RichTextBoxScrollBars.Vertical
        self.textbox.Multiline = True
        self.textbox.ReadOnly = True
        self.textbox.Font = Font("Consolas", 9)
        self.textbox.Location = Point(10, 40)
        self.textbox.Size = Size(860, 450)
        self.textbox.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self.Controls.Add(self.textbox)

        # Populate lines with color
        # Clear textbox first
        self.textbox.Clear()

        for line in preview_lines:
            # Move caret to end of text
            self.textbox.SelectionStart = self.textbox.TextLength
            self.textbox.SelectionLength = 0

            # Set color before appending
            if "[⚠ Duplicate!" in line:
                self.textbox.SelectionColor = Color.Red
            elif line.startswith("Old:"):
                self.textbox.SelectionColor = Color.RoyalBlue
            else:
                self.textbox.SelectionColor = Color.Black

            # Add the line
            self.textbox.AppendText(line + "\n")

        # Optional: reset color back to black
        self.textbox.SelectionColor = Color.Black

        # Buttons
        self.rename_btn = Button()
        self.rename_btn.Text = "Rename"
        self.rename_btn.Size = Size(100, 30)
        self.rename_btn.Location = Point(760, 500)
        self.rename_btn.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self.rename_btn.Click += self.on_rename
        self.Controls.Add(self.rename_btn)
        self.AcceptButton = self.rename_btn

        self.back_btn = Button()
        self.back_btn.Text = "Back"
        self.back_btn.Size = Size(100, 30)
        self.back_btn.Location = Point(640, 500)
        self.back_btn.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self.back_btn.Click += self.on_back
        self.Controls.Add(self.back_btn)

        self.cancel_btn = Button()
        self.cancel_btn.Text = "Cancel"
        self.cancel_btn.Size = Size(100, 30)
        self.cancel_btn.Location = Point(520, 500)
        self.cancel_btn.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self.cancel_btn.Click += self.on_cancel
        self.Controls.Add(self.cancel_btn)

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
# Revit Document Setup
# ================================
uidoc = __revit__.ActiveUIDocument  # type: ignore
doc = uidoc.Document

# ================================
# Step 1: Select Views
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
# Step 2–4: Rename Options + Preview Loop
# ================================
from rpw.ui.forms import FlexForm, Label as FLabel, TextBox as FTextBox, Separator, Button as FButton

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

    preview_lines = []
    renamable_views = []

    header = "Old: {:40} | New: {:40}".format("Original Name", "Proposed Name")
    separator = "-" * 90
    preview_lines = [header, separator]

    proposed_names = set()  # <-- to catch duplicates within selection too

    for view in selected_views:
        original_name = view.Name
        new_name = original_name

        if find:
            new_name = new_name.replace(find, replace)
        new_name = prefix + new_name + suffix

        line = "Old: {:40} → New: {:40}".format(original_name, new_name)

        # Check against existing view names AND already proposed ones
        if ((new_name in existing_names and new_name != original_name) or
                (new_name in proposed_names)):
            line += " |  [⚠ Duplicate! Skipped]"
        else:
            renamable_views.append((view, new_name))
            proposed_names.add(new_name)  # <- track this name to catch duplicates in loop

        preview_lines.append(line)

    preview_form = PreviewRenameForm(preview_lines)
    result = preview_form.ShowDialog()

    if preview_form.result == "rename":
        break
    elif preview_form.result == "cancel":
        forms.alert("🚫 Rename operation cancelled by user.", title="Cancelled")
        script.exit()
    else:
        continue  # back to input

# ================================
# Step 5: Commit Rename Transaction
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
        print("⚠️ Error renaming '{}': {}".format(view.Name, str(e)))
        skipped_count += 1

t.Commit()

forms.alert("✅ Renamed {} views.\n⚠️ Skipped {} duplicate(s).".format(
    renamed_count, skipped_count), title="Done")
