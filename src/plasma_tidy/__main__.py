# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Run Tidy: python3 -m plasma_tidy, or the single file made by build.py."""

import sys

from .main import main

sys.exit(main())
