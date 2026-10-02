# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tidy's own Plasma widgets: writing them where Plasma finds them, and their settings."""

import json
import os
import sys

from .consts import (APP_NAME, DRAWER_DEFAULTS, DRAWER_DIR, DRAWER_ID, DRAWER_PAGE_TEXTS,
                     FADE_DIR, FADE_ID, LICENSE, VERSION)
from .i18n import tr
from .resources import (DRAWER_CONFIG_MODEL, DRAWER_CONFIG_QML, DRAWER_CONFIG_XML, DRAWER_QML,
                        FADE_CONFIG_XML, FADE_QML)


def drawer_files():
    """The drawer widget as Plasma wants it on disk: {relative path: contents}."""
    metadata = {"KPlugin": {"Id": DRAWER_ID, "Name": f"{APP_NAME} Drawer",
                            "Name[nl]": f"{APP_NAME}-la",
                            "Description": "Tucks panel widgets away behind an arrow",
                            "Description[nl]": "Bergt paneelonderdelen op achter een pijltje",
                            "Icon": "arrow-right", "Category": "Utilities",
                            "Version": VERSION, "License": LICENSE},
                "KPackageStructure": "Plasma/Applet",
                "X-Plasma-API-Minimum-Version": "6.0"}
    return {"metadata.json": json.dumps(metadata, indent=4) + "\n",
            "contents/config/main.xml": DRAWER_CONFIG_XML.lstrip("\n"),
            "contents/config/config.qml": DRAWER_CONFIG_MODEL,
            "contents/ui/ConfigGeneral.qml": DRAWER_CONFIG_QML.lstrip("\n"),
            "contents/ui/main.qml": DRAWER_QML.lstrip("\n")}


def fade_files():
    """The fade helper as Plasma wants it on disk: {relative path: contents}."""
    metadata = {"KPlugin": {"Id": FADE_ID, "Name": f"{APP_NAME} desktop helper",
                            "Description": "Fades the desktop icons for Tidy; invisible",
                            "Icon": "view-visible", "Category": "Utilities",
                            "Version": VERSION, "License": LICENSE},
                "KPackageStructure": "Plasma/Applet",
                "X-Plasma-API-Minimum-Version": "6.0",
                "NoDisplay": True}
    return {"metadata.json": json.dumps(metadata, indent=4) + "\n",
            "contents/config/main.xml": FADE_CONFIG_XML,
            "contents/ui/main.qml": FADE_QML.lstrip("\n")}


def install_drawer():
    """Write Tidy's widgets (the drawer and the fade helper) where Plasma finds them. They
    ship inside this file, so that installing Tidy stays a matter of copying one file. A
    changed widget is picked up by Plasma at its next start."""
    for folder, files in ((DRAWER_DIR, drawer_files()), (FADE_DIR, fade_files())):
        for name, text in files.items():
            path = os.path.join(folder, name)
            try:
                with open(path) as f:
                    if f.read() == text:
                        continue
            except OSError:
                pass
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(text)


def drawer_texts():
    """What a drawer needs to know from Tidy: how to open the settings, and its texts."""
    return {"tidyCommand": os.path.abspath(sys.argv[0]),
            "textOpen": tr("Show the hidden items"),
            "textClose": tr("Hide the items"),
            "textSettings": tr("{app} settings…").format(app=APP_NAME),
            "textPaused": tr("Paused. Click to resume"),
            "uiTexts": json.dumps({text: tr(text) for text in DRAWER_PAGE_TEXTS})}


def stored(settings, key, kind=dict):
    """A setting that holds a table or a list, as that. Empty when it is not there or cannot
    be read: a broken note must never stop Tidy."""
    try:
        found = json.loads(settings.value(key, "") or "null")
    except (ValueError, TypeError):
        return kind()
    return found if isinstance(found, kind) else kind()


def drawer_value(key, raw):
    """A drawer setting as read from Plasma (always text) in the type of its default."""
    default = DRAWER_DEFAULTS[key]
    if raw is None or raw == "":
        return list(default) if isinstance(default, list) else default
    if isinstance(default, bool):
        return raw if isinstance(raw, bool) else str(raw).lower() == "true"
    if isinstance(default, int):
        try:
            return int(float(raw))
        except ValueError:
            return default
    if isinstance(default, list):
        return [str(i) for i in raw] if isinstance(raw, list) else [
            i for i in str(raw).split(",") if i]
    return str(raw)
