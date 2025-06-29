import requests

def find_pyrevit_repos(max_results=20):
    url = "https://api.github.com/search/repositories"
    params = {"q": "pyrevit language:python", "per_page": max_results}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    for item in resp.json().get("items", []):
        yield item["clone_url"]

from CloneBuddyCore import clone_repo, validate_structure, auto_fix_structure

def collect_from_github(limit=30):
    for url in find_pyrevit_repos(limit):
        print(f"\n→ Testing: {url}")
        path = clone_repo(url)
        if not path:
            continue
        issues = validate_structure(path)
        path = auto_fix_structure(path)
        issues = validate_structure(path)
        if not issues:
            print(f"[✔] {url} is valid and ready.")
            # Optionally add metadata to catalog.json here

