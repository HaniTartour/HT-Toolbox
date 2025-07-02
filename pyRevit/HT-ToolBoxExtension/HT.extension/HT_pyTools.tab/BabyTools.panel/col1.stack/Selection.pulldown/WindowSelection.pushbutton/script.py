# -*- coding: utf-8 -*-
__title__ = "Window Selection"
__doc__ = """v1.0.0
--------------------------
Description:
This Python script is intended to select some elements 
from the project
--------------------------
Author: Hani M Tartour
"""
import clr

# Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# Revit UI (for selection, if needed)
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

# Revit Document Setup (pyrevit style) : Current document reference
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
# ---------------------------------------------
# 🚀 STEP 1: Get User Selection (assumes ModelCurves selected)
# ---------------------------------------------
selection_ids = uidoc.Selection.GetElementIds()
selected_elements = [doc.GetElement(ele_id) for ele_id in selection_ids]

# ---------------------------------------------
# ✅ Output Summary
# ---------------------------------------------
print("✅ Selected {} Elements.".format(len(selected_elements)))