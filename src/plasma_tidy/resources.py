# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The files that ship inside Tidy: its Plasma widgets and its KWin script."""

from importlib.resources import files


def text(name):
    """The contents of a file that ships inside Tidy."""
    return files(__package__).joinpath("data", name).read_text(encoding="utf-8")


KWIN_JS = text("kwin/helper.js")
KWIN_INFO_JS = text("kwin/info.js")
KWIN_RULES_JS = text("kwin/rules.js")
KWIN_POINTER_JS = text("kwin/pointer.js")
KWIN_EDGE_JS = text("kwin/edge.js")
DRAWER_CONFIG_XML = text("drawer/main.xml")
DRAWER_QML = text("drawer/main.qml")
DRAWER_CONFIG_MODEL = text("drawer/config.qml")
DRAWER_CONFIG_QML = text("drawer/ConfigGeneral.qml")
FADE_CONFIG_XML = text("helper/main.xml")
FADE_QML = text("helper/main.qml")
