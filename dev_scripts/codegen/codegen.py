"""Generate the SDK based on the aas-core-meta model and the snippets."""

import argparse
import os
import pathlib
import subprocess
import sys


def _generate_sdk(
    meta_model_path: pathlib.Path,
    snippet_path: pathlib.Path,
    sdk_path: pathlib.Path,
) -> None:
    subprocess.run(
        [
            "aas-core-codegen",
            "--model_path",
            str(meta_model_path),
            "--snippets_dir",
            str(snippet_path),
            "--output_dir",
            str(sdk_path / "src/AasCore.Aas3_0"),
            "--target",
            "csharp",
        ],
        check=True,
    )


def main() -> int:
    """Execute the main routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meta_model", type=pathlib.Path, required=True)
    parser.add_argument("--target", type=pathlib.Path, required=True)
    args = parser.parse_args()

    this_dir = pathlib.Path(os.path.realpath(__file__)).parent

    snippet_dir = this_dir / "snippets"

    _generate_sdk(args.meta_model, snippet_dir, this_dir.parent.parent)

    return 0


if __name__ == "__main__":
    sys.exit(main())
