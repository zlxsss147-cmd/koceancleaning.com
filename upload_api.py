#!/usr/bin/env python3
"""
Upload the local commit 84d37bb to GitHub `zlxsss147-cmd/koceancleaning.com` main
as a SINGLE commit via the Git Data API (blob -> tree -> commit -> ref).

Why single commit: the working tree has 250 new/changed files. Pushing them as
one commit triggers exactly ONE Cloudflare Pages build instead of 250.

Usage:
  python upload_api.py --dry-run            # verify, no token needed
  TOKEN=github_pat_xxx python upload_api.py # perform the real upload
  python upload_api.py <github_token>       # also accepted

Requires a GitHub fine-grained PAT with Contents: read&write on the repo.
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

REPO = "zlxsss147-cmd/koceancleaning.com"
API = f"https://api.github.com/repos/{REPO}"
COMMIT_MSG = "Revert homepage category cover images to original placeholder graphics"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_token():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        return sys.argv[1]
    return os.environ.get("TOKEN") or os.environ.get("GITHUB_TOKEN")


def api(method, path, token, data=None, dry=False):
    url = API + path
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "kocean-upload",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    if dry:
        # Do not actually send writes during a dry run.
        if method in ("POST", "PATCH", "PUT", "DELETE"):
            print(f"   [dry] {method} {path}")
            return {"sha": "dry-run-sha", "object": {"sha": "dry-run-sha"}}
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read().decode()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:400]
            if e.code in (502, 503, 429) and attempt < 4:
                wait = 2 ** attempt
                print(f"   [retry {attempt}] HTTP {e.code} on {method} {path}, wait {wait}s")
                time.sleep(wait)
                continue
            print(f"HTTP ERROR {e.code} on {method} {path}: {detail}")
            raise
        except Exception as e:  # noqa
            if attempt < 4:
                print(f"   [retry {attempt}] {e} on {method} {path}, wait 2s")
                time.sleep(2)
                continue
            raise


def git(*args):
    return subprocess.check_output(["git", *args], cwd=SCRIPT_DIR).decode()


def main():
    dry = "--dry-run" in sys.argv
    token = None if dry else get_token()
    if not dry and not token:
        print("ERROR: no token. Set TOKEN env or pass as arg, or use --dry-run.")
        sys.exit(2)

    os.chdir(SCRIPT_DIR)

    # 1. Remote parent (current main)
    ref = api("GET", "/git/refs/heads/main", token, dry=dry)
    parent = ref["object"]["sha"]
    commit = api("GET", f"/git/commits/{parent}", token, dry=dry)
    base_tree = commit["tree"]["sha"]
    print(f"Remote main (parent): {parent}")
    print(f"Base tree:            {base_tree}")

    # 2. Files changed in the local commit (with status to detect deletions)
    raw = git("diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD").strip()
    changes = []  # (status, path)
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        changes.append((parts[0], parts[1]))
    print(f"Files to upload:      {len(changes)}")
    for st, p in changes:
        print(f"   {st}  {p}")

    total_bytes = 0
    for st, f in changes:
        if st == "D":
            continue
        try:
            total_bytes += os.path.getsize(os.path.join(SCRIPT_DIR, f))
        except OSError:
            pass
    print(f"Total payload:        {total_bytes/1024/1024:.1f} MB")

    if dry:
        print("Dry run complete. Re-run WITHOUT --dry-run (with a token) to upload.")
        return

    # 3. Upload blobs + build tree entries
    entries = []
    idx = 0
    for st, f in changes:
        if st == "D":
            # Deletion: null sha removes the path from the tree.
            entries.append({"path": f, "mode": "100644", "type": "blob", "sha": None})
            idx += 1
            print(f"  delete [{idx}/{len(changes)}] {f}")
            continue
        content = subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{f}"], cwd=SCRIPT_DIR)
        b64 = base64.b64encode(content).decode()
        blob = api("POST", "/git/blobs", token, {"content": b64, "encoding": "base64"})
        entries.append({"path": f, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        idx += 1
        if idx % 25 == 0 or idx == len(changes):
            print(f"  blobs [{idx}/{len(changes)}] last={f}")

    # 4. Create tree
    tree = api("POST", "/git/trees", token, {"base_tree": base_tree, "tree": entries})
    tree_sha = tree["sha"]
    print(f"New tree: {tree_sha}")

    # 5. Create commit
    new_commit = api("POST", "/git/commits", token, {
        "message": COMMIT_MSG,
        "tree": tree_sha,
        "parents": [parent],
    })
    new_sha = new_commit["sha"]
    print(f"New commit: {new_sha}")

    # 6. Move main ref
    api("PATCH", "/git/refs/heads/main", token, {"sha": new_sha, "force": False})
    print("DONE. main now points to the new commit. Cloudflare will build once.")
    print(f"Live: https://koceancleaning.com/products/")


if __name__ == "__main__":
    main()
