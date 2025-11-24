#!/usr/bin/env python3

"""Run pre-commit checks on the repository."""

import argparse
import enum
import os
import pathlib
import shlex
import subprocess
import sys
from typing import Optional, Mapping, Sequence


# pylint: disable=unnecessary-comprehension


class Step(enum.Enum):
    """Enumerate different pre-commit steps."""

    REFORMAT = "reformat"
    MYPY = "mypy"
    PYLINT = "pylint"
    TEST = "test"
    DOCTEST = "doctest"


def call_and_report(
    verb: str,
    cmd: Sequence[str],
    cwd: Optional[pathlib.Path] = None,
    env: Optional[Mapping[str, str]] = None,
) -> int:
    """
    Wrap a subprocess call with the reporting to STDERR if it failed.

    Return 1 if there is an error and 0 otherwise.
    """
    cmd_str = " ".join(shlex.quote(part) for part in cmd)

    if cwd is not None:
        print(f"Executing from {cwd}: {cmd_str}")
    else:
        print(f"Executing: {cmd_str}")

    exit_code = subprocess.call(cmd, cwd=str(cwd) if cwd is not None else None, env=env)

    if exit_code != 0:
        print(
            f"Failed to {verb} with exit code {exit_code}: {cmd_str}", file=sys.stderr
        )

    return exit_code


def main() -> int:
    """Execute entry_point routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--overwrite",
        help="Try to automatically fix the offending files (e.g., by re-formatting).",
        action="store_true",
    )
    parser.add_argument(
        "--select",
        help=(
            "If set, only the selected steps are executed. "
            "This is practical if some of the steps failed and you want to "
            "fix them in isolation. "
            "The steps are given as a space-separated list of: "
            + " ".join(value.value for value in Step)
        ),
        metavar="",
        nargs="+",
        choices=[value.value for value in Step],
    )
    parser.add_argument(
        "--skip",
        help=(
            "If set, skips the specified steps. "
            "This is practical if some of the steps passed and "
            "you want to fix the remainder in isolation. "
            "The steps are given as a space-separated list of: "
            + " ".join(value.value for value in Step)
        ),
        metavar="",
        nargs="+",
        choices=[value.value for value in Step],
    )

    args = parser.parse_args()

    overwrite = bool(args.overwrite)

    selects = (
        [Step(value) for value in args.select]
        if args.select is not None
        else [value for value in Step]
    )
    skips = [Step(value) for value in args.skip] if args.skip is not None else []

    src_root = pathlib.Path(os.path.realpath(__file__)).parent.parent

    if Step.REFORMAT in selects and Step.REFORMAT not in skips:
        print("Re-formatting...")
        reformat_targets = [
            "codegen/codegen.py",
            "codegen/download_aas_core_meta_model.py",
            "continuous_integration_of_dev_scripts",
            "update_to_aas_core_meta_codegen.py",
        ]
        if overwrite:
            exit_code = call_and_report(
                verb="black",
                cmd=["black"] + reformat_targets,
                cwd=src_root,
            )
            if exit_code != 0:
                return 1
        else:
            exit_code = call_and_report(
                verb="check with black",
                cmd=["black", "--check"] + reformat_targets,
                cwd=src_root,
            )
            if exit_code != 0:
                return 1
    else:
        print("Skipped re-formatting.")

    if Step.MYPY in selects and Step.MYPY not in skips:
        print("Mypy'ing...")
        mypy_targets = [
            "codegen/codegen.py",
            "codegen/download_aas_core_meta_model.py",
            "continuous_integration_of_dev_scripts",
            "update_to_aas_core_meta_codegen.py",
        ]
        config_file = pathlib.Path("continuous_integration_of_dev_scripts") / "mypy.ini"

        exit_code = call_and_report(
            verb="mypy",
            cmd=["mypy", "--strict", "--config-file", str(config_file)] + mypy_targets,
            cwd=src_root,
        )
        if exit_code != 0:
            return 1
    else:
        print("Skipped mypy'ing.")

    if Step.PYLINT in selects and Step.PYLINT not in skips:
        print("Pylint'ing...")
        pylint_targets = [
            "codegen/codegen.py",
            "codegen/download_aas_core_meta_model.py",
            "continuous_integration_of_dev_scripts",
            "update_to_aas_core_meta_codegen.py",
        ]
        rcfile = pathlib.Path("continuous_integration_of_dev_scripts") / "pylint.rc"

        exit_code = call_and_report(
            verb="pylint",
            cmd=["pylint", f"--rcfile={rcfile}"] + pylint_targets,
            cwd=src_root,
        )
        if exit_code != 0:
            return 1
    else:
        print("Skipped pylint'ing.")

    if Step.DOCTEST in selects and Step.DOCTEST not in skips:
        print("Doctest'ing...")

        for module_name in [
            "continuous_integration_of_dev_scripts",
        ]:
            for pth in (src_root / module_name).glob("**/*.py"):
                if pth.name == "__main__.py":
                    continue

                # NOTE (mristin, 2022-12-08):
                # The subprocess calls are expensive, call only if there is an actual
                # doctest
                text = pth.read_text(encoding="utf-8")
                if ">>>" in text:
                    exit_code = call_and_report(
                        verb="doctest",
                        cmd=[sys.executable, "-m", "doctest", str(pth)],
                        cwd=src_root,
                    )
                    if exit_code != 0:
                        return 1
    else:
        print("Skipped doctest'ing.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
