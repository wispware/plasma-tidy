# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The package for Fedora (COPR). Build it with:
#   rpmbuild -ba packaging/plasma-tidy.spec   (with the source tarball in ~/rpmbuild/SOURCES)
# or let COPR build it from the tagged release on GitHub.

%bcond_without tests

Name:           plasma-tidy
Version:        0.3.0
Release:        1%{?dist}
Summary:        Keeps the KDE Plasma desktop, panel and system tray tidy

# The program is GPL-3.0-or-later. The Wispware name and logo (wispware.svg, shown on the
# About page) are not covered by that licence; see the README.
License:        GPL-3.0-or-later AND LicenseRef-Wispware-Logo
URL:            https://github.com/wispware/plasma-tidy
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
%if %{with tests}
BuildRequires:  python3-pyqt6
BuildRequires:  dbus-daemon
%endif

Requires:       python3-pyqt6
# The idle watcher.
Requires:       swayidle
# Tidy works with Plasma's shell and KWin through their scripting interfaces, and writes
# Plasma's balloon setting with kwriteconfig6.
Requires:       plasma-workspace
Requires:       kwin
Requires:       kf6-kconfig

%description
Tidy keeps your KDE Plasma desktop, panel and system tray clean. It hides the
desktop icons when you are not using them and brings them back when you need
them; puts drawers in the panel that tuck programs and widgets away; trims the
system tray; and has a focus mode, rules and profiles, a peek key, and settings
for Plasma's balloons and the pop-ups of programs in the panel. It is light:
about 24 MB of memory and no processor time at rest.

Tidy is made for Plasma 6 on Wayland.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build: Tidy is Python, and its Plasma widgets are written out when it starts.

%install
install -d %{buildroot}%{_datadir}/%{name}
cp -a src/plasma_tidy %{buildroot}%{_datadir}/%{name}/
find %{buildroot}%{_datadir}/%{name} -name __pycache__ -prune -exec rm -rf {} +
# Tidy's own modules are not for other programs: they stay in its own folder, and this
# small starter puts that folder first.
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!%{python3}
import sys

sys.path.insert(0, "%{_datadir}/%{name}")

from plasma_tidy.main import main

sys.exit(main())
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications data/%{name}.desktop
%py_byte_compile %{python3} %{buildroot}%{_datadir}/%{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%if %{with tests}
# The tests need a session bus and no screen.
QT_QPA_PLATFORM=offscreen dbus-run-session -- %{python3} -m unittest
%endif

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop

%changelog
* Sun Oct 04 2026 Ivar <hallo@wispware.dev> - 0.3.0-1
- First package; see CHANGELOG.md
