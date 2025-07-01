# update_version.py
# Auto-inserts new version header in changelog and optionally updates about_form.py

import os
import datetime

# === CONFIG ===
version = "1.2.0"
changelog_path = os.path.join(os.path.dirname(__file__), "changelog.txt")
about_form_path = os.path.join(os.path.dirname(__file__), "HT_pyTools.tab", "About.panel", "AboutBIMBuddy.pushbutton", "about_form.py")

# === Insert into changelog ===
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
new_entry = f"""
## [v{version}] - {date_str}
### 🚀 Added
- Describe new features here

### 🐞 Fixed
- Describe fixes here

### 🧼 Changed
- Describe UI tweaks or changes here
"""

with open(changelog_path, "r") as f:
    lines = f.readlines()

# Insert new version after header line
for idx, line in enumerate(lines):
    if line.strip().startswith("## [v"):
        lines.insert(idx, new_entry + "\n---\n")
        break
else:
    lines.append(new_entry)

with open(changelog_path, "w") as f:
    f.writelines(lines)

print(f"✅ Changelog updated with v{version}")

# === Update about_form.py (optional) ===
if os.path.exists(about_form_path):
    with open(about_form_path, "r") as f:
        code = f.read()
    updated_code = code.replace(
        'version.Text = "Version: ',
        f'version.Text = "Version: {version}"  # Updated automatically\n# version.Text = "Version: '
    )
    with open(about_form_path, "w") as f:
        f.write(updated_code)
    print("✅ About form version updated.")

