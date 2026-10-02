# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The system tray: reading its icons, and the tab to arrange them."""

import json
import re

from PyQt6.QtCore import Qt
from PyQt6.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

from .consts import (TRAY_AUTO, TRAY_DISABLED, TRAY_HIDDEN, TRAY_MINIMAL_AUTO, TRAY_MINIMAL_SHOWN,
                     TRAY_MODES, TRAY_NAMES, TRAY_SHOWN)
from .i18n import tr


def tray_app_items():
    """Application icons (StatusNotifierItems) currently in the system tray."""
    bus = QDBusConnection.sessionBus()
    def get(service, path, interface, name):
        props = QDBusInterface(service, path, "org.freedesktop.DBus.Properties", bus)
        props.setTimeout(500)  # a hung application must not hold up the window
        reply = props.call("Get", interface, name)
        if reply.type() != QDBusMessage.MessageType.ReplyMessage:
            return None  # error reply: don't use it as a name
        args = reply.arguments()
        return args[0] if args else None

    items = {}
    entries = get("org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher",
                  "org.kde.StatusNotifierWatcher", "RegisteredStatusNotifierItems") or []
    for entry in entries:
        service, _, path = entry.partition("/")
        path = "/" + (path or "StatusNotifierItem")
        item_id = get(service, path, "org.kde.StatusNotifierItem", "Id")
        if item_id:
            items[item_id] = get(service, path, "org.kde.StatusNotifierItem", "Title") or item_id
    return items


def tray_minimal(config, apps):
    """The "Minimal" choice for the system tray, as (extra, shown, hidden): only network,
    volume and battery visible, a few indicators automatic, the rest under ^."""
    plasmoids = list(dict.fromkeys(config["known"] + [
        i for i in config["extra"] if i.startswith("org.kde.")]))
    others = list(dict.fromkeys(list(apps) + [
        i for i in config["shown"] + config["hidden"] + config["extra"] if i not in plasmoids]))
    extra, shown, hidden = list(config["extra"]), [], []
    for item in plasmoids + others:
        if item in TRAY_MINIMAL_SHOWN or item in TRAY_MINIMAL_AUTO:
            if item in TRAY_MINIMAL_SHOWN:
                shown.append(item)
            if item in plasmoids and item not in extra:
                extra.append(item)
        elif item in plasmoids and item not in config["extra"]:
            continue  # what was already off stays off
        else:
            hidden.append(item)
    return extra, shown, hidden


def tray_rules(settings):
    """Rules for application icons by name: [{"match": text, "mode": shown/hidden/auto}]."""
    try:
        found = json.loads(settings.value("tray_rules", "") or "[]")
    except ValueError:
        return []
    if not isinstance(found, list):
        return []
    return [r for r in found if isinstance(r, dict) and r.get("match")
            and r.get("mode") in (TRAY_AUTO, TRAY_SHOWN, TRAY_HIDDEN)]


def tray_rule_mode(rules, item_id, title):
    """What the first rule that fits this icon says, or None."""
    names = f"{item_id} {title or ''}".lower()
    for rule in rules:
        if rule["match"].lower() in names:
            return rule["mode"]
    return None


def remember_tray(settings, config):
    """Remember how the tray was before Tidy first touched it, for "Restore everything"."""
    if not settings.value("tray_original", ""):
        settings.setValue("tray_original", json.dumps(
            {k: config[k] for k in ("extra", "shown", "hidden")}))


class TrayTab(QWidget):
    """Tab for choosing per icon how it appears in the system tray."""

    def __init__(self, plasma, settings):
        super().__init__()
        self.plasma = plasma
        self.settings = settings
        self.config = plasma.tray_config()
        layout = QVBoxLayout(self)
        if self.config is None:
            layout.addWidget(QLabel(tr("No system tray found in the panel.")))
            return

        intro = QLabel(tr("Choose for each icon how it appears in the system tray.\n"
                          "Automatic: only when relevant · Hide: under the ^ arrow"))
        intro.setWordWrap(True)
        layout.addWidget(intro)

        apps = tray_app_items()
        plasmoids = list(dict.fromkeys(self.config["known"] + [
            i for i in self.config["extra"] if i.startswith("org.kde.")]))
        app_ids = list(dict.fromkeys(list(apps) + [
            i for i in self.config["shown"] + self.config["hidden"] + self.config["extra"]
            if i not in plasmoids]))
        self.plasmoids = set(plasmoids)

        self.search = QLineEdit()
        self.search.setPlaceholderText(tr("Search…"))
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self.filter)
        self.search.setProperty("tidyNoSetting", True)
        layout.addWidget(self.search)

        area = QScrollArea(widgetResizable=True)
        inner = QWidget()
        form = QFormLayout(inner)
        self.form = form
        self.combos = {}
        for section, ids in ((tr("System items"), plasmoids), (tr("Applications"), app_ids)):
            header = QLabel(f"<b>{section}</b>")
            form.addRow(header)
            for item_id in sorted(ids, key=lambda i: self.label(i, apps).lower()):
                combo = QComboBox()
                for key, text, tip in TRAY_MODES:
                    if key == TRAY_DISABLED and item_id not in self.plasmoids:
                        continue  # applications can only be shown or hidden
                    combo.addItem(tr(text), key)
                    combo.setItemData(combo.count() - 1, tr(tip), Qt.ItemDataRole.ToolTipRole)
                combo.setCurrentIndex(combo.findData(self.mode_of(item_id)))
                self.combos[item_id] = combo
                form.addRow(self.label(item_id, apps) + ":", combo)
        area.setWidget(inner)
        # Wide enough for the whole list: scroll vertically only.
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        area.setMinimumWidth(inner.sizeHint().width()
                             + area.verticalScrollBar().sizeHint().width()
                             + 2 * area.frameWidth())
        layout.addWidget(area, 1)

        def button(text, tip, action, icon=None):
            widget = QPushButton(QIcon.fromTheme(icon), tr(text)) if icon else QPushButton(tr(text))
            widget.setToolTip(tr(tip))
            widget.clicked.connect(action)
            return widget

        # Every icon at once. Nothing changes in the tray until OK.
        row = QHBoxLayout()
        row.addWidget(button("Minimal", "Only network, volume and battery visible; "
                             "notifications and devices when relevant; the rest under ^.",
                             self.apply_minimal, "games-config-theme"))
        row.addWidget(button("Show all", "Every icon always visible in the panel; what is "
                             "switched off stays off.",
                             lambda: self.apply_all(TRAY_SHOWN), "view-visible"))
        row.addWidget(button("Hide all", "Every icon under the ^ arrow; what is switched off "
                             "stays off.", lambda: self.apply_all(TRAY_HIDDEN), "view-hidden"))
        row.addWidget(button("All automatic", "Plasma decides for every icon; what is switched "
                             "off stays off.", lambda: self.apply_all(TRAY_AUTO)))
        row.addStretch()
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(button("Plasma default", "Everything switched on and automatic, as a "
                             "fresh Plasma has it.", self.apply_default))
        self.preset = button("My preset", "Apply the arrangement you saved.", self.apply_preset)
        self.preset.setEnabled(bool(self.settings.value("tray_preset", "")))
        row.addWidget(self.preset)
        row.addWidget(button("Save as my preset", "Remember the choices as they are now.",
                             self.save_preset, "document-save"))
        row.addStretch()
        row.addWidget(button("Undo", "Back to how the list was when this window opened.",
                             self.undo, "edit-undo"))
        layout.addLayout(row)

        self.titles = apps
        self.hide_new = QCheckBox(tr("New icons go under the ^ arrow by themselves"))
        self.hide_new.setChecked(self.settings.value("tray_hide_new", False, bool))
        self.hide_new.setToolTip(tr("An application that shows a tray icon for the first time "
                                    "gets it hidden. Works while Tidy is running."))
        row = QHBoxLayout()
        row.addWidget(self.hide_new)
        row.addStretch()
        row.addWidget(button("Add a rule for a name",
                             "A rule decides by name how an application's icon appears: when "
                             "the rule is made, and every time such an icon shows up for the "
                             "first time. A rule goes before the choice on the left.",
                             lambda: self.add_rule("", TRAY_HIDDEN, by_hand=True), "list-add"))
        layout.addLayout(row)
        self.rule_rows = []
        self.rules_layout = QVBoxLayout()
        layout.addLayout(self.rules_layout)
        for rule in tray_rules(self.settings):
            self.add_rule(rule["match"], rule["mode"])

    def add_rule(self, match, mode, by_hand=False):
        row = QWidget()
        row.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.addWidget(QLabel(tr("Name contains:")))
        text = QLineEdit(match)
        text.setPlaceholderText(tr("for example: discord"))
        row_layout.addWidget(text, 1)
        combo = QComboBox()
        for key, label, _tip in TRAY_MODES:
            if key != TRAY_DISABLED:
                combo.addItem(tr(label), key)
        combo.setCurrentIndex(max(0, combo.findData(mode)))
        row_layout.addWidget(combo)
        remove = QPushButton(QIcon.fromTheme("list-remove"), "")
        remove.setToolTip(tr("Remove this rule"))
        row_layout.addWidget(remove)
        entry = (row, text, combo)
        remove.clicked.connect(lambda: self.remove_rule(entry))
        self.rule_rows.append(entry)
        self.rules_layout.addWidget(row)
        if by_hand:
            self.rules_edited()
            text.setFocus()

    def remove_rule(self, entry):
        self.rule_rows.remove(entry)
        entry[0].setParent(None)
        entry[0].deleteLater()
        self.rules_edited()

    def rules_edited(self):
        window = self.window()
        if hasattr(window, "watch_changes"):
            window.watch_changes(self)
            window.mark_changed()

    def rules(self):
        return [{"match": text.text().strip(), "mode": combo.currentData()}
                for _row, text, combo in self.rule_rows if text.text().strip()]

    @staticmethod
    def label(item_id, apps):
        if item_id in TRAY_NAMES:
            return tr(TRAY_NAMES[item_id])
        # Chromium/Electron apps are called "<Name>_status_icon_<n>".
        name = re.sub(r"_status_icon_\d+$", "", item_id)
        return name if name != item_id else apps.get(item_id) or item_id

    def mode_of(self, item_id):
        if item_id in self.config["shown"]:
            return TRAY_SHOWN
        if item_id in self.config["hidden"]:
            return TRAY_HIDDEN
        if item_id in self.plasmoids and item_id not in self.config["extra"]:
            return TRAY_DISABLED
        return TRAY_AUTO

    def apply_minimal(self):
        for item_id, combo in self.combos.items():
            if item_id in TRAY_MINIMAL_SHOWN:
                mode = TRAY_SHOWN
            elif item_id in TRAY_MINIMAL_AUTO:
                mode = TRAY_AUTO
            elif item_id in self.plasmoids and item_id not in self.config["extra"]:
                mode = TRAY_DISABLED  # what was already off stays off
            else:
                mode = TRAY_HIDDEN
            combo.setCurrentIndex(combo.findData(mode))

    def apply_all(self, mode):
        """Put every icon on the same choice; what is off stays off."""
        for item_id, combo in self.combos.items():
            if combo.currentData() != TRAY_DISABLED:
                combo.setCurrentIndex(combo.findData(mode))

    def apply_default(self):
        for combo in self.combos.values():
            combo.setCurrentIndex(combo.findData(TRAY_AUTO))

    def undo(self):
        for item_id, combo in self.combos.items():
            combo.setCurrentIndex(combo.findData(self.mode_of(item_id)))

    def save_preset(self):
        self.settings.setValue("tray_preset", json.dumps(
            {item_id: combo.currentData() for item_id, combo in self.combos.items()}))
        self.preset.setEnabled(True)

    def apply_preset(self):
        try:
            preset = json.loads(self.settings.value("tray_preset", "") or "{}")
        except ValueError:
            return
        for item_id, combo in self.combos.items():
            index = combo.findData(preset.get(item_id))
            if index >= 0:  # icons the preset doesn't know stay as they are
                combo.setCurrentIndex(index)

    def filter(self, text):
        """Show only the rows whose name contains the search text."""
        text = text.strip().lower()
        for row in range(self.form.rowCount()):
            label = self.form.itemAt(row, QFormLayout.ItemRole.LabelRole)
            field = self.form.itemAt(row, QFormLayout.ItemRole.FieldRole)
            if label is None or field is None:
                continue  # a section header
            self.form.setRowVisible(row, text in label.widget().text().lower())

    def apply(self):
        if self.config is None:
            return
        self.settings.setValue("tray_hide_new", self.hide_new.isChecked())
        rules = self.rules()
        if rules != tray_rules(self.settings):
            # New or changed rules: use them at once on the icons that are there.
            self.settings.setValue("tray_rules", json.dumps(rules))
            for item_id, combo in self.combos.items():
                mode = None if item_id in self.plasmoids else tray_rule_mode(
                    rules, item_id, self.label(item_id, self.titles))
                if mode:
                    combo.setCurrentIndex(combo.findData(mode))
        modes = {i: c.currentData() for i, c in self.combos.items()}
        if modes == {i: self.mode_of(i) for i in self.combos}:
            return  # nothing changed
        extra = [i for i in self.config["extra"] if modes.get(i) != TRAY_DISABLED]
        extra += [i for i, m in modes.items()
                  if i in self.plasmoids and m != TRAY_DISABLED and i not in extra]
        shown = [i for i, m in modes.items() if m == TRAY_SHOWN]
        hidden = [i for i, m in modes.items() if m == TRAY_HIDDEN]
        remember_tray(self.settings, self.config)
        self.plasma.set_tray_config(extra, shown, hidden)
        self.config = dict(self.config, extra=extra, shown=shown, hidden=hidden)
