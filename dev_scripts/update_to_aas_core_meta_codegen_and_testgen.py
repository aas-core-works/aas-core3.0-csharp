"""
Update everything in this project to the latest aas-core-meta, -codegen and -testgen.

Git is expected to be installed.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Optional, List, Callable, AnyStr, Sequence

# noinspection RegExpSimplifiable
AAS_CORE_META_DEPENDENCY_RE = re.compile(
    r"aas-core-meta@git\+https://github.com/aas-core-works/aas-core-meta@([a-fA-F0-9]+)"
)

# noinspection RegExpSimplifiable
AAS_CORE_CODEGEN_DEPENDENCY_RE = re.compile(
    r"aas-core-codegen@git\+https://github.com/aas-core-works/aas-core-codegen@([a-fA-F0-9]+)"
)


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


def _update_pyproject_toml(
    our_repo: pathlib.Path, aas_core_meta_revision: str, aas_core_codegen_revision: str
) -> None:
    """Update the aas-core-meta in pyproject.toml."""
    pyproject_toml = our_repo / "dev_scripts" / "pyproject.toml"
    text = pyproject_toml.read_text(encoding="utf-8")

    aas_core_meta_dependency = (
        f"aas-core-meta@git+https://github.com/aas-core-works/aas-core-meta"
        f"@{aas_core_meta_revision}"
    )

    text = re.sub(AAS_CORE_META_DEPENDENCY_RE, aas_core_meta_dependency, text)

    aas_core_codegen_dependency = (
        f"aas-core-codegen@git+https://github.com/aas-core-works/aas-core-codegen"
        f"@{aas_core_codegen_revision}"
    )

    text = re.sub(AAS_CORE_CODEGEN_DEPENDENCY_RE, aas_core_codegen_dependency, text)

    pyproject_toml.write_text(text, encoding="utf-8")


def _uninstall_and_install_aas_core_meta(
    our_repo: pathlib.Path, aas_core_meta_revision: str
) -> None:
    """Uninstall and install the latest aas-core-meta in the virtual environment."""
    subprocess.check_call(
        [sys.executable, "-m", "pip", "uninstall", "-y", "aas-core-meta"],
        cwd=str(our_repo),
    )

    aas_core_meta_dependency = (
        f"aas-core-meta@git+https://github.com/aas-core-works/aas-core-meta"
        f"@{aas_core_meta_revision}"
    )

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", aas_core_meta_dependency],
        cwd=str(our_repo),
    )


def _uninstall_and_install_aas_core_codegen(
    our_repo: pathlib.Path, aas_core_codegen_revision: str
) -> None:
    """Uninstall and install the latest aas-core-codegen in the virtual environment."""
    subprocess.check_call(
        [sys.executable, "-m", "pip", "uninstall", "-y", "aas-core-codegen"],
        cwd=str(our_repo),
    )

    aas_core_codegen_dependency = (
        f"aas-core-codegen@git+https://github.com/aas-core-works/aas-core-codegen"
        f"@{aas_core_codegen_revision}"
    )

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", aas_core_codegen_dependency],
        cwd=str(our_repo),
    )


def _copy_code_from_aas_core_codegen(
    aas_core_codegen_repo: pathlib.Path, our_repo: pathlib.Path
) -> None:
    """Copy the generated code from aas-core-codegen's test data."""
    source_dir = (
        aas_core_codegen_repo
        / "test_data/csharp/test_main/aas_core_meta.v3/expected_output"
    )

    target_dir = our_repo / "src/AasCore.Aas3_0"

    print(
        f"Copying the code: "
        f"from {source_dir} "
        f"to {target_dir.relative_to(our_repo)} ..."
    )

    for pth in source_dir.glob("*.cs"):
        tgt_pth = target_dir / pth.name
        shutil.copy(pth, tgt_pth)


def _copy_python_sdk_from_aas_core_codegen(
    aas_core_codegen_repo: pathlib.Path,
    our_repo: pathlib.Path,
    aas_core_codegen_revision: str,
) -> None:
    """Copy the generated Python SDK from aas-core-codegen's test data."""
    source_dir = (
        aas_core_codegen_repo
        / "test_data/python/test_main/aas_core_meta.v3/expected_output"
    )

    target_dir = our_repo / "dev_scripts/aas_core3"

    for pth in source_dir.glob("*.py"):
        tgt_pth = target_dir / pth.name
        shutil.copy(pth, tgt_pth)

    init_py = target_dir / "__init__.py"

    text = f'''\
"""
Provide Python SDK as copied from aas-core-codegen test data.

This copy is necessary so that we can decouple from ``aas-core*-python`` repository.

The revision of aas-core-codegen was: {aas_core_codegen_revision}
"""
'''
    init_py.write_text(text, encoding="utf-8")


def _run_in_parallel(
    calls: Sequence[Callable[[], subprocess.Popen[AnyStr]]],
    on_status_update: Callable[[int], None],
) -> Optional[int]:
    """
    Run the given scripts in parallel.

    Return an error code, if any.
    """
    procs = []  # type: List[subprocess.Popen[AnyStr]]

    try:
        for call in calls:
            proc = call()
            procs.append(proc)

        failure = False
        remaining_procs = sum(1 for proc in procs if proc.returncode is None)

        next_print = time.time() + 15
        while remaining_procs > 0:
            if time.time() > next_print:
                on_status_update(remaining_procs)
                next_print = time.time() + 15

            time.sleep(1)

            for proc in procs:
                proc.poll()

                if proc.returncode is not None:
                    if proc.returncode != 0:
                        failure = True

            if failure:
                print(
                    "One or more processes failed. Terminating all the processes...",
                    file=sys.stderr,
                )
                for proc in procs:
                    proc.terminate()

                print("Terminated all the processes.", file=sys.stderr)
                return 1

            for proc in procs:
                proc.poll()

            remaining_procs = sum(1 for proc in procs if proc.returncode is None)

        return None
    finally:
        for proc in procs:
            if proc.returncode is None:
                proc.terminate()


def _generate_test_code(our_repo: pathlib.Path) -> Optional[int]:
    """Run the internal code generation."""
    test_codegen_dir = our_repo / "dev_scripts/test_codegen"
    scripts = sorted(
        pth
        for pth in test_codegen_dir.glob("generate_*.py")
        if pth.name != "generate_all.py"
    )

    # pylint: disable=consider-using-with
    calls = [
        lambda a_pth=pth, cwd=our_repo: subprocess.Popen(  # type: ignore
            [sys.executable, str(a_pth)],
            cwd=str(cwd),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            encoding="utf-8",
        )
        for pth in scripts
    ]  # type: Sequence[Callable[[], subprocess.Popen[str]]]
    # pylint: enable=consider-using-with

    scripts_joined = ",\n".join(str(script) for script in scripts)
    print(f"Starting to run test codegen scripts:\n{scripts_joined}")
    start = time.perf_counter()

    exit_code = _run_in_parallel(
        calls=calls,
        on_status_update=(
            lambda remaining: print(
                f"There are {remaining} codegen script(s) still running..."
            )
        ),
    )
    if exit_code is not None:
        return exit_code

    duration = time.perf_counter() - start
    print(f"Generating the code took: {duration:.2f} seconds.")

    return None


def _replace_test_data(
    our_repo: pathlib.Path, aas_core_testgen_repo: pathlib.Path
) -> None:
    """
    Remove the test data and copy it from the testgen repository.

    Return an error code, if any.
    """
    test_data_dir = our_repo / "test_data"

    print(f"Removing the test data from: {test_data_dir}")

    for pth in sorted(
            sub_pth
            for sub_pth in test_data_dir.iterdir()
            if sub_pth.is_dir()
    ):
        print(f"Removing {pth} ...")
        shutil.rmtree(pth)

    print(f"Copying the test data from: {aas_core_testgen_repo} ...")
    for pth in [aas_core_testgen_repo / "test_data" / name for name in ("Json", "Xml")]:
        target_pth = test_data_dir / pth.name
        assert not target_pth.exists()
        assert pth.exists(), f"Expected the test data directory to exist: {pth=}"
        shutil.copytree(pth, target_pth)


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


def main() -> int:
    """Execute the main routine."""
    this_path = pathlib.Path(os.path.realpath(__file__))
    our_repo = this_path.parent.parent

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--aas_core_meta_repo",
        help="path to the aas-core-meta repository",
        default=str(our_repo.parent / "aas-core-meta"),
    )
    parser.add_argument(
        "--expected_aas_core_meta_branch",
        help="Git branch expected in the aas-core-meta repository",
        default="main",
    )
    parser.add_argument(
        "--aas_core_codegen_repo",
        help="path to the aas-core-codegen repository",
        default=str(our_repo.parent / "aas-core-codegen"),
    )
    parser.add_argument(
        "--expected_aas_core_codegen_branch",
        help="Git branch expected in the aas-core-meta repository",
        default="main",
    )
    parser.add_argument(
        "--aas_core_testgen_repo",
        help="path to the aas-core-codegen repository",
        default=str(our_repo.parent / "aas-core3.0-testgen"),
    )
    parser.add_argument(
        "--expected_aas_core_testgen_branch",
        help="Git branch expected in the aas-core-meta repository",
        default="main",
    )
    parser.add_argument(
        "--expected_our_branch",
        help="Git branch expected in this repository",
        default="main",
    )

    args = parser.parse_args()

    aas_core_meta_repo = pathlib.Path(args.aas_core_meta_repo)
    expected_aas_core_meta_branch = str(args.expected_aas_core_meta_branch)

    aas_core_codegen_repo = pathlib.Path(args.aas_core_codegen_repo)
    expected_aas_core_codegen_branch = str(args.expected_aas_core_codegen_branch)

    aas_core_testgen_repo = pathlib.Path(args.aas_core_testgen_repo)
    expected_aas_core_testgen_branch = str(args.expected_aas_core_testgen_branch)

    expected_our_branch = str(args.expected_our_branch)

    # region aas-core-meta repo

    if not aas_core_meta_repo.exists():
        print(
            f"--aas_core_meta_repo does not exist: {aas_core_meta_repo}",
            file=sys.stderr,
        )
        return 1

    if not aas_core_meta_repo.is_dir():
        print(
            f"--aas_core_meta_repo is not a directory: {aas_core_meta_repo}",
            file=sys.stderr,
        )
        return 1

    aas_core_meta_branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(aas_core_meta_repo),
        encoding="utf-8",
    ).strip()
    if aas_core_meta_branch != expected_aas_core_meta_branch:
        print(
            f"--expected_aas_core_meta_branch is {expected_aas_core_meta_branch}, "
            f"but got {aas_core_meta_branch} "
            f"in --aas_core_meta_repo: {aas_core_meta_repo}",
            file=sys.stderr,
        )
        return 1

    aas_core_meta_revision = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(aas_core_meta_repo),
        encoding="utf-8",
    ).strip()

    # endregion

    # region aas-core-codegen repo

    if not aas_core_codegen_repo.exists():
        print(
            f"--aas_core_codegen_repo does not exist: {aas_core_codegen_repo}",
            file=sys.stderr,
        )
        return 1

    if not aas_core_codegen_repo.is_dir():
        print(
            f"--aas_core_codegen_repo is not a directory: {aas_core_codegen_repo}",
            file=sys.stderr,
        )
        return 1

    aas_core_codegen_branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(aas_core_codegen_repo),
        encoding="utf-8",
    ).strip()
    if aas_core_codegen_branch != expected_aas_core_codegen_branch:
        print(
            f"--expected_aas_core_codegen_branch is {expected_aas_core_codegen_branch}, "
            f"but got {aas_core_codegen_branch} "
            f"in --aas_core_codegen_repo: {aas_core_codegen_repo}",
            file=sys.stderr,
        )
        return 1

    aas_core_codegen_revision = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(aas_core_codegen_repo),
        encoding="utf-8",
    ).strip()

    # endregion

    # region aas-core3.0-testgen repo

    if not aas_core_testgen_repo.exists():
        print(
            f"--aas_core_testgen_repo does not exist: {aas_core_testgen_repo}",
            file=sys.stderr,
        )
        return 1

    if not aas_core_testgen_repo.is_dir():
        print(
            f"--aas_core_testgen_repo is not a directory: {aas_core_testgen_repo}",
            file=sys.stderr,
        )
        return 1

    aas_core_testgen_branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(aas_core_testgen_repo),
        encoding="utf-8",
    ).strip()
    if aas_core_testgen_branch != expected_aas_core_testgen_branch:
        print(
            f"--expected_aas_core_testgen_branch is {expected_aas_core_testgen_branch}, "
            f"but got {aas_core_testgen_branch} "
            f"in --aas_core_testgen_repo: {aas_core_testgen_repo}",
            file=sys.stderr,
        )
        return 1

    aas_core_testgen_revision = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(aas_core_testgen_repo),
        encoding="utf-8",
    ).strip()

    # endregion

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

    for repo_dir, expected_branch in [
        (our_repo, expected_our_branch),
        (aas_core_meta_repo, expected_aas_core_meta_branch),
        (aas_core_codegen_repo, expected_aas_core_codegen_branch),
        (aas_core_testgen_repo, expected_aas_core_testgen_branch),
    ]:
        exit_code = _make_sure_no_changed_files(
            repo_dir=repo_dir, expected_branch=expected_branch
        )
        if exit_code is not None:
            return exit_code

    _update_pyproject_toml(
        our_repo=our_repo,
        aas_core_meta_revision=aas_core_meta_revision,
        aas_core_codegen_revision=aas_core_codegen_revision,
    )

    _uninstall_and_install_aas_core_meta(
        our_repo=our_repo, aas_core_meta_revision=aas_core_meta_revision
    )

    _uninstall_and_install_aas_core_codegen(
        our_repo=our_repo, aas_core_codegen_revision=aas_core_codegen_revision
    )

    _copy_code_from_aas_core_codegen(
        aas_core_codegen_repo=aas_core_codegen_repo, our_repo=our_repo
    )

    _copy_python_sdk_from_aas_core_codegen(
        aas_core_codegen_repo=aas_core_codegen_repo,
        our_repo=our_repo,
        aas_core_codegen_revision=aas_core_codegen_revision,
    )

    _replace_test_data(our_repo=our_repo, aas_core_testgen_repo=aas_core_testgen_repo)

    exit_code = _generate_test_code(our_repo=our_repo)
    if exit_code is not None:
        return exit_code

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
