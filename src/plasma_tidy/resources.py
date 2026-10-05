# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The files that ship inside Tidy: its Plasma widgets and its KWin script."""

import os


def text(name):
    """The contents of a file that ships inside Tidy. Asked of whatever loaded this module,
    so it works from the source tree and from the single file alike. (importlib.resources
    does the same, but brings some fifty modules and 3 MB along.)"""
    path = os.path.join(os.path.dirname(__file__), "data", *name.split("/"))
    return __spec__.loader.get_data(path).decode("utf-8")


KWIN_JS = text("kwin/helper.js")
KWIN_INFO_JS = text("kwin/info.js")
KWIN_RULES_JS = text("kwin/rules.js")
KWIN_POINTER_JS = text("kwin/pointer.js")
KWIN_EDGE_JS = text("kwin/edge.js")
KWIN_AFTER_JS = text("kwin/after.js")
DRAWER_CONFIG_XML = text("drawer/main.xml")
DRAWER_QML = text("drawer/main.qml")
DRAWER_CONFIG_MODEL = text("drawer/config.qml")
DRAWER_CONFIG_QML = text("drawer/ConfigGeneral.qml")
FADE_CONFIG_XML = text("helper/main.xml")
FADE_QML = text("helper/main.qml")
WISPWARE_LOGO = text("wispware.svg")
