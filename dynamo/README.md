[![About Me](https://img.shields.io/badge/About-Hani%20Tartour-orange?style=for-the-badge&logo=readthedocs)](https://hanitartour.github.io/about.html)
<p align="left">
  <img src="../resources/BIMBuddy Logo-2d.png" width="300" alt="BIMBuddy Logo">

# 🔷 Dynamo Tools

Custom Dynamo graphs and nodes.

# 🧠 HT Toolbox – Dynamo Scripts

Welcome to the **Dynamo** tools section of the HT Toolbox!  
Here you'll find custom Dynamo workflows designed to support coordination, visualization, and automation inside Revit — especially for structural and MEP models.

---

## 📌 Current Tools

### 🔶 Shaft Opening Converter

Convert abstract Revit `Shaft Opening` elements into visualized **DirectShape solids**, improving visibility, comparison, and export readiness — especially for Navisworks coordination.

#### 🔧 Features
- Supports both:
  - **Host Project Openings** (e.g., structural model)
  - **Linked Model Openings** (e.g., architectural shaft openings)
- Creates visible geometry inside Revit for non-graphical opening elements
- Helps detect mismatches between architectural and structural shafts
- Keeps geometry lightweight using `DirectShape` creation
- Great for **Navisworks exports**, review, or QA sessions

#### 📁 Files
| Script | Description |
|--------|-------------|
| `Host-shaft to solid.dyn` | Converts shaft openings in the current (host) project |
| `LinkedModel-shaft to solid.dyn` | Extracts and solidifies shaft openings from linked Revit models |

#### 🖼 Screenshots
> (Place sample screenshots here if available)

---

## 🔗 Usage Notes

- Scripts are compatible with **Dynamo 2.x**.
- Open from the **Manage > Dynamo Player** or **Dynamo Editor** in Revit.
- No custom packages required.

---

## 📥 How to Use

1. Open your Revit project.
2. Launch **Dynamo** or **Dynamo Player**.
3. Browse to the script folder:
4. Choose the appropriate script for:
- Host Model
- or Linked Model
5. Run & inspect the generated solids!

---

## 📎 Licensing

These scripts are part of the **HT Toolbox**  
Created by [Hani Tartour](https://www.linkedin.com/in/hanimtartour) – 2025  
Released under the [MIT License](../LICENSE)  
Feel free to fork, adapt, or contribute!

---

## 🚀 More Dynamo Tools Coming Soon...

Stay tuned for:
- Level-based filtering
- Smart 3D annotations
- Sheet name validation
- View template matchers

---

