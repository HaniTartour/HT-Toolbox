[![About Me](https://img.shields.io/badge/About-Hani%20Tartour-orange?style=for-the-badge&logo=readthedocs)](https://hanitartour.github.io/about.html)

<p align="left">
  <img src="resources/BIMBuddy Logo-2d.png" width="300" alt="BIMBuddy Logo">

# 🧰 HT-Toolbox – Revit Automation Toolkit by Hani Tartour

Welcome to **HT-Toolbox**, a growing collection of smart, time-saving tools built for Autodesk Revit users.  
This open-source toolbox includes **pyRevit extensions**, **Dynamo automation scripts**, and custom **branded UIs** — all designed to supercharge BIM workflows with clarity, control, and class.  

> ⚡ Built for architects, engineers, BIM specialists, and Revit nerds who want to automate the boring and build the awesome.

---

## 📦 Toolkit Structure
HT-Toolbox/
│
├── pyRevit/ → Custom extensions built for pyRevit
│ ├── HT-ToolBoxExtension/
│ │ └── Dev.panel/
│ │ └── BabyTools.panel/
│ └── README.md → 🔗 Details of all pyRevit tools
│
├── dynamo/ → Dynamo scripts and guides
│ ├── Host-shaft to solid.dyn
│ ├── LinkedModel-shaft to solid.dyn
│ └── README.md → 🔗 Dynamo automation use cases
│
├── projects/ → Tool-specific HTML pages and guides
│ └── rename-views.html
│ └── clone-from-github.html
│ └── pick-one-object.html
│ └── shaft-opening-converter.html
│
├── assets/ → Logos, icons, screenshots
└── README.md → 👈 You're here


---

## 🧠 What’s Inside?

### 🛠 pyRevit Tools
Custom Revit buttons with UI, automation logic, and rich UX — all inside the **pyRevit** ribbon.

| Tool | Description |
|------|-------------|
| 🔄 [Rename Views+](projects/rename-views.html) | Batch rename views with live preview, filters, Excel I/O, and branded grid UI |
| 📥 [Clone From GitHub](projects/clone-from-github.html) | Clone pyRevit extensions directly from GitHub and auto-register them |
| 🎯 [Pick on Object](projects/pick-one-object.html) | Click on any Revit element and display its metadata in a branded modal |
| 🧱 [Shaft Opening Converter](projects/shaft-opening-converter.html) | Visualize shaft openings (host & linked models) as DirectShapes via Dynamo |

➡️ Explore full details in the [`pyRevit/README.md`](pyRevit/README.md)

---

### ⚙️ Dynamo Scripts

High-value Dynamo graphs for model data visualization, geometry generation, and QA processes.

| Tool | Description |
|------|-------------|
| 🧱 Shaft Opening to Solid (Host Model) | Converts host model shaft openings to solids using DirectShape |
| 🧱 Shaft Opening to Solid (Linked Model) | Scans linked models for shafts and visualizes them as solids |

➡️ See full documentation in [`dynamo/README.md`](dynamo/README.md)

---

## 🎯 Vision

This toolkit is a living, modular system focused on:

- 🔁 Automating Revit tasks
- 🧩 Enhancing model QA & clarity
- 🎨 Offering polished UX through branded forms
- 💡 Educating others through transparent scripting

The goal?  
**Turn chaos into clarity. Turn clicks into code. Turn BIM work into magic.**

---

## 🚀 Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/HaniTartour/HT-Toolbox.git
2.Link the pyRevit extension:
    
    pyrevit extensions add "C:\Path\To\HT-Toolbox\pyRevit\HT-ToolBoxExtension"
    pyrevit reload
3.Open any .dyn file inside Dynamo 2.6+ and hit Run!

---

## 🌐 Live Demos & Docs
🌐 Online Project Demos

📘 Tool Instructions & Guides

[📸 Screenshot Lightboxes & Feature Previews](each HTML project page)


---

## 🧩 Tech Stack
🐍 Python (IronPython for pyRevit)

🧠 Revit API

🔧 pyRevit SDK

💎 Windows Forms (for UI)

📐 Dynamo Visual Programming

---


## 🤝 Contributing
Have an idea? Want to improve a tool? Submit a PR or open an issue!
This repo is open for collaboration and knowledge-sharing.

---

## 🧑‍💻 Author
Made with 💙 by Hani M. Tartour
Follow my journey on YouTube and GitHub.

---

## 🚧 Coming Soon
🧮 View Template QA Tool

🗂 Parameter Consistency Checker

🌍 BIMBuddy Launcher App

🎨 Custom Branding Package for Forms

---

