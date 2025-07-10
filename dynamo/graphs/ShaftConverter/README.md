[![About Me](https://img.shields.io/badge/About-Hani%20Tartour-orange?style=for-the-badge&logo=readthedocs)](https://hanitartour.github.io/about.html)

<p align="left">
  <img src="resources/BIMBuddy Logo-2d.png" width="300" alt="BIMBuddy Logo">

# 🚧 Shaft Opening Converter (Dynamo Tool)

A Dynamo-based visualization tool that converts *shaft openings* from both host and linked Revit models into **DirectShape geometry** for clearer 3D inspection, export, and coordination.

---

## 🧠 Purpose

Shafts in Revit are often **voids** that disappear when exporting to platforms like Navisworks. This tool creates **solid geometry** for these openings so you can:

- View them easily in 3D
- Perform visual QA/QC
- Export them into **NWC** files for Navisworks

---

## 📂 Contents

| Script                                | Description                                  |
|---------------------------------------|----------------------------------------------|
| `Host-shaft to solid.dyn`             | Generates solids from shafts in the **host** model |
| `LinkedModel-shaft to solid.dyn`      | Extracts shaft openings from a **linked** model and renders them as solids in the host |

---

## 🧰 Requirements

- Revit 2022+
- Dynamo 2.x
- Active model with shaft openings (and linked models if needed)

---

## ✅ Features

- 🔍 Converts voids into **visual solids**
- 🔗 Supports both **host** and **linked** models
- 🖼️ Compatible with Navisworks export (solids appear in NWC)
- 📐 Maintains original shaft dimensions & positions
- 👁️ Useful for **clash detection** and drawing coordination

---

## 🚀 How to Use

1. Open your Revit model (host).
2. Launch **Dynamo**.
3. Open the appropriate `.dyn` script.
4. Follow prompts and **Run** the script.

---

## 📸 Screenshots

Coming soon!

---

## 📁 Repo Structure
HT-Toolbox/
└── Dynamo/
└── ShaftConverter/
├── Host-shaft to solid.dyn
├── LinkedModel-shaft to solid.dyn
└── README.md


---

## 📃 License

MIT License (if applicable)

---

## ✍️ Author

**Hani M. Tartour**  
🔗 [LinkedIn](https://www.linkedin.com/in/hanimtartour) | 🌐 [hanitartour.github.io](https://hanitartour.github.io)

---

Built with 💡 for BIM coordination.
