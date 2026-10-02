# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The window shown the first time Tidy starts."""

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout,
                             QHBoxLayout, QLabel, QSpinBox, QVBoxLayout)

from .consts import APP_NAME, MODE_ACTIVITY, MODE_CLICK
from .i18n import tr


class Welcome(QDialog):
    """Shown the first time Tidy starts: the few choices that matter most."""

    def __init__(self, autohide):
        super().__init__()
        self.autohide = autohide
        settings = autohide.settings
        self.setWindowTitle(tr("Welcome to {app}").format(app=APP_NAME))
        self.setWindowIcon(QIcon.fromTheme("view-visible"))
        layout = QVBoxLayout(self)

        head = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(QIcon.fromTheme("view-visible").pixmap(48, 48))
        head.addWidget(icon)
        title = QLabel(tr("Welcome to {app}").format(app=APP_NAME))
        font = title.font()
        font.setPointSizeF(font.pointSizeF() * 1.5)
        font.setBold(True)
        title.setFont(font)
        head.addWidget(title, 1)
        layout.addLayout(head)

        intro = QLabel(tr("{app} keeps your desktop clean. It hides the desktop icons when you "
                          "don't need them and brings them back when you do. Three choices to "
                          "start with; everything can be changed later.").format(app=APP_NAME))
        intro.setWordWrap(True)
        layout.addWidget(intro)

        form = QFormLayout()
        self.timeout = QSpinBox(suffix=" s", minimum=3, maximum=3600)
        self.timeout.setValue(settings.value("timeout", 10, int))
        form.addRow(tr("Hide the icons after:"), self.timeout)
        self.mode = QComboBox()
        self.mode.addItem(tr("On any mouse movement or key press"), MODE_ACTIVITY)
        self.mode.addItem(tr("Only on a click on the desktop"), MODE_CLICK)
        self.mode.setCurrentIndex(max(0, self.mode.findData(settings.value("mode", MODE_ACTIVITY))))
        form.addRow(tr("Show again:"), self.mode)
        self.autostart = QCheckBox(tr("Start at login"))
        self.autostart.setChecked(True)
        form.addRow(self.autostart)
        layout.addLayout(form)

        more = QLabel(tr("There is more in the settings: drawers that tuck panel icons away, a "
                         "tidy system tray, focus mode, rules and profiles. {app} lives in the "
                         "system tray: click its eye icon to open the settings.")
                      .format(app=APP_NAME))
        more.setWordWrap(True)
        more.setEnabled(False)
        layout.addWidget(more)

        buttons = QDialogButtonBox()
        start = buttons.addButton(tr("Start"), QDialogButtonBox.ButtonRole.AcceptRole)
        start.setDefault(True)
        settings_button = buttons.addButton(tr("More settings…"),
                                            QDialogButtonBox.ButtonRole.ActionRole)
        buttons.accepted.connect(self.accept)
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(buttons)

    def save(self):
        a = self.autohide
        a.settings.setValue("timeout", self.timeout.value())
        a.settings.setValue("mode", self.mode.currentData())
        a.set_autostart(self.autostart.isChecked())
        a.after_settings(a.hidden, a.hidden_setup())

    def accept(self):
        self.save()
        super().accept()

    def open_settings(self):
        self.accept()
        QTimer.singleShot(0, self.autohide.show_settings)
