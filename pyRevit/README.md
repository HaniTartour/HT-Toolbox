[![About Me](https://img.shields.io/badge/About-Hani%20Tartour-orange?style=for-the-badge&logo=readthedocs)](https://hanitartour.github.io/about.html)

# 🧩 pyRevit Tools

All custom pyRevit buttons live here.


# 🧰 HT Toolbox – pyRevit Extensions

Welcome to the **pyRevit** extension library built by [Hani Tartour](https://www.linkedin.com/in/hanimtartour)!  
These tools are crafted to enhance productivity inside Autodesk Revit using **Python**, **Revit API**, **WinForms**, and **pyRevit**’s extensibility.

> ⚙️ Built for Revit Power Users, BIM Coordinators, and Automation Enthusiasts.

---

## 📦 Toolset Overview

| Tool | Description | Status |
|------|-------------|--------|
| 🔄 **Rename Views+** | Rename Revit views in bulk with live preview, filtering & branded UI | ✅ Stable |
| 📥 **Clone from GitHub** | Quickly clone and register pyRevit extensions directly from GitHub | ✅ Stable |
| 🎯 **Pick on Object** | Pick a Revit element and display detailed info in a sleek modal | ✅ Stable |
| 🧱 **Shaft Opening Converter** | Use Dynamo scripts to convert `Shaft Opening` to solids for review/export | ✅ Mixed (Dynamo + pyRevit) |
| ...More Coming Soon | View template matchers, smart QA flags, etc. | 🚧 In Development |

---

## 🧠 Why Use HT Toolbox?

- 🚀 Speeds up repetitive Revit tasks
- 🧩 Integrated with **pyRevit** UI panels
- 🎨 Custom branded Windows Forms (BIMBuddy style)
- 🧰 Built with **clean**, **commented**, and **modular** Python code
- 💡 Open-source, extensible, and built to scale

---

## 📁 Folder Structure
HT-Toolbox/
│
├── pyRevit/
│ └── HT-ToolBoxExtension/
│ ├── HT.extension/
│ │ ├── About.panel/
│ │ ├── BabyTools.panel/
│ │ │ └── PickOneObject.pushbutton/
│ │ ├── Dev.panel/
│ │ │ ├── 01RenameViewsPlus.pushbutton/
│ │ │ ├── 02CloneFromGitHub.pushbutton/
│ │ │ └── ...
│ │ └── extension.json
│ └── resources/
│ ├── icons/
│ ├── HT-logo.png
│ └── level.ico


---

## 🛠 Requirements

- Revit 2021+
- pyRevit v4.8+
- Python 2.7 (IronPython) – for compatibility with pyRevit scripts
- No external libraries required (WinForms only)

---

## 🚀 How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/HaniTartour/HT-Toolbox.git
2.Link your extension in pyRevit:
        
        pyrevit extensions add "C:\Path\To\HT-Toolbox\pyRevit\HT-ToolBoxExtension"
 3.Hit Reload in pyRevit — your HT tab should appear!
 
---

## 📄 Documentation
Each tool includes:

📝 .md Instruction Guide (tool_name-instructions_guide.md)

🧠 Comments inside each Python script

🎨 Branded UI for consistency

For example:

📄 Rename Views+ Guide

📄 Clone from GitHub Guide

📄 Shaft Converter Guide

---

## 🤝 Contribute
This is an open toolkit. Feel free to:

Suggest ideas

Submit issues

Fork & build your own tools

Let’s automate BIM workflows — the smart way.

---

## 📎 Licensing

These scripts are part of the **HT Toolbox**  
Created by [Hani Tartour](https://www.linkedin.com/in/hanimtartour) – 2025  
Released under the [MIT License](../LICENSE)  
Feel free to fork, adapt, or contribute!

---

⭐ Showcase Tools (with UI)
🎨 Branded Windows Forms

✅ Filters, checkboxes, grid previews

💾 Excel IO & view rename automation

🌐 Live GitHub integration

🧠 Revit-safe operations & error handling

Want a live demo? Visit my LinkedIn or check the YouTube channel!

---



