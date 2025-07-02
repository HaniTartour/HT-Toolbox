# -*- coding: utf-8 -*-
__title__ = "Pick One Object"
__doc__ = """v1.0.0
--------------------------
🧠 Description:
This baby tool picks one element from the Revit model.
Intended for beginner Revit API exploration.

✍️ Author: Hani M Tartour
"""

import clr

# Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# Revit UI Services (for access to UI + selection)
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

# pyRevit Built-in Access
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# ---------------------------------------------
# 🚀 STEP 1: Let user pick one element
# ---------------------------------------------
from Autodesk.Revit.UI.Selection import ObjectType

try:
    ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick one element in the model")
    element = doc.GetElement(ref)

    # ---------------------------------------------
    # ✅ Output Summary
    # ---------------------------------------------
    print("🎯 You picked: {}".format(element))
    print("🆔 Element ID: {}".format(element.Id))
    print("📦 Category: {}".format(element.Category.Name if element.Category else "None"))

except Exception as e:
    print("⚠️ Selection canceled or failed: {}".format(e))
