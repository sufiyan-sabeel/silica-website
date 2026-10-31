"""Capture the live Silica repository facts into tools/repo_status.json.

    python3 tools/fetch_repo_status.py

Uses the public GitHub API (no token needed for a handful of requests). Set
GITHUB_TOKEN in the environment to raise the rate limit. The build bakes these
values into the page; the site then refreshes them in the browser.
"""

import datetime
import json
import os
import urllib.request

REPO = "sufiyan-sabeel/silica"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repo_status.json")


def get(path):
    request = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "silica-website-build",
            **({"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"]}
               if os.environ.get("GITHUB_TOKEN") else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    repo = get("/repos/" + REPO)
    status = {
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "watchers": repo.get("subscribers_count"),
        "open_issues": repo.get("open_issues_count"),
        "size_kb": repo.get("size"),
        "language": repo.get("language"),
        "default_branch": repo.get("default_branch"),
        "pushed_at": repo.get("pushed_at"),
        "created_at": repo.get("created_at"),
        "license": (repo.get("license") or {}).get("spdx_id"),
        "html_url": repo.get("html_url"),
        "latest_release": None,
        "releases": [],
        "last_commit": None,
    }

    try:
        release = get("/repos/%s/releases/latest" % REPO)
        status["latest_release"] = {
            "tag": release.get("tag_name"),
            "name": release.get("name"),
            "published_at": release.get("published_at"),
            "url": release.get("html_url"),
        }
    except Exception as exc:  # noqa: BLE001
        print("latest release unavailable:", exc)

    try:
        releases = get("/repos/%s/releases?per_page=8" % REPO)
        status["releases"] = [
            {"tag": r.get("tag_name"), "name": r.get("name"),
             "published_at": r.get("published_at")}
            for r in releases
        ]
    except Exception as exc:  # noqa: BLE001
        print("releases unavailable:", exc)

    try:
        commits = get("/repos/%s/commits?per_page=1" % REPO)
        if commits:
            commit = commits[0]
            status["last_commit"] = {
                "sha": (commit.get("sha") or "")[:7],
                "message": ((commit.get("commit") or {}).get("message") or "").splitlines()[0],
                "date": ((commit.get("commit") or {}).get("committer") or {}).get("date"),
                "url": commit.get("html_url"),
            }
    except Exception as exc:  # noqa: BLE001
        print("commits unavailable:", exc)

    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(status, handle, indent=2)

    print("wrote %s" % OUT)
    print("  stars %s · forks %s · issues %s · release %s"
          % (status["stars"], status["forks"], status["open_issues"],
             (status["latest_release"] or {}).get("tag")))


if __name__ == "__main__":
    main()
