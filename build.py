#!/usr/bin/python3
# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Make the single file `plasma-tidy` out of src/.

    ./build.py            writes ./plasma-tidy
    ./build.py <file>     writes it somewhere else
    ./build.py --install  puts it in ~/.local/bin, with its entry in the application menu

The result is everything in src/plasma_tidy packed together (a Python "zipapp"): one file to
copy to ~/.local/bin, which Python runs as it is.
"""

import compileall
import os
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


def install():
    """For yourself, without a package. The menu entry names the program by its full path:
    not every distribution has ~/.local/bin on the PATH of the desktop session, and then
    the menu, the shortcuts and the entry itself would not find a bare "plasma-tidy"."""
    home = pathlib.Path.home()
    target = home / ".local" / "bin" / "plasma-tidy"
    target.parent.mkdir(parents=True, exist_ok=True)
    build(target)
    target.chmod(0o755)
    entry = (ROOT / "data" / "plasma-tidy.desktop").read_text()
    menu = home / ".local" / "share" / "applications" / "plasma-tidy.desktop"
    menu.parent.mkdir(parents=True, exist_ok=True)
    menu.write_text(entry.replace("Exec=plasma-tidy", f"Exec={target}"))
    print(f"Installed {target}\nand {menu}")
    if str(target.parent) not in os.environ.get("PATH", "").split(":"):
        print(f"{target.parent} is not on your PATH: start Tidy from the application menu, or "
              f"with {target}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--install"]:
        install()
        sys.exit(0)
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "plasma-tidy"
    build(target)
    print(f"Wrote {target} ({target.stat().st_size // 1024} kB)")
