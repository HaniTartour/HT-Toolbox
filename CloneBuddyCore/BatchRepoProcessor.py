# -*- coding: utf-8 -*-
# BatchRepoProcessor.py
# Purpose: Batch-process multiple pyRevit GitHub extensions using CloneBuddyCore

import os
import re
from CloneBuddyCore import clone_repo, validate_structure, auto_fix_structure,log

# -------------------------------
# Repo List to Process
# -------------------------------
REPO_URLS = [
    "https://github.com/GiuseppeDotto/pyM4B.extension",
    "https://github.com/eirannejad/pyRevit-Search",
    "https://github.com/marius311/pyRevit.neoCL",
    "https://github.com/derangedhk/pyRevit.Translator",
    "https://github.com/OpenRevit/pyrevit.sheetlink.extension",
    # Add more URLs as needed
]

# -------------------------------
# Logging Config
# -------------------------------
LOG_TO_FILE = True
LOG_FILE_PATH = os.path.expanduser("~/CloneBuddyBatchLog.txt")

# Open log file safely with UTF-8
if LOG_TO_FILE:
    try:
        log_file = open(LOG_FILE_PATH, "a", encoding="utf-8")
    except Exception as e:
        print(f"[BatchCloneBuddy] ❌ Failed to open log file: {e}")
        LOG_TO_FILE = False


# Strip emoji characters if needed (optional safety net)
def remove_emojis(text):
    emoji_pattern = re.compile(
        "[\U00010000-\U0010FFFF]",  # match all emoji codepoints
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


# Main logging wrapper
def batch_log(msg):
    tag = "[BatchCloneBuddy] " + msg
    print(tag)
    if LOG_TO_FILE:
        try:
            log_file.write(tag + "\n")
        except UnicodeEncodeError:
            log_file.write(remove_emojis(tag) + "\n")


# -------------------------------
# Main Process Loop
# -------------------------------
def process_all_repos():
    for repo_url in REPO_URLS:
        batch_log("\n" + "=" * 60)
        batch_log(f"📦 Processing: {repo_url}")
        try:
            path = clone_repo(repo_url)
            if not path:
                batch_log("⛔ Skipped — clone failed")
                continue

            issues = validate_structure(path)
            auto_fix_structure(path)
            issues = validate_structure(path)  # Re-validate after fix

            if issues:
                batch_log("⚠ Extension has unresolved issues. Skipping registration.")
                for i in issues:
                    batch_log(f"  - {i}")
            else:
                register_with_pyrevit(path)
                batch_log("✅ Fully processed and registered!")

        except Exception as e:
            batch_log(f"❌ Unexpected error: {str(e)}")


# -------------------------------
# Run it!
# -------------------------------
if __name__ == "__main__":
    process_all_repos()
    if LOG_TO_FILE:
        log_file.close()
        print(f"\n📝 Log saved at: {LOG_FILE_PATH}")
