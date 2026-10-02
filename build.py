#!/usr/bin/python3
# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Make the single file `plasma-tidy` out of src/.

    ./build.py            writes ./plasma-tidy
    ./build.py <file>     writes it somewhere else

The result is everything in src/plasma_tidy packed together (a Python "zipapp"): one file to
copy to ~/.local/bin, which Python runs as it is.
"""

import compileall
import pathlib
import py_compile
import shutil
import sys
import tempfile
import zipapp

ROOT = pathlib.Path(__file__).resolve().parent
START = "import sys\n\nfrom plasma_tidy.main import main\n\nsys.exit(main())\n"


def build(target):
    with tempfile.TemporaryDirectory() as folder:
        folder = pathlib.Path(folder)
        shutil.copytree(ROOT / "src" / "plasma_tidy", folder / "plasma_tidy",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (folder / "__main__.py").write_text(START)
        # Compiled copies go along, so that starting does not begin with compiling. They are
        # for the Python that builds; another Python simply uses the source next to them.
        compileall.compile_dir(folder, quiet=1, legacy=True,
                               invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
        zipapp.create_archive(folder, target, interpreter="/usr/bin/python3")


if __name__ == "__main__":
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "plasma-tidy"
    build(target)
    print(f"Wrote {target} ({target.stat().st_size // 1024} kB)")
