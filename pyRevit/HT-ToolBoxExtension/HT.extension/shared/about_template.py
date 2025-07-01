# -*- coding: utf-8 -*-
"""
About Form Template for pyRevit Add‑ins
--------------------------------------
Built as a *drop‑in* replacement for the bespoke `AboutBIMBuddyForm` so you can
reuse the same polished UI in **any** tool inside your HT‑Toolbox extension.

How to use
~~~~~~~~~~
>>> from about_template import show_about_dialog
>>> show_about_dialog(
        title="BIMBuddy Toolkit",
        subtitle="Your Revit Companion",
        version="1.0.0",
        logo_path=__logo__,        # optional absolute path
        repo_url="https://github.com/HaniTartour/HT-Toolbox",
        changelog_path="changelog.txt",  # relative or absolute
        update_url="https://github.com/HaniTartour/HT-Toolbox/releases/latest"
    )

Key Features
~~~~~~~~~~~~
* Brandable title, subtitle, logo, and footer.
* Optional **GitHub** and **Check Updates** links.
* Optional **What's New** button that reads from a `changelog.txt` file.
* All strings are passed as parameters – *no hard‑coded text*.
* Works under IronPython 2.7 (pyRevit) with UTF‑8 encoding.

Feel free to extend or subclass `AboutFormTemplate` if you need more controls.
"""

import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (
    Form, Label, Button, PictureBox, DialogResult, LinkLabel, FormStartPosition,
    FormBorderStyle, MessageBox, MessageBoxButtons, MessageBoxIcon, ToolTip
)
from System.Drawing import Point, Size, Font, FontStyle, Color, Image
import os
import webbrowser


class AboutFormTemplate(Form):
    """Reusable Windows Form that displays branded About information."""

    # ---------------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------------
    def __init__(self,
                 title="Tool Name",
                 subtitle="",
                 version="0.0.0",
                 logo_path=None,
                 repo_url=None,
                 changelog_path=None,
                 update_url=None,
                 footer_text="HT-Toolbox · Built with pyRevit"):
        """Build the About form.

        Parameters
        ----------
        title : str
            Main heading of the dialog.
        subtitle : str
            Secondary tagline under the title.
        version : str
            Semantic version string displayed on the dialog.
        logo_path : str or None
            Absolute or relative path to a PNG logo/Icon (32‑64 px ideal).
        repo_url : str or None
            URL opened when the GitHub link is clicked.
        changelog_path : str or None
            Text file path read when the *What's New* button is pressed.
        update_url : str or None
            URL opened when the *Check for Updates* button is pressed.
        footer_text : str
            Branding footer shown in small gray text.
        """
        # Basic window properties ------------------------------------------------
        self.Text = "About " + title
        self.Size = Size(420, 320)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False

        # ------------------------------------------------------------------
        # Controls: Logo (optional)
        # ------------------------------------------------------------------
        if logo_path and os.path.exists(logo_path):
            logo = PictureBox()
            logo.Image = Image.FromFile(logo_path)
            logo.Size = Size(48, 48)
            logo.Location = Point(20, 20)
            self.Controls.Add(logo)
            text_x_offset = 80  # shift title right of logo
        else:
            text_x_offset = 20  # no logo, align left

        # ------------------------------------------------------------------
        # Title & Subtitle labels
        # ------------------------------------------------------------------
        lbl_title = Label()
        lbl_title.Text = title
        lbl_title.Font = Font("Segoe UI", 14, FontStyle.Bold)
        lbl_title.Location = Point(text_x_offset, 25)
        lbl_title.AutoSize = True
        self.Controls.Add(lbl_title)

        if subtitle:
            lbl_sub = Label()
            lbl_sub.Text = subtitle
            lbl_sub.Font = Font("Segoe UI", 10)
            lbl_sub.Location = Point(text_x_offset, 55)
            lbl_sub.AutoSize = True
            self.Controls.Add(lbl_sub)

        # ------------------------------------------------------------------
        # Version label
        # ------------------------------------------------------------------
        lbl_ver = Label()
        lbl_ver.Text = "Version: {0}".format(version)
        lbl_ver.Font = Font("Segoe UI", 9)
        lbl_ver.Location = Point(20, 100)
        lbl_ver.AutoSize = True
        self.Controls.Add(lbl_ver)

        # ------------------------------------------------------------------
        # GitHub / Repo link (optional)
        # ------------------------------------------------------------------
        if repo_url:
            lnk_repo = LinkLabel()
            lnk_repo.Text = "View on GitHub"
            lnk_repo.Location = Point(20, 130)
            lnk_repo.AutoSize = True
            lnk_repo.LinkClicked += lambda s, e: webbrowser.open(repo_url)
            self.Controls.Add(lnk_repo)

        # ------------------------------------------------------------------
        # Divider line
        # ------------------------------------------------------------------
        divider = Label()
        divider.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        divider.Location = Point(20, 160)
        divider.Size = Size(360, 2)
        self.Controls.Add(divider)

        # ------------------------------------------------------------------
        # Footer (branding)
        # ------------------------------------------------------------------
        lbl_footer = Label()
        lbl_footer.Text = footer_text
        lbl_footer.Font = Font("Segoe UI", 8)
        lbl_footer.ForeColor = Color.Gray
        lbl_footer.Location = Point(20, 170)
        lbl_footer.AutoSize = True
        self.Controls.Add(lbl_footer)

        # ------------------------------------------------------------------
        # Buttons row (Update, Changelog, Close)
        # ------------------------------------------------------------------
        btn_y = 230
        btn_spacing = 140

        # Check for Updates -------------------------------------------------
        if update_url:
            btn_update = Button()
            btn_update.Text = "Check for Updates"
            btn_update.Size = Size(130, 30)
            btn_update.Location = Point(20, btn_y)
            btn_update.Click += lambda s, e: webbrowser.open(update_url)
            self.Controls.Add(btn_update)

        # What's New (changelog) -------------------------------------------
        if changelog_path and os.path.exists(changelog_path):
            btn_changelog = Button()
            btn_changelog.Text = "What's New"
            btn_changelog.Size = Size(100, 30)
            btn_changelog.Location = Point(20 + btn_spacing, btn_y)
            btn_changelog.Click += lambda s, e: self._show_changelog(changelog_path)
            self.Controls.Add(btn_changelog)

        # Close -------------------------------------------------------------
        btn_close = Button()
        btn_close.Text = "Close"
        btn_close.Size = Size(80, 30)
        btn_close.Location = Point(300, btn_y)
        btn_close.DialogResult = DialogResult.OK
        self.Controls.Add(btn_close)

        # ------------------------------------------------------------------
        # Optional ToolTips (hover text)
        # ------------------------------------------------------------------
        tooltip = ToolTip()
        tooltip.SetToolTip(btn_close, "Close this window")
        if update_url:
            tooltip.SetToolTip(btn_update, "Open GitHub releases to check for latest version")
        if changelog_path:
            tooltip.SetToolTip(btn_changelog, "View detailed changelog")

    # ----------------------------------------------------------------------
    # Private helpers
    # ----------------------------------------------------------------------
    def _show_changelog(self, path):
        """Display changelog contents in a message box."""
        try:
            with open(path, "r") as f:
                content = f.read()
        except IOError:
            content = "Changelog file not found."  # fallback

        MessageBox.Show(content, "Changelog", MessageBoxButtons.OK, MessageBoxIcon.Information)


# -------------------------------------------------------------------------
# Convenience function -----------------------------------------------------
# -------------------------------------------------------------------------

def show_about_dialog(**kwargs):
    """Instantiate and show the about dialog with given keyword args."""
    dlg = AboutFormTemplate(**kwargs)
    dlg.ShowDialog()
