# Tidy (plasma-tidy)

Tidy keeps your KDE Plasma desktop and system tray clean.

- **Desktop:** hides your desktop icons when you're not using them, and brings them back on
  mouse movement, a click on the desktop, a screen corner or a shortcut.
- **System tray:** choose per icon whether it's shown, hidden under `^`, automatic or disabled.

It lives in the system tray as a small eye icon and stays out of the way: it never steals
focus, and it waits while you have a menu open or are editing your desktop.

The interface is available in English and Dutch. It follows your system language unless you
pick one in the settings.

## Requirements

- KDE Plasma 6 on **Wayland** (X11 is not supported)
- A desktop that uses the *Folder View* layout (the Plasma default when you have desktop icons)
- `python3-pyqt6` and `swayidle`

Tested on Fedora 44 with Plasma 6.7. Other distributions should work with the equivalent
packages but have not been tested.

## Install

There is no package yet; a Fedora COPR package is planned. Until then, install from source:

```sh
sudo dnf install python3-pyqt6 swayidle

git clone https://github.com/wispware/plasma-tidy.git
cd plasma-tidy
install -Dm755 plasma-tidy ~/.local/bin/plasma-tidy
install -Dm644 data/plasma-tidy.desktop ~/.local/share/applications/plasma-tidy.desktop
```

`~/.local/bin` must be on your `PATH` (it is by default on Fedora). Start **Tidy** from the
application menu, or run `plasma-tidy`. To have it start when you log in, tick
*Start at login* in the settings.

## Using it

Tidy shows an eye in the system tray: open when your icons are visible, crossed out when they
are hidden, grey when Tidy is switched off. Click it to open the settings; right-click for
the menu.

### Desktop

| Setting | What it does | Default |
| --- | --- | --- |
| Hide after | Seconds without activity before the icons disappear | 10 s |
| Show again | On any mouse movement or key press, or only on a click on the desktop | movement or key |
| With mouse button | Which buttons count as a click on the desktop (left, middle, right) | all three |
| Hide again | After that time without movement, or after a fixed time even while you move | without movement |
| Screen corner shows | Moving the mouse into this corner shows the icons | none |
| Activity in other windows doesn't count | The icons hide behind the window you're working in | on |
| Also hide the panel (taskbar) | Auto-hides the panel while the icons are hidden | off |
| Start at login | Adds or removes the autostart entry | off |
| Language | System language, English or Nederlands; takes effect at once | system language |

*Show desktop* (Meta+D) always brings the icons back.

If the screen corner you pick already has an action in System Settings → Screen Edges, both
will fire.

### System tray

The *System tray* tab lists every icon in your system tray. For each one, choose:

- **Automatic**: visible only when relevant
- **Show**: always visible in the panel
- **Hide**: only reachable through the `^` arrow
- **Off**: switched off completely (Plasma's own items only; icons that belong to an
  application can be shown or hidden, not switched off)

The *Minimal* button applies a minimal preset: network, volume and battery shown;
notifications, devices, camera and Caps Lock indicators automatic; everything else hidden.

### Shortcuts and command line

Tidy has three actions you can bind to a key in System Settings → Keyboard → Shortcuts →
Add New → Application → Tidy: show the icons, hide the icons, and switch Tidy on or off.

The same actions are available from the command line. Only one copy of Tidy runs at a time; a
second call passes its command to the running one.

```
plasma-tidy             start Tidy, or open the settings if it is already running
plasma-tidy --show      show the icons now
plasma-tidy --hide      hide the icons now
plasma-tidy --toggle    switch Tidy on or off
plasma-tidy --settings  open the settings
plasma-tidy --version   print the version
```

## How it works

- **Hiding** points the desktop's Folder View at an empty folder. The original folder is
  saved first and put back when the icons are shown, when you quit Tidy, when you log out,
  and (after a crash) the next time Tidy starts.
- **Idle time** comes from `swayidle`, which uses the Wayland idle-notify protocol.
- **Click to show** puts an invisible window on each screen, just above the desktop and below
  everything else. A small KWin script, loaded while Tidy runs, keeps it there, keeps it out
  of the task switcher, and handles the screen corner.

Tidy needs no root access and changes nothing outside your own Plasma configuration.

## Limitations

- Plasma 6 on Wayland only.
- The icons appear and disappear at once; there is no fade.
- Only icons are hidden. Widgets you placed on the desktop stay visible.
- Hiding reloads the desktop's Folder View, so Tidy postpones it while a menu is open or the
  desktop is in edit mode.
- Connecting or disconnecting a monitor while the icons are hidden has not been tested yet.

## Troubleshooting

**My desktop icons are gone and don't come back.** Start Tidy again, or quit it from the
tray menu: both restore the original folder. If that doesn't help, right-click the desktop →
Configure Desktop and Wallpaper → Location, and set it back to *Desktop folder*.

## Uninstall

Quit Tidy from the tray menu first, so your icons are restored. Then:

```sh
rm ~/.local/bin/plasma-tidy
rm ~/.local/share/applications/plasma-tidy.desktop
rm -f ~/.config/autostart/plasma-tidy.desktop
rm -rf ~/.config/plasma-tidy ~/.local/share/plasma-tidy
```

## Feedback

Bug reports and ideas are welcome in the
[issue tracker](https://github.com/wispware/plasma-tidy/issues).

## License and support

Made by Ivar. Free and open source under the GNU GPL v3 or later (see `LICENSE`).

If Tidy is useful to you, you can support development at
[ko-fi.com/wispware](https://ko-fi.com/wispware).
