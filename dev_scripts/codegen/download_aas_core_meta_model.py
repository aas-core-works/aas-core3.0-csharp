"""Download the meta-model to this directory."""

import pathlib
import os
import argparse
import sys
from typing import Dict, Union

import requests


GITHUB_API = "https://api.github.com"
OWNER = "aas-core-works"
REPO = "aas-core-meta"
REF = "main"
FILEPATH = "aas_core_meta/v3.py"


def _latest_commit_sha_for_path(
    owner: str, repo: str, ref: str, path: str, *, timeout: float = 15.0
) -> str:
    """
    Resolve the latest commit SHA on a ref for a specific path.

    Uses: GET /repos/{owner}/{repo}/commits?path=...&sha=...&per_page=1
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits"
    params: Dict[str, Union[str, int]] = {"path": path, "sha": ref, "per_page": 1}
    resp = requests.get(url, params=params, timeout=timeout)
    try:
        resp.raise_for_status()
    except requests.HTTPError as ex:
        raise RuntimeError(
            f"Failed to resolve latest commit for {owner}/{repo}:{ref} path={path} "
            f"({resp.status_code}): {resp.text}"
        ) from ex

    commits = resp.json()
    if not commits or not isinstance(commits, list):
        raise RuntimeError(
            "Could not determine latest commit SHA (empty API response)."
        )

    sha = commits[0].get("sha")
    if not sha or not isinstance(sha, str):
        raise RuntimeError("API did not return a valid commit SHA.")
    assert isinstance(sha, str)
    return sha


def _download_raw_from_commit(
    owner: str, repo: str, sha: str, path: str, *, timeout: float = 30.0
) -> str:
    """
    Download the raw file contents for a given commit SHA and path.
    """
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{path}"
    resp = requests.get(raw_url, timeout=timeout)
    try:
        resp.raise_for_status()
    except requests.HTTPError as ex:
        raise RuntimeError(
            f"Failed to download file from {raw_url} ({resp.status_code}): {resp.text}"
        ) from ex
    # We expect Python source, decode as text.
    return resp.text


def main() -> int:
    """Execute the main routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.parse_args()

    this_dir = pathlib.Path(os.path.realpath(__file__)).parent

    # 1) Get the latest commit SHA for the file on `main`.
    sha = _latest_commit_sha_for_path(OWNER, REPO, REF, FILEPATH)

    # 2) Download the exact file from that commit.
    content = _download_raw_from_commit(OWNER, REPO, sha, FILEPATH)

    # 3) Write to current_dir/v3_1.py, with the required comment
    #    at the beginning *and* at the end.
    pinned_url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{sha}/{FILEPATH}"
    banner = f"# Downloaded from: {pinned_url}\n"

    out_path = this_dir / "meta_model.py"
    # Overwrite unconditionally.
    out_path.write_text(f"{banner}{content.rstrip()}\n\n{banner}", encoding="utf-8")

    print(f"Wrote {out_path} (from commit {sha[:12]}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
