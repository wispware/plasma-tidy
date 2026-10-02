# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for Tidy. Run them from the project folder with: python3 -m unittest"""

import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.dont_write_bytecode = True
# The tests need Qt's classes, not a screen.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
