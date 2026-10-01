# Tidy (plasma-tidy)

Tidy keeps your KDE Plasma desktop, panel and system tray clean.

- **Desktop:** hides your desktop icons when you're not using them, and brings them back on
  mouse movement, a click on the desktop, a screen corner or a shortcut.
- **Panel:** a drawer, an arrow in the panel, tucks the programs and widgets you choose away
  and brings them back on a click or when you point at it.
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

### Panel

The *Panel* tab adds drawers to your panel. A drawer is a small arrow that tucks the widgets
you choose away. Click the arrow to close or open the drawer. If you like, it also opens when
you point at the arrow, and closes by itself or on a click on an empty spot of the panel.

*Add a drawer* puts one just before the task manager, with the task manager in it; a second
drawer starts with the system tray. The arrow sits next to the widgets it hides and moves
along when you change them. To place it yourself, choose *Where I put it myself*, right-click
the panel, choose *Enter Edit Mode* and drag it.

| Setting | What it does | Default |
| --- | --- | --- |
| In this drawer | Which of the panel's widgets the drawer hides | the task manager |
| Task manager | Hide all programs, open ones too; or only the pinned programs that are not open | all programs |
| Open with | A click on the arrow, or pointing at it (a click always works) | click |
| Pointing opens after | How long the pointer must rest on the arrow | 200 ms |
| Close by itself | Never, when the pointer leaves the drawer (the arrow and the items it shows), or when it leaves the panel | never |
| Closes after | How long after the pointer left | 2 s |
| Close with a click on an empty spot in the panel | A left click where the panel is empty closes the drawer; a click on a widget does what it always did | off |
| Open when a program asks for attention | A hidden program that wants you opens the drawer | on |
| Sliding animation | Slide and fade, or switch at once | on |
| Arrow points the other way | Closed, the arrow points the way the drawer opens: away from the nearest end of the panel. This flips it | off |
| Place of the arrow | Just before the items it hides, just after them, or where you put it yourself | just before |
| Close and open the drawers together with the desktop icons | The drawers follow Tidy's hiding and showing of the desktop icons | off |

A widget that fills the panel, usually the task manager, keeps its place while hidden, so the
rest of the panel does not jump. Other widgets give up their space.

With the arrow *just after* a task manager, it sits right behind the last program. For that
the task manager stops filling the panel (its own *Fill free space on panel* setting) and the
drawer fills it instead; the setting is put back when you move the arrow or remove the drawer.

With *only the pinned programs*, open programs stay in the panel: they are windows. Tidy
remembers the pinned list while the drawer is closed and puts it back when it opens,
including anything you pinned in the meantime.

### System tray

The *System tray* tab lists every icon in your system tray. For each one, choose:

- **Automatic**: visible only when relevant
- **Show**: always visible in the panel
- **Hide**: only reachable through the `^` arrow
- **Off**: switched off completely (Plasma's own items only; icons that belong to an
  application can be shown or hidden, not switched off)

Three buttons set every icon at once; items that are switched off stay off, and nothing
changes until you press OK:

- **Minimal**: network, volume and battery shown; notifications, devices, camera and Caps Lock
  indicators automatic; everything else hidden
- **Show all**: every icon always visible in the panel
- **Hide all**: every icon under the `^` arrow

### Shortcuts and command line

Tidy has four actions you can bind to a key in System Settings → Keyboard → Shortcuts →
Add New → Application → Tidy: show the icons, hide the icons, switch Tidy on or off, and open
or close the panel drawers.

The same actions are available from the command line. Only one copy of Tidy runs at a time; a
second call passes its command to the running one.

```
plasma-tidy             start Tidy, or open the settings if it is already running
plasma-tidy --show      show the icons now
plasma-tidy --hide      hide the icons now
plasma-tidy --toggle    switch Tidy on or off
plasma-tidy --settings  open the settings
plasma-tidy --drawer-open    open the panel drawers
plasma-tidy --drawer-close   close the panel drawers
plasma-tidy --drawer-toggle  close them if one is open, otherwise open them
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
- **The drawer** is a small Plasma widget that ships inside Tidy and is written to
  `~/.local/share/plasma/plasmoids/` when Tidy starts. Plasma offers no way to hide another
  widget, so the drawer reaches into the panel's layout and makes its neighbours invisible. It
  changes two settings of a task manager, and only when you ask for it: in *only the pinned
  programs* mode it empties the pinned list while closed, and with the arrow *just after* the
  task manager it switches off *Fill free space on panel*. Both are put back when the drawer
  opens, moves or is removed. The drawer keeps working when Tidy is not running; Tidy is only
  needed to change its settings.

Tidy needs no root access and changes nothing outside your own Plasma configuration.

## Limitations

- Plasma 6 on Wayland only.
- The desktop icons appear and disappear at once; there is no fade.
- On the desktop only icons are hidden. Widgets you placed there stay visible.
- Hiding reloads the desktop's Folder View, so Tidy postpones it while a menu is open or the
  desktop is in edit mode.
- Connecting or disconnecting a monitor while the icons are hidden has not been tested yet.
- The drawer depends on how Plasma builds its panel, which is not a public interface. It is
  tested with Plasma 6.7. If a Plasma update changes the panel, the drawer stops hiding
  things; nothing is lost, your widgets simply stay visible.
- A new version of the drawer is picked up when Plasma starts, so after updating Tidy, log out
  and in once.
- Closing by itself follows the pointer inside the panel. A window preview or a menu that
  opens above the panel counts as having left the drawer.

## Troubleshooting

**My desktop icons are gone and don't come back.** Start Tidy again, or quit it from the
tray menu: both restore the original folder. If that doesn't help, right-click the desktop →
Configure Desktop and Wallpaper → Location, and set it back to *Desktop folder*.

**A widget stays hidden in the panel.** Click the drawer's arrow, or remove the drawer in the
*Panel* tab: both bring everything back. Restarting Plasma (log out and in) does too.

## Uninstall

Remove your drawers in the *Panel* tab and quit Tidy from the tray menu, so your panel and
icons are restored. Then:

```sh
rm ~/.local/bin/plasma-tidy
rm ~/.local/share/applications/plasma-tidy.desktop
rm -f ~/.config/autostart/plasma-tidy.desktop
rm -rf ~/.config/plasma-tidy ~/.local/share/plasma-tidy
rm -rf ~/.local/share/plasma/plasmoids/io.github.wispware.plasmatidy.drawer
```

## Feedback

Bug reports and ideas are welcome in the
[issue tracker](https://github.com/wispware/plasma-tidy/issues).

## License and support

Made by Ivar. Free and open source under the GNU GPL v3 or later (see `LICENSE`).

If Tidy is useful to you, you can support development at
[ko-fi.com/wispware](https://ko-fi.com/wispware).
