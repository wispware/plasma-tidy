# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Every name the code uses must exist. Python only finds a missing one when that line runs,
which for a rarely used button may be never; this looks at all of them."""

import builtins
import importlib
import pathlib
import symtable
import unittest

from tests import SRC

MODULES = sorted(p.stem for p in (SRC / "plasma_tidy").glob("*.py") if p.stem != "__main__")


def global_names(table, top=True):
    """The names a module's code looks up in the module: at the top, and in every function."""
    found = set()
    for symbol in table.get_symbols():
        if not symbol.is_referenced():
            continue
        if top or symbol.is_global():
            found.add(symbol.get_name())
    for child in table.get_children():
        found |= global_names(child, False)
    return found


class Names(unittest.TestCase):
    def test_every_name_exists(self):
        for name in MODULES:
            with self.subTest(module=name):
                module = importlib.import_module("plasma_tidy." + name)
                source = pathlib.Path(module.__file__).read_text()
                table = symtable.symtable(source, module.__file__, "exec")
                missing = sorted(n for n in global_names(table)
                                 if not hasattr(module, n) and not hasattr(builtins, n))
                self.assertEqual(missing, [])

    def test_nothing_imported_for_nothing(self):
        for name in MODULES:
            with self.subTest(module=name):
                module = importlib.import_module("plasma_tidy." + name)
                source = pathlib.Path(module.__file__).read_text()
                table = symtable.symtable(source, module.__file__, "exec")
                used = global_names(table)
                unused = sorted(s.get_name() for s in table.get_symbols()
                                if s.is_imported() and s.get_name() not in used)
                self.assertEqual(unused, [])


if __name__ == "__main__":
    unittest.main()
