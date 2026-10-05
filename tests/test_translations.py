# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Every text the program shows has a translation in every language Tidy offers."""

import ast
import unittest

from tests import SRC

from plasma_tidy import consts
from plasma_tidy.i18n import TRANSLATIONS

# Lists of texts that are translated where they are used, not where they are written.
LISTS = ["RULE_WHEN", "ANIMATIONS", "ACTIVE_PLACES", "ICON_STYLES", "TRAY_MODES", "CORNERS",
         "DRAWER_PAGE_TEXTS", "DISPLAYS", "POPUP_STYLES", "POPUP_PLACES", "PANEL_AFTERS",
         "TRAY_ARROWS", "TASK_POPUPS"]
# Texts that are the same in a language, and so need no entry in its table.
UNCHANGED = {"nl": {"Bluetooth", "Discover (updates)", "KDE Connect", "Printers", "Spotify",
                    "Volume"}}


def texts_in_code():
    found = set()
    for path in (SRC / "plasma_tidy").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "tr" and node.args
                    and isinstance(node.args[0], ast.Constant)):
                found.add(node.args[0].value)
    for name in LISTS:
        for entry in getattr(consts, name):
            if isinstance(entry, str):
                found.add(entry)          # just a text
            else:
                found.add(entry[1])       # (key, text, ...)
    found.update(tip for _key, _text, tip in consts.TRAY_MODES)
    for table in (consts.PANEL_NAMES, consts.PANEL_PLACES, consts.TRAY_NAMES):
        found.update(table.values())
    return found


class Translations(unittest.TestCase):
    def test_complete(self):
        wanted = texts_in_code()
        self.assertGreater(len(wanted), 250)
        for language, table in TRANSLATIONS.items():
            with self.subTest(language=language):
                self.assertEqual(sorted(wanted - set(table) - UNCHANGED.get(language, set())), [])

    def test_placeholders_survive(self):
        import re
        for language, table in TRANSLATIONS.items():
            for english, translated in table.items():
                with self.subTest(language=language, text=english[:40]):
                    self.assertEqual(sorted(re.findall(r"\{\w+\}", english)),
                                     sorted(re.findall(r"\{\w+\}", translated)))


if __name__ == "__main__":
    unittest.main()
