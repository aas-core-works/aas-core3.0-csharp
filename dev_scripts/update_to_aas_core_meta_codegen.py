"""
Update everything in this project to the latest aas-core-meta, -codegen.

Git is expected to be installed.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
from typing import Optional


def _make_sure_no_changed_files(
    repo_dir: pathlib.Path, expected_branch: str
) -> Optional[int]:
    """
    Make sure that no files are modified in the given repository.

    Return exit code if something is unexpected.
    """
    diff_name_status = subprocess.check_output(
        ["git", "diff", "--name-status", expected_branch],
        cwd=str(repo_dir),
        encoding="utf-8",
    ).strip()

    if len(diff_name_status.splitlines()) > 0:
        print(
            f"The following files are modified "
            f"compared to branch {expected_branch!r} in {repo_dir}:\n"
            f"{diff_name_status}\n"
            f"\n"
            f"Please stash the changes first before you update to aas-core-meta.",
            file=sys.stderr,
        )
        return 1

    return None


def _regenerate_code(our_repo: pathlib.Path) -> Optional[int]:
    """
    Call codegen script.

    Return an error code, if any.
    """
    codegen_dir = our_repo / "dev_scripts/codegen"

    meta_model_path = our_repo / "dev_scripts/codegen/meta_model.py"

    target_dir = our_repo

    print(f"Starting to run codegen script")
    start = time.perf_counter()

    proc = subprocess.run(
        [
            sys.executable,
            "codegen.py",
            "--meta_model",
            str(meta_model_path),
            "--target",
            str(target_dir),
        ],
        cwd=str(codegen_dir),
    )

    if proc.returncode != 0:
        return proc.returncode

    duration = time.perf_counter() - start
    print(f"Generating the code took: {duration:.2f} seconds.")

    return None


def _reformat_code(our_repo: pathlib.Path) -> None:
    """Reformat the generated code."""
    print("Re-formatting the C# code...")
    subprocess.check_call(["powershell", "./FormatCode.ps1"], cwd=our_repo / "src")


def _run_tests_and_rerecord(our_repo: pathlib.Path) -> None:
    """Run the tests with the environment variables set to re-record."""
    print("Running tests & re-recording the test traces...")

    env = os.environ.copy()
    env["AAS_CORE_AAS3_0_TESTS_TEST_DATA_DIR"] = str(our_repo / "test_data")
    env["AAS_CORE_AAS3_0_TESTS_RECORD_MODE"] = "true"

    subprocess.check_call(["dotnet", "test"], env=env, cwd=our_repo / "src")


def _run_check(our_repo: pathlib.Path) -> None:
    """Run all the pre-commit checks."""
    subprocess.check_call(["powershell", "./Check.ps1"], cwd=our_repo / "src")


def _create_branch_commit_and_push(
    our_repo: pathlib.Path,
    aas_core_meta_revision: str,
    aas_core_codegen_revision: str,
    aas_core_testgen_revision: str,
) -> None:
    """Create a feature branch, commit the changes and push it."""
    branch = (
        f"Update-to-aas-core-meta-codegen-testgen-{aas_core_meta_revision}-"
        f"{aas_core_codegen_revision}-{aas_core_testgen_revision}"
    )
    print(f"Creating the branch {branch!r}...")
    subprocess.check_call(["git", "checkout", "-b", branch], cwd=our_repo)

    print("Adding files...")
    subprocess.check_call(["git", "add", "."], cwd=our_repo)

    # pylint: disable=line-too-long
    message = f"""\
Update to aas-core-meta, codegen, testgen {aas_core_meta_revision}, {aas_core_codegen_revision}, {aas_core_testgen_revision}

We update the development requirements to and re-generate everything
with:
* [aas-core-meta {aas_core_meta_revision}],
* [aas-core-codegen {aas_core_codegen_revision}] and
* [aas-core3.0-testgen {aas_core_testgen_revision}].

[aas-core-meta {aas_core_meta_revision}]: https://github.com/aas-core-works/aas-core-meta/commit/{aas_core_meta_revision}
[aas-core-codegen {aas_core_codegen_revision}]: https://github.com/aas-core-works/aas-core-codegen/commit/{aas_core_codegen_revision}
[aas-core3.0-testgen {aas_core_testgen_revision}]: https://github.com/aas-core-works/aas-core3.0-testgen/commit/{aas_core_testgen_revision}
"""

    # pylint: enable=line-too-long

    print("Committing...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = pathlib.Path(tmp_dir) / "commit-message.txt"
        tmp_file.write_text(message, encoding="utf-8")

        subprocess.check_call(["git", "commit", "--file", str(tmp_file)], cwd=our_repo)

    print(f"Pushing to remote {branch}...")
    subprocess.check_call(["git", "push", "-u"], cwd=our_repo)


_AAS_CORE_CODEGEN_SHA_RE = re.compile(
    r"aas-core-codegen@git\+https://github.com/aas-core-works/aas-core-codegen@([a-zA-Z0-9]+)"
)


def _get_codegen_revision(our_repo: pathlib.Path) -> str | None:
    pyproject_toml_path = our_repo / "dev_scripts/pyproject.toml"

    codegen_sha: str | None = None

    sha_re = re.compile(_AAS_CORE_CODEGEN_SHA_RE)

    try:
        with pyproject_toml_path.open("r") as pyproject_toml_file:
            for line in pyproject_toml_file:
                matches = sha_re.search(line)

                if matches is None:
                    continue

                codegen_sha = matches.group(1)
                break

    except OSError as os_error:
        print(f"Cannot read codegen revision: {os_error}.")

    if codegen_sha is None:
        print(f"Cannot read codegen revision.")

    return codegen_sha


_AAS_CORE_META_SHA_RE = re.compile(
    r"https://raw.githubusercontent.com/aas-core-works/aas-core-meta/([a-zA-Z0-9]+)/aas_core_meta/v.*.py"
)


def _get_meta_model_revision(our_repo: pathlib.Path) -> str | None:
    meta_model_path = our_repo / "dev_scripts/codegen/meta_model.py"

    meta_model_sha: str | None = None

    sha_re = re.compile(_AAS_CORE_META_SHA_RE)

    try:
        with meta_model_path.open("r") as meta_model_file:
            for line in meta_model_file:
                matches = sha_re.search(line)

                if matches is None:
                    continue

                meta_model_sha = matches.group(1)[:8]
                break

    except OSError as os_error:
        print(f"Cannot read meta model revision: {os_error}.")

    if meta_model_sha is None:
        print(f"Cannot read meta model revision.")

    return meta_model_sha


def _get_testgen_revision(our_repo: pathlib.Path) -> str | None:
    testgen_rev_path = our_repo / "src/AasCore.Aas3_0.Tests/testgen_rev.txt"

    testgen_rev: str | None = None

    try:
        with testgen_rev_path.open("r") as testgen_rev_file:
            testgen_rev = testgen_rev_file.read().strip()
    except OSError as os_error:
        print(f"Cannot read testgen revision: {os_error}.")

    if testgen_rev is None:
        print(f"Cannot read testgen revision.")

    return testgen_rev


def main() -> int:
    """Execute the main routine."""
    this_path = pathlib.Path(os.path.realpath(__file__))
    our_repo = this_path.parent.parent

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--expected_our_branch",
        help="Git branch expected in this repository",
        default="main",
    )

    args = parser.parse_args()

    expected_our_branch = str(args.expected_our_branch)

    # region Our repo

    our_branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(our_repo),
        encoding="utf-8",
    ).strip()
    if our_branch != expected_our_branch:
        print(
            f"--expected_our_branch is {expected_our_branch}, "
            f"but got {our_branch} in: {our_repo}",
            file=sys.stderr,
        )
        return 1

    # endregion

    exit_code = _make_sure_no_changed_files(
        repo_dir=our_repo, expected_branch=expected_our_branch
    )
    if exit_code is not None:
        return exit_code

    exit_code = _regenerate_code(our_repo=our_repo)
    if exit_code is not None:
        return exit_code

    aas_core_codegen_revision = _get_codegen_revision(our_repo=our_repo)
    if aas_core_codegen_revision is None:
        return 1

    aas_core_meta_revision = _get_meta_model_revision(our_repo=our_repo)
    if aas_core_meta_revision is None:
        return 1

    aas_core_testgen_revision = _get_testgen_revision(our_repo=our_repo)
    if aas_core_testgen_revision is None:
        return 1

    _reformat_code(our_repo=our_repo)

    _run_tests_and_rerecord(our_repo=our_repo)

    _run_check(our_repo=our_repo)

    _create_branch_commit_and_push(
        our_repo=our_repo,
        aas_core_meta_revision=aas_core_meta_revision,
        aas_core_codegen_revision=aas_core_codegen_revision,
        aas_core_testgen_revision=aas_core_testgen_revision,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
