# -*- coding: utf-8 -*-
__title__ = "Rename Views+"
__doc__ = """Version = 1.0.1
Release Date    = 25.06.2025
________________________________________________________________
Description:
check duplicated view names , then Rename selected views using prefix, find/replace, and suffix.
________________________________________________________________
How-To Use:
1. you can select any views from project browser to rename it. 
2. if no views are selected , then you can select any views from selection window dialog.
3. use the find/replace logic with or without prefix and suffix.
4.a review checks for the duplicated view names before final renmaing.
_______________________________________________________________
Last Updates:
- [25.06.2025] v1.0.1 , Alpha Version.
________________________________________________________________
Author: Hani M Tartour"""

# ==================================================
# Revit & pyRevit Imports
# ==================================================
from Autodesk.Revit.DB import *
from pyrevit import revit, forms

# ==================================================
# .NET Imports
# ==================================================
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# ==================================================
# UI Form Components
# ==================================================
from rpw.ui.forms import FlexForm, Label, TextBox, Separator, Button

# ==================================================
# Revit Document Setup
# ==================================================
app   = __revit__.Application # type: ignore
uidoc = __revit__.ActiveUIDocument # type: ignore
doc   = uidoc.Document  # type: Document

# ==================================================
# Step 1: Get Views (from selection or prompt)
# ==================================================
selected_ids = uidoc.Selection.GetElementIds()
selected_elements = [doc.GetElement(id) for id in selected_ids]
selected_views = [v for v in selected_elements if isinstance(v, View) and not v.IsTemplate]

if not selected_views:
    selected_views = forms.select_views(multiple=True)
    selected_views = [v for v in selected_views if not v.IsTemplate]

if not selected_views:
    forms.alert("❌ No views were selected.\nPlease try again.", exitscript=True)

# ==================================================
# Step 2: Show Rename Options Form
# ==================================================
components = [
    Label('Find:'),       TextBox('find'),
    Label('Replace:'),    TextBox('replace'),
    Label('Prefix:'),     TextBox('prefix'),
    Label('Suffix:'),     TextBox('suffix'),
    Separator(),          Button('Rename Views')
]

form = FlexForm('Rename Views', components)
form.show()

user_input = form.values
if not user_input:
    script.exit() # type: ignore

# ==================================================
# Retrieve input safely
# ==================================================
prefix  = user_input["prefix"] if "prefix" in user_input else ""
find    = user_input["find"] if "find" in user_input else ""
replace = user_input["replace"] if "replace" in user_input else ""
suffix  = user_input["suffix"] if "suffix" in user_input else ""

# ==================================================
# Step 3: Collect All Existing View Names (avoid duplicates)
# ==================================================
all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
existing_names = set()
for v in all_views:
    if not v.IsTemplate: # type: ignore
        existing_names.add(v.Name)

# ==================================================
# Step 4: Rename Views with Duplication Check
# ==================================================
t = Transaction(doc, "Rename Views")
t.Start()

renamed_count = 0
skipped_count = 0

for view in selected_views:
    try:
        original_name = view.Name
        new_name = original_name

        if find in new_name:
            new_name = new_name.replace(find, replace)

        new_name = prefix + new_name + suffix

        if new_name in existing_names:
            print("⚠️ Skipped duplicate name: '{}' already exists.".format(new_name))
            skipped_count += 1
            continue

        view.Name = new_name
        existing_names.add(new_name)
        renamed_count += 1

    except Exception as e:
        print("⚠️ Could not rename view '{}': {}".format(original_name, str(e)))

t.Commit()

forms.alert("✅ Renamed {} views.\n⚠️ Skipped {} duplicate(s).".format(renamed_count, skipped_count), title="Done")
