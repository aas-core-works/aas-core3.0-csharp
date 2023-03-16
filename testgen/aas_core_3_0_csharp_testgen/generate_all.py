"""Generate all the code using testgen."""

import os
import pathlib
import shlex
import subprocess
import sys


def main() -> int:
    """Execute the main routine."""
    this_path = pathlib.Path(os.path.realpath(__file__))
    testgen_dir = this_path.parent

    for script_pth in sorted(testgen_dir.glob("generate_*.py")):
        if script_pth == this_path:
            continue

        cmd = [sys.executable, str(script_pth)]

        cmd_str = " ".join(shlex.quote(part) for part in cmd)

        print(f"Executing: {script_pth.relative_to(testgen_dir)}")
        return_code = subprocess.call(cmd, cwd=str(script_pth.parent))
        if return_code != 0:
            print(f"Failed with return code {return_code}: {cmd_str}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
