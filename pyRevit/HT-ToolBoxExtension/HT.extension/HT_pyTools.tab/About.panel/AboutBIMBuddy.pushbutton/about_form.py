# -*- coding: utf-8 -*-
# about_form.py
# Custom Windows Form for BIMBuddy About panel

import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (
    Form, Label, Button, PictureBox, DialogResult, LinkLabel, FormStartPosition , FormBorderStyle , ToolTip
)

from System.Drawing import Point, Size, Font, FontStyle, Color, Image
import webbrowser
import os
import System




class AboutBIMBuddyForm(Form):
    def __init__(self):
        self.Text = "About BIMBuddy"
        self.Size = Size(400, 300)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog  # ✅ Use the proper enum
        self.MaximizeBox = False
  
        # BIMBuddy Logo (if available)
        logo_path = os.path.join(os.path.dirname(__file__), "button.png")
        if os.path.exists(logo_path):
            logo = PictureBox()
            logo.Image = Image.FromFile(logo_path)
            logo.Size = Size(48, 48)
            logo.Location = Point(20, 20)
            self.Controls.Add(logo)
                    
        # Title
        title = Label()
        title.Text = "BIMBuddy Toolkit"
        title.Font = Font("Segoe UI", 14, FontStyle.Bold)
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

        # Version Info
        version = Label()
        version.Text = "Version: 1.0.0"
        version.Font = Font("Segoe UI", 9)
        version.Location = Point(20, 100)
        version.AutoSize = True
        self.Controls.Add(version)

        # Link to GitHub
        link = LinkLabel()
        link.Text = "View on GitHub"
        link.Location = Point(20, 130)
        link.AutoSize = True
        link.LinkClicked += self.open_github
        self.Controls.Add(link)

        # Branding Footer
        footer = Label()
        footer.Text = "HT_pyTools · Built with pyRevit"
        footer.Font = Font("Segoe UI", 8)
        footer.ForeColor = Color.Gray
        footer.Location = Point(20, 170)  # Adjust if needed
        footer.AutoSize = True
        self.Controls.Add(footer)

        divider = Label()
        divider.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        divider.Location = Point(20, 160)
        divider.Size = Size(340, 2)
        self.Controls.Add(divider)


        # "What's New" Button
        btn_changelog = Button()
        btn_changelog.Text = "What's New"
        btn_changelog.Size = Size(100, 30)
        btn_changelog.Location = Point(170, 220)
        btn_changelog.Click += self.show_changelog
        self.Controls.Add(btn_changelog)
        
        
        # "Check for Updates" Button
        btn_update = Button()
        btn_update.Text = "Check for Updates"
        btn_update.Size = Size(130, 30)
        btn_update.Location = Point(20, 220)
        btn_update.Click += self.check_updates
        self.Controls.Add(btn_update)



        # Close Button
        btn_close = Button()
        btn_close.Text = "Close"
        btn_close.Size = Size(80, 30)
        btn_close.Location = Point(280, 220)
        btn_close.DialogResult = DialogResult.OK
        self.Controls.Add(btn_close)
        
        # adding buttons tooltips
        tooltip = ToolTip()
        tooltip.SetToolTip(btn_changelog, "View recent changes to BIMBuddy Toolkit")
        tooltip.SetToolTip(btn_close, "Close this window")
        tooltip.SetToolTip(btn_update, "Opens GitHub to check for the latest version")

        
        
    def show_changelog(self, sender, args):
        changelog_path = os.path.join(os.path.dirname(__file__), "changelog.txt")
        if os.path.exists(changelog_path):
            with open(changelog_path, "r") as f:
                content = f.read()
        else:
            content = "No changelog found."

        from System.Windows.Forms import MessageBox, MessageBoxButtons, MessageBoxIcon
        MessageBox.Show(content, "BIMBuddy Changelog", MessageBoxButtons.OK, MessageBoxIcon.Information) 

    def open_github(self, sender, args):
        webbrowser.open("https://github.com/HaniTartour/HT-Toolbox")
        
    def check_updates(self, sender, args):
        # Replace with your real GitHub release or repo URL
        webbrowser.open("https://github.com/HaniTartour/HT-Toolbox/releases/latest")
