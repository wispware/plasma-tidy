# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The Panel tab: the settings of the drawers."""

import json
import os

from PyQt6.QtGui import QIcon, QKeySequence
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout,
                             QFrame, QGridLayout, QGroupBox, QHBoxLayout, QKeySequenceEdit,
                             QLabel, QLineEdit, QMenu, QMessageBox, QPushButton, QScrollArea,
                             QSpinBox, QStackedWidget, QTabWidget, QVBoxLayout, QWidget)

from .consts import (ACTIVE_PLACES, ANIMATIONS, APP_NAME, DRAWER_SKIP, ICON_STYLES,
                     MARK_ATTENTION, MARK_COUNT, MARK_NONE, MARK_OPEN, OPEN_CLICK, OPEN_HOVER,
                     PANEL_PLACES, PLACE_AFTER, PLACE_BEFORE, PLACE_MANUAL, SCOPE_DRAWER,
                     SCOPE_PANEL, TASKS_ALL, TASKS_PINNED, TASK_PLUGINS)
from .i18n import tr
from .plasma import app_icon, panel_widget_name
from .widgets import drawer_texts, install_drawer


class DrawerPage(QWidget):
    """The settings of one drawer, in three parts: what is in it, how it opens and closes,
    and what its arrow looks like."""

    def __init__(self, drawer, widgets, number, on_label=None):
        super().__init__()
        self.drawer = drawer
        self.number = number
        self.panel_name = ""      # which panel it is in, when there are several
        self.on_label = on_label  # called when the name to show for this drawer changes
        self.targets = {}
        config = drawer["config"]
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        row = QHBoxLayout()
        row.addWidget(QLabel(tr("Name:")))
        self.name = QLineEdit(config["name"])
        self.name.setToolTip(tr("A name of your own for this drawer. Without one it is called "
                                "after what is in it."))
        self.name.textChanged.connect(self.relabel)
        row.addWidget(self.name, 1)
        outer.addLayout(row)

        parts = QTabWidget()
        outer.addWidget(parts)

        # --- contents ---
        page = QWidget()
        form = QFormLayout(page)
        box = QGroupBox(tr("In this drawer"))
        box_layout = QVBoxLayout(box)
        for widget in widgets:
            if widget["type"] in DRAWER_SKIP:
                continue
            check = QCheckBox(panel_widget_name(widget["type"]))
            check.setChecked(str(widget["id"]) in config["targets"])
            check.toggled.connect(self.update_enabled)
            check.toggled.connect(self.relabel)
            self.targets[widget["id"]] = (check, widget["type"])
            box_layout.addWidget(check)
        form.addRow(box)

        self.task_mode = QComboBox()
        self.task_mode.addItem(tr("Hide all programs, open ones too"), TASKS_ALL)
        self.task_mode.addItem(tr("Hide only pinned programs that are not open"), TASKS_PINNED)
        self.task_mode.setCurrentIndex(max(0, self.task_mode.findData(config["taskMode"])))
        self.task_mode.setToolTip(tr("Open programs are windows: with the second choice they "
                                     "stay in the panel and only the pinned icons of programs "
                                     "that are not running disappear."))
        form.addRow(tr("Task manager:"), self.task_mode)

        self.active_place = QComboBox()
        for key, label in ACTIVE_PLACES:
            self.active_place.addItem(tr(label), key)
        self.active_place.setCurrentIndex(max(0, self.active_place.findData(config["activePlace"])))
        self.active_place.setToolTip(tr("A pinned program that is open normally stays on its "
                                        "pinned spot, between the others. In front or at the "
                                        "back, the open programs stand together and the pinned "
                                        "ones slide out next to them."))
        form.addRow(tr("Open programs:"), self.active_place)

        # Per program: in the drawer, or kept in the panel.
        self.programs = {}
        try:
            listed = json.loads(config["taskList"] or "[]")
        except ValueError:
            listed = []
        self.programs_box = QGroupBox(tr("Programs that go in the drawer"))
        self.programs_box.setToolTip(tr("A program without a tick stays in the panel, also "
                                        "while the drawer is closed."))
        box_layout = QVBoxLayout(self.programs_box)
        if listed:
            inner = QWidget()
            grid = QGridLayout(inner)
            grid.setContentsMargins(0, 0, 0, 0)
            for index, program in enumerate(p for p in listed if isinstance(p, dict)
                                            and p.get("id")):
                check = QCheckBox(str(program.get("name") or program["id"]))
                check.setIcon(app_icon(program["id"]))
                check.setChecked(program["id"] not in config["taskKeep"])
                self.programs[program["id"]] = check
                grid.addWidget(check, index // 2, index % 2)
            area = QScrollArea(widgetResizable=True)
            area.setFrameShape(QFrame.Shape.NoFrame)
            area.setWidget(inner)
            area.setMaximumHeight(min(inner.sizeHint().height() + 8, 150))
            box_layout.addWidget(area)
        else:
            note = QLabel(tr("The programs of the task manager appear here a moment after the "
                             "drawer has one in it. Open this window again to see them."))
            note.setWordWrap(True)
            note.setEnabled(False)
            box_layout.addWidget(note)
        form.addRow(self.programs_box)
        parts.addTab(page, tr("Contents"))

        # --- opening and closing ---
        page = QWidget()
        layout = QVBoxLayout(page)
        box = QGroupBox(tr("Opening"))
        form = QFormLayout(box)
        self.open_on = QComboBox()
        self.open_on.addItem(tr("A click on the arrow"), OPEN_CLICK)
        self.open_on.addItem(tr("Pointing at the arrow (a click works too)"), OPEN_HOVER)
        self.open_on.setCurrentIndex(max(0, self.open_on.findData(config["openOn"])))
        self.open_on.currentIndexChanged.connect(self.update_enabled)
        form.addRow(tr("Open with:"), self.open_on)

        self.hover_delay = QSpinBox(suffix=" ms", minimum=0, maximum=3000, singleStep=50)
        self.hover_delay.setValue(config["hoverDelay"])
        form.addRow(tr("Pointing opens after:"), self.hover_delay)

        self.shortcut = QKeySequenceEdit(QKeySequence(drawer.get("shortcut", "")))
        self.shortcut.setClearButtonEnabled(True)
        self.shortcut.setMaximumSequenceLength(1)
        self.shortcut.setToolTip(tr("A shortcut for this drawer alone. The shortcut for all "
                                    "drawers at once is set in System Settings."))
        form.addRow(tr("Shortcut:"), self.shortcut)

        self.attention = QCheckBox(tr("Open when a program asks for attention"))
        self.attention.setChecked(config["openOnAttention"])
        form.addRow(self.attention)

        self.panel_open = QCheckBox(tr("Open with a click on an empty spot in the panel"))
        self.panel_open.setChecked(config["openOnPanelClick"])
        self.panel_open.setToolTip(tr("A left click where the panel is empty opens this drawer. "
                                      "If a drawer that closes on such a click is open, the "
                                      "click only closes; it opens when none is."))
        form.addRow(self.panel_open)

        self.on_desktop = QCheckBox(tr("Open when the desktop is shown"))
        self.on_desktop.setChecked(config["openOnDesktop"])
        self.on_desktop.setToolTip(tr("Works while Tidy is running."))
        form.addRow(self.on_desktop)
        layout.addWidget(box)

        box = QGroupBox(tr("Closing"))
        form = QFormLayout(box)
        self.auto_close = QComboBox()
        self.auto_close.addItem(tr("Never"), "")
        self.auto_close.addItem(tr("When the pointer leaves the drawer"), SCOPE_DRAWER)
        self.auto_close.addItem(tr("When the pointer leaves the panel"), SCOPE_PANEL)
        self.auto_close.setCurrentIndex(max(0, self.auto_close.findData(
            config["closeScope"] if config["autoClose"] else "")))
        self.auto_close.setToolTip(tr("The drawer is the arrow and the items it shows; empty "
                                      "panel space next to them is outside it."))
        self.auto_close.currentIndexChanged.connect(self.update_enabled)
        form.addRow(tr("Close by itself:"), self.auto_close)

        self.close_delay = QDoubleSpinBox(suffix=" s", minimum=0, maximum=60, singleStep=0.5,
                                          decimals=1)
        self.close_delay.setValue(config["closeDelay"] / 1000)
        form.addRow(tr("Closes after:"), self.close_delay)

        self.panel_click = QCheckBox(tr("Close with a click on an empty spot in the panel"))
        self.panel_click.setChecked(config["closeOnPanelClick"])
        form.addRow(self.panel_click)

        self.after_use = QCheckBox(tr("Close after a click on something in the drawer"))
        self.after_use.setChecked(config["closeAfterUse"])
        form.addRow(self.after_use)

        self.on_maximized = QCheckBox(tr("Close when a window that fills the screen comes to "
                                         "the front"))
        self.on_maximized.setChecked(config["closeOnMaximized"])
        form.addRow(self.on_maximized)
        layout.addWidget(box)
        layout.addStretch()
        parts.addTab(page, tr("Opening and closing"))

        # --- the arrow ---
        page = QWidget()
        form = QFormLayout(page)
        self.icon = QComboBox()
        for key, label in ICON_STYLES:
            self.icon.addItem(tr(label), key)
        self.icon.setCurrentIndex(max(0, self.icon.findData(config["icon"])))
        self.icon.setToolTip(tr("Without an icon the spot stays clickable and lights up under "
                                "the pointer."))
        self.icon.currentIndexChanged.connect(self.update_enabled)
        form.addRow(tr("Icon:"), self.icon)

        self.icon_custom = QLineEdit(config["iconCustom"])
        self.icon_custom.setPlaceholderText(tr("Icon name or image file"))
        self.icon_choose = QPushButton(tr("Choose…"))
        self.icon_choose.clicked.connect(self.choose_icon)
        row = QHBoxLayout()
        row.addWidget(self.icon_custom, 1)
        row.addWidget(self.icon_choose)
        form.addRow("", row)

        self.mark = QComboBox()
        self.mark.addItem(tr("None"), MARK_NONE)
        self.mark.addItem(tr("A dot when programs are open"), MARK_OPEN)
        self.mark.addItem(tr("The number of open programs"), MARK_COUNT)
        self.mark.addItem(tr("A dot only when a program asks for attention"), MARK_ATTENTION)
        self.mark.setCurrentIndex(max(0, self.mark.findData(config["indicator"])))
        self.mark.setToolTip(tr("Shown on the arrow while the drawer is closed and hides a task "
                                "manager with all its programs. The dot changes colour when a "
                                "program asks for attention."))
        form.addRow(tr("Mark on the closed drawer:"), self.mark)

        self.place = QComboBox()
        self.place.addItem(tr("Just before the items it hides"), PLACE_BEFORE)
        self.place.addItem(tr("Just after the items it hides"), PLACE_AFTER)
        self.place.addItem(tr("Where I put it myself"), PLACE_MANUAL)
        self.place.setCurrentIndex(max(0, self.place.findData(config["place"])))
        self.place.setToolTip(tr("After a task manager the arrow sits right behind the last "
                                 "program. The task manager then no longer fills the panel; "
                                 "the drawer does that instead."))
        form.addRow(tr("Place of the arrow:"), self.place)

        self.reverse = QCheckBox(tr("Arrow points the other way"))
        self.reverse.setChecked(config["reverseArrow"])
        form.addRow(self.reverse)

        self.animation = QComboBox()
        for key, label in ANIMATIONS:
            self.animation.addItem(tr(label), key)
        self.animation.setCurrentIndex(max(0, self.animation.findData(config["animation"])))
        self.animation.setToolTip(tr("Slide: the icons slide out from under the arrow at their "
                                     "normal size, like a drawer. Grow: they grow from small to "
                                     "their normal size. One by one: they come and go one after "
                                     "the other. Fade: they fade together and the rest closes "
                                     "up."))
        form.addRow(tr("Animation:"), self.animation)

        self.duration = QSpinBox(suffix=" ms", minimum=50, maximum=2000, singleStep=50)
        self.duration.setValue(config["animationDuration"])
        self.duration.setToolTip(tr("How long the movement takes; one by one, how long each "
                                    "icon takes."))
        form.addRow(tr("Speed:"), self.duration)

        hint = QLabel(tr("The arrow sits next to the items it hides. To place it yourself, "
                         "choose \"Where I put it myself\", right-click the panel, choose "
                         "Enter Edit Mode and drag it."))
        hint.setWordWrap(True)
        hint.setEnabled(False)
        form.addRow(hint)
        parts.addTab(page, tr("Appearance"))

        self.update_enabled()
        self.relabel()

    def auto_name(self):
        """What the drawer is called without a name of its own: after its contents."""
        inside = [check.text() for check, _ in self.targets.values() if check.isChecked()]
        return ", ".join(inside) or tr("Drawer {n}").format(n=self.number)

    def label(self):
        return self.name.text().strip() or self.auto_name()

    def relabel(self, *_):
        self.name.setPlaceholderText(self.auto_name())
        if self.on_label:
            self.on_label(self)

    def update_enabled(self):
        tasks = any(check.isChecked() and plugin in TASK_PLUGINS
                    for check, plugin in self.targets.values())
        self.task_mode.setEnabled(tasks)
        self.active_place.setEnabled(tasks)
        self.programs_box.setEnabled(tasks)
        self.hover_delay.setEnabled(self.open_on.currentData() == OPEN_HOVER)
        self.close_delay.setEnabled(bool(self.auto_close.currentData()))
        custom = self.icon.currentData() == "custom"
        self.icon_custom.setEnabled(custom)
        self.icon_choose.setEnabled(custom)

    def choose_icon(self):
        name, _ = QFileDialog.getOpenFileName(
            self, tr("Choose an image"), os.path.dirname(self.icon_custom.text()),
            "(*.svg *.svgz *.png *.jpg *.jpeg *.webp)")
        if name:
            self.icon_custom.setText(name)

    def values(self):
        return {"name": self.name.text().strip(),
                "targets": [str(i) for i, (check, _) in self.targets.items()
                            if check.isChecked()],
                "taskMode": self.task_mode.currentData(),
                "taskKeep": [i for i in self.drawer["config"]["taskKeep"]
                             if i not in self.programs]
                            + [i for i, check in self.programs.items() if not check.isChecked()],
                "activePlace": self.active_place.currentData(),
                "openOn": self.open_on.currentData(),
                "hoverDelay": self.hover_delay.value(),
                "openOnAttention": self.attention.isChecked(),
                "openOnDesktop": self.on_desktop.isChecked(),
                "autoClose": bool(self.auto_close.currentData()),
                "closeScope": self.auto_close.currentData() or self.drawer["config"]["closeScope"],
                "closeDelay": round(self.close_delay.value() * 1000),
                "closeOnPanelClick": self.panel_click.isChecked(),
                "openOnPanelClick": self.panel_open.isChecked(),
                "closeAfterUse": self.after_use.isChecked(),
                "closeOnMaximized": self.on_maximized.isChecked(),
                "icon": self.icon.currentData(),
                "iconCustom": self.icon_custom.text().strip(),
                "indicator": self.mark.currentData(),
                "place": self.place.currentData(),
                "reverseArrow": self.reverse.isChecked(),
                "animation": self.animation.currentData(),
                "animationDuration": self.duration.value()}

    def apply(self, plasma):
        config = self.drawer["config"]
        changed = {k: v for k, v in self.values().items() if v != config[k]}
        if changed:
            plasma.set_drawer_config(self.drawer["id"], changed)
            config.update(changed)
        if "targets" in changed or "place" in changed:
            # The arrow belongs next to what it hides.
            plasma.place_drawer(self.drawer["id"], config["targets"], config["place"])
        shortcut = self.shortcut.keySequence().toString(QKeySequence.SequenceFormat.PortableText)
        if shortcut != self.drawer.get("shortcut", ""):
            plasma.set_drawer_shortcut(self.drawer["id"], shortcut)
            self.drawer["shortcut"] = shortcut


class DrawerTab(QWidget):
    """Tab for the panel drawers: arrows that tuck panel widgets away."""

    def __init__(self, autohide):
        super().__init__()
        self.plasma = autohide.plasma
        self.pages = []
        self.panels = []
        layout = QVBoxLayout(self)

        intro = QLabel(tr("A drawer is an arrow in the panel. It tucks the widgets you choose "
                          "away and brings them back when you click or point at the arrow."))
        intro.setWordWrap(True)
        layout.addWidget(intro)

        row = QHBoxLayout()
        row.addWidget(QLabel(tr("Drawer:")))
        self.selector = QComboBox()
        self.selector.setProperty("tidyNoSetting", True)
        self.rebuilt = None  # called with this tab when its pages have been made anew
        row.addWidget(self.selector, 1)
        self.add_button = QPushButton(QIcon.fromTheme("list-add"), tr("Add a drawer"))
        self.add_button.clicked.connect(self.add)
        row.addWidget(self.add_button)
        self.remove_button = QPushButton(QIcon.fromTheme("list-remove"), tr("Remove"))
        self.remove_button.clicked.connect(self.remove)
        row.addWidget(self.remove_button)
        layout.addLayout(row)

        self.stack = QStackedWidget()
        self.selector.currentIndexChanged.connect(self.stack.setCurrentIndex)
        layout.addWidget(self.stack)

        box = QGroupBox(tr("All drawers"))
        box_layout = QVBoxLayout(box)
        self.follow = QCheckBox(tr("Close and open together with the desktop icons"))
        self.follow.setChecked(autohide.settings.value("drawer_follow", False, bool))
        box_layout.addWidget(self.follow)
        layout.addWidget(box)
        layout.addStretch()
        self.rebuild()

    def rebuild(self, select=None):
        """Read the drawers from the panels again and show a page for each."""
        self.selector.blockSignals(True)
        self.selector.clear()
        while self.stack.count():
            page = self.stack.widget(0)
            self.stack.removeWidget(page)
            page.deleteLater()
        self.pages = []
        self.panels = self.plasma.panel_widgets()
        by_id = {panel["panel"]: panel for panel in self.panels}
        for number, drawer in enumerate(self.plasma.drawers(), 1):
            panel = by_id.get(drawer["panel"])
            if not panel:
                continue
            page = DrawerPage(drawer, panel["widgets"], number, self.relabel)
            # Which panel only matters when there is more than one.
            page.panel_name = (tr(PANEL_PLACES.get(panel["location"], "Panel"))
                               if len(self.panels) > 1 else "")
            self.pages.append(page)
            self.stack.addWidget(page)
            self.selector.addItem(self.label(page), drawer["id"])
        if not self.pages:
            empty = QLabel(tr("No drawer yet. Add one to hide panel icons behind an arrow."))
            empty.setWordWrap(True)
            empty.setEnabled(False)
            self.stack.addWidget(empty)
        self.selector.blockSignals(False)
        self.selector.setEnabled(bool(self.pages))
        self.remove_button.setEnabled(bool(self.pages))
        index = max(0, self.selector.findData(select)) if select is not None else 0
        self.selector.setCurrentIndex(index)
        self.stack.setCurrentIndex(index)
        if self.rebuilt:
            self.rebuilt(self)

    @staticmethod
    def label(page):
        return f"{page.label()} — {page.panel_name}" if page.panel_name else page.label()

    def relabel(self, page):
        if page in self.pages:
            self.selector.setItemText(self.pages.index(page), self.label(page))

    def add(self):
        if not self.panels:
            QMessageBox.warning(self, APP_NAME, tr("No panel found."))
            return
        panel = self.panels[0]
        if len(self.panels) > 1:
            # Several panels: ask which one.
            menu = QMenu(self)
            for candidate in self.panels:
                action = menu.addAction(tr(PANEL_PLACES.get(candidate["location"], "Panel")))
                action.setData(candidate["panel"])
            chosen = menu.exec(self.add_button.mapToGlobal(self.add_button.rect().bottomLeft()))
            if not chosen:
                return
            panel = next(p for p in self.panels if p["panel"] == chosen.data())
        # A new drawer starts with the task manager in it. If another drawer has that
        # already, with the system tray; failing that, empty. Its arrow sits next to them.
        self.apply()
        taken = {i for page in self.pages for i in page.drawer["config"]["targets"]}
        targets = []
        for plugins in (TASK_PLUGINS, ("org.kde.plasma.systemtray",)):
            targets = [str(w["id"]) for w in panel["widgets"]
                       if w["type"] in plugins and str(w["id"]) not in taken]
            if targets:
                break
        config = dict(drawer_texts(), targets=targets)
        install_drawer()
        new_id = self.plasma.add_drawer(panel["panel"], config)
        if new_id is None:
            QMessageBox.warning(self, APP_NAME, tr("The drawer could not be added to the panel."))
        self.rebuild(select=new_id)

    def remove(self):
        drawer_id = self.selector.currentData()
        if drawer_id is None:
            return
        self.apply()
        self.plasma.remove_drawer(drawer_id)
        self.rebuild()

    def apply(self):
        for page in self.pages:
            page.apply(self.plasma)
