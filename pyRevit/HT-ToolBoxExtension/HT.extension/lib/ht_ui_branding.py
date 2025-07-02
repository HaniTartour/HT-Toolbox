# ht_ui_branding.py
# Shared helper to add BIMBuddy/HT logo to custom Windows Forms

import os
import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (
    Form, Label, Button, PictureBox, DialogResult, LinkLabel, FormStartPosition , FormBorderStyle , ToolTip
)

from System.Drawing import Point, Size, Font, FontStyle, Color, Image


def add_branding_logo(form, image_name="button.png", location=Point(20, 20), size=Size(48, 48)):
    """
    Adds a BIMBuddy or HT logo to the top-left of a Windows Form.

    Parameters:
        form (Form): The Windows Form object to apply branding to.
        image_name (str): The logo filename (usually 'button.png' or 'HT-logo.png').
        location (Point): Top-left position for logo.
        size (Size): Width and height of the logo image.
    """
    logo_path = os.path.join(os.path.dirname(__file__), "button.png")
    if os.path.exists(logo_path):
        logo = PictureBox()
        logo.Image = Image.FromFile(logo_path)
        logo.Size = size
        logo.Location = location
        logo.SizeMode = PictureBoxSizeMode.Zoom
        form.Controls.Add(logo)
