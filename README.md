# Tidy (plasma-tidy)

Tidy keeps your KDE Plasma desktop, panel and system tray clean.

- **Desktop:** hides your desktop icons when you're not using them, and brings them back on
  mouse movement, a click on the desktop, a screen corner or a shortcut.
- **Panel:** a drawer, an arrow in the panel, tucks the programs and widgets you choose away
  and brings them back on a click or when you point at it.
- **Focus mode:** one shortcut hides the icons, closes the drawers and trims the system tray,
  and keeps it that way until you switch it off.
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

In the settings window, *Apply* puts your changes to work and keeps the window open, so you
can try them out; *OK* does the same and closes it. *Apply* becomes available as soon as you
change something.

### Desktop

| Setting | What it does | Default |
| --- | --- | --- |
| Hide after | Seconds without activity before the icons disappear | 10 s |
| Show again | On any mouse movement or key press, or only on a click on the desktop | movement or key |
| With mouse button | Which buttons count as a click on the desktop (left, middle, right) | all three |
| Hide again | After that time without movement, or after a fixed time even while you move | without movement |
| Screen corner shows | Moving the mouse into this corner shows the icons | none |
| Activity in other windows doesn't count | The icons hide behind the window you're working in; moving the mouse over the desktop itself always counts | on |
| Moving over the panel does count | With the setting above: moving the mouse over the panel keeps the icons too, like moving over the desktop | on |
| Also hide the panel (taskbar) | Auto-hides the panel while the icons are hidden | off |
| Fade the icons in and out | The icons fade away and back instead of switching at once, in the time you set; uses an invisible helper widget on the desktop | off, 300 ms |
| Hide the icons on | With more than one screen: the screens whose icons are hidden; the others keep theirs | every screen |

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

You can give a drawer a name; without one it is called after what is in it. The name shows in
the list of drawers and in the arrow's tooltip.

The settings of a drawer come in three parts.

*Contents*

| Setting | What it does | Default |
| --- | --- | --- |
| In this drawer | Which of the panel's widgets the drawer hides | the task manager |
| Task manager | Hide all programs, open ones too; or only the pinned programs that are not open | all programs |
| Open programs | Where open programs stand in the task manager: on their pinned spot, all in front, or all at the back | pinned spot |

*Opening and closing*

| Setting | What it does | Default |
| --- | --- | --- |
| Open with | A click on the arrow, or pointing at it (a click always works) | click |
| Pointing opens after | How long the pointer must rest on the arrow | 200 ms |
| Shortcut | A key for this drawer alone | none |
| Open when a program asks for attention | A hidden program that wants you opens the drawer | on |
| Open when the desktop is shown | Opens when you go to the desktop; needs Tidy running | off |
| Close by itself | Never, when the pointer leaves the drawer (the arrow and the items it shows), or when it leaves the panel | never |
| Closes after | How long after the pointer left | 2 s |
| Close with a click on an empty spot in the panel | A left click where the panel is empty closes the drawer; a click on a widget does what it always did | off |
| Close after a click on something in the drawer | Closes once you have started or picked something; a pop-up it opened is waited for | off |
| Close when a window that fills the screen comes to the front | Closes each time a maximized or full-screen window becomes the active one | off |

*Appearance*

| Setting | What it does | Default |
| --- | --- | --- |
| Icon | Arrow, double arrow, triangle, dots, menu lines, grip, an icon or image of your own, or none at all: the spot then stays clickable and lights up under the pointer | arrow |
| Mark on the closed drawer | A dot on the arrow when hidden programs are open, their number, a dot only when one asks for attention, or nothing. Applies when the drawer hides a task manager with all its programs | a dot |
| Arrow points the other way | Closed, the arrow points the way the drawer opens: away from the nearest end of the panel. This flips it | off |
| Place of the arrow | Just before the items it hides, just after them, or where you put it yourself | just before |
| Animation | Slide: the icons of a task manager slide out from under the arrow at their normal size, like a drawer. Grow: they grow from small to their normal size. One by one: they come and go one after the other. Fade: they fade together and the rest closes up | slide |
| Speed | How long the movement takes; one by one, how long each icon takes | 250 ms |

Below the drawers, *All drawers: close and open together with the desktop icons* makes every
drawer follow Tidy's hiding and showing of the desktop icons (off by default).

A drawer also has a settings page of its own: right-click the arrow and choose *Configure Tidy
Drawer*. It has the same settings except the place of the arrow, and it works when Tidy is
not running.

A task manager is not hidden as a whole: its icons are, one by one, so they can slide away
smoothly. The task manager itself keeps its place, and the rest of the panel does not jump.
Other widgets give up their space.

With *Open programs* in front or at the back, the open programs stand together and the pinned
ones slide out next to them, instead of appearing in between.

With the arrow *just after* a task manager, it sits right behind the last program. For that
the task manager stops filling the panel (its own *Fill free space on panel* setting) and the
drawer fills it instead; the setting is put back when you move the arrow or remove the drawer.

With *only the pinned programs*, open programs stay in the panel and only the icons of pinned
programs that are not running slide away. Start one of them some other way and its icon
appears.

### System tray

The *System tray* tab lists every icon in your system tray. For each one, choose:

- **Automatic**: visible only when relevant
- **Show**: always visible in the panel
- **Hide**: only reachable through the `^` arrow
- **Off**: switched off completely (Plasma's own items only; icons that belong to an
  application can be shown or hidden, not switched off)

The buttons below the list set every icon at once. Nothing changes until you press *Apply* or
*OK*.

- **Minimal**: network, volume and battery shown; notifications, devices, camera and Caps Lock
  indicators automatic; everything else hidden
- **Show all**, **Hide all**, **All automatic**: every icon on that choice; items that are
  switched off stay off
- **Plasma default**: everything switched on and automatic
- **Save as my preset** and **My preset**: keep an arrangement of your own and apply it again
- **Undo**: back to how the list was when you opened the window

The search field above the list narrows it down by name.

With *New icons go under the ^ arrow by themselves*, an application that shows a tray icon for
the first time gets it hidden. Icons you already had are left as they are. It works while Tidy
is running.

### General

| Setting | What it does | Default |
| --- | --- | --- |
| Start at login | Adds or removes the autostart entry | off |
| Language | System language, English or Nederlands; takes effect at once | system language |

**Profiles** keep all settings together: the desktop, the drawers, the system tray and focus
mode. *Save current as…* stores what is in the window under a name; *Apply* switches to a
profile, and so does the *Profiles* menu of the tray icon. A profile changes the settings of the
drawers that are in your panel; it does not add or remove drawers.

*Export…* writes all settings and profiles to a file and *Import…* reads them back, for
instance on another computer. *Defaults…* puts every setting back to how Tidy comes: your
drawers stay, with what is in them, and the system tray is left alone.

*Restore everything* is on this tab too.

### Focus mode

Focus mode tucks everything away at once and keeps it away: the desktop icons are hidden, the
panel drawers closed and the system tray set to *Minimal*, and nothing comes back on mouse
movement, a click on the desktop or the screen corner. Switch it on and off in the tray menu,
on the *Focus mode* tab, with a shortcut or with `plasma-tidy --focus`. Switching it off puts
everything back as it was.

| Setting | What focus mode does | Default |
| --- | --- | --- |
| Hide the desktop icons | Hides them and keeps them hidden | on |
| Close the panel drawers | Closes every drawer; a drawer still opens on its arrow | on |
| Set the system tray to Minimal | Network, volume and battery visible, the rest under `^` | on |
| Auto-hide the panel | The panel slides away until you move to the screen edge | off |

Opening the settings and pressing OK, switching Tidy off, and *Restore everything* end focus
mode. After a crash or a logout in focus mode, Tidy puts everything back the next time it
starts.

### Restore everything

*Restore everything* (in the tray menu and on the *General* tab) puts your desktop
back as if Tidy were not there. It shows the desktop icons, the panel and everything in the
drawers, and puts back the Plasma settings Tidy changed: the desktop folder, the panel's
visibility, and a task manager's pinned list and *Fill free space on panel*. If you tick the
box, the system tray goes back to how it was before Tidy first changed it.

Tidy is then switched off and the drawers are paused: their arrows stay in the panel, dimmed,
and hide nothing. Switch Tidy on again in the tray menu, or click an arrow, to resume. Your
settings are kept.

### Shortcuts and command line

Tidy has six actions you can bind to a key in System Settings → Keyboard → Shortcuts →
Add New → Application → Tidy: show the icons, hide the icons, switch Tidy on or off, focus
mode on or off, open or close the panel drawers, and restore everything.

The same actions are available from the command line. Only one copy of Tidy runs at a time; a
second call passes its command to the running one.

```
plasma-tidy             start Tidy, or open the settings if it is already running
plasma-tidy --show      show the icons now
plasma-tidy --hide      hide the icons now
plasma-tidy --toggle    switch Tidy on or off
plasma-tidy --settings  open the settings
plasma-tidy --focus     switch focus mode on or off
plasma-tidy --drawer-open    open the panel drawers
plasma-tidy --drawer-close   close the panel drawers
plasma-tidy --drawer-toggle  close them if one is open, otherwise open them
plasma-tidy --restore   restore everything and switch Tidy off (does not touch the tray)
plasma-tidy --version   print the version
```

## How it works

- **Hiding** points the desktop's Folder View at an empty folder. The original folder is
  saved first and put back when the icons are shown, when you quit Tidy, when you log out,
  and (after a crash) the next time Tidy starts.
- **Idle time** comes from `swayidle`, which uses the Wayland idle-notify protocol.
- **Whose activity counts** comes from the same KWin script: it tells Tidy whether the desktop
  is the active window and whether the pointer is above the desktop. It never sees what you
  type or click.
- **Click to show** puts an invisible window on each screen, just above the desktop and below
  everything else. A small KWin script, loaded while Tidy runs, keeps it there, keeps it out
  of the task switcher, and handles the screen corner.
- **The drawer** is a small Plasma widget that ships inside Tidy and is written to
  `~/.local/share/plasma/plasmoids/` when Tidy starts. Plasma offers no way to hide another
  widget, so the drawer reaches into the panel's layout and makes its neighbours invisible; in
  a task manager it does that per icon. It changes one setting of a task manager, and only
  when you ask for it: with the arrow *just after* the task manager it switches off *Fill
  free space on panel*, and puts that back when the arrow moves or the drawer is removed. The
  drawer keeps working when Tidy is not running; Tidy is only needed to change its settings.
- **Fading the desktop icons** needs something inside Plasma as well: a helper widget that
  Tidy puts on each desktop. It is invisible and only changes how see-through the layer of
  icons is. Hiding itself works as described above; without the helper the icons simply switch
  at once.

Tidy needs no root access and changes nothing outside your own Plasma configuration.

## Limitations

- Plasma 6 on Wayland only.
- On the desktop only icons are hidden. Widgets you placed there stay visible.
- Hiding reloads the desktop's Folder View, so Tidy postpones it while a menu is open or the
  desktop is in edit mode.
- Connecting or disconnecting a monitor while the icons are hidden has not been tested yet.
- The drawer and the fade depend on how Plasma builds its panel, task manager and desktop,
  which is not a public interface. They are tested with Plasma 6.7. If a Plasma update changes
  these, the drawer stops hiding things or the icons stop fading; nothing is lost, your
  widgets simply stay visible.
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

**Something is hidden and I don't know why.** Choose *Restore everything* in Tidy's tray menu,
or run `plasma-tidy --restore`.

## Uninstall

Remove your drawers in the *Panel* tab, switch off *Fade the icons in and out*, and quit Tidy
from the tray menu, so your panel and desktop are as they were. Then:

```sh
rm ~/.local/bin/plasma-tidy
rm ~/.local/share/applications/plasma-tidy.desktop
rm -f ~/.config/autostart/plasma-tidy.desktop
rm -rf ~/.config/plasma-tidy ~/.local/share/plasma-tidy
rm -rf ~/.local/share/plasma/plasmoids/io.github.wispware.plasmatidy.drawer
rm -rf ~/.local/share/plasma/plasmoids/io.github.wispware.plasmatidy.fade
```

## Feedback

Bug reports and ideas are welcome in the
[issue tracker](https://github.com/wispware/plasma-tidy/issues).

## License and support

Made by Ivar. Free and open source under the GNU GPL v3 or later (see `LICENSE`).

If Tidy is useful to you, you can support development at
[ko-fi.com/wispware](https://ko-fi.com/wispware).
