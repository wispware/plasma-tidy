# Changes

## 0.3.0 — not released yet

The first version meant for others. Since 0.2.0:

**Desktop icons**
- Fading, hiding the desktop widgets along with the icons (each widget can stay), a double-click
  on an empty spot hides them, and moving over the panel can count as activity.
- Hiding is done by a small helper on the desktop: instant, without reloading the desktop.
  The old way (an empty folder) stays as a fallback.
- Tidy no longer polls: it sleeps until something happens.

**Panel drawers**
- Open with a click on an empty spot of the panel; close when the pointer leaves, after use,
  when a window fills the screen, or when the panel slides out of view.
- A pop-up drawer that leaves the panel as it is (also for panels as long as their contents),
  in a row, column, grid or list, with or without a background.
- Which programs go in a drawer, where open programs stand, animations (slide, grow, one by
  one, fade), a mark on a closed drawer, names, and an arrow that can take no room at all.
- A drawer stays open under a program's pop-up or a menu.

**More**
- Focus mode: everything away until you switch it off.
- Rules and profiles: switch settings by power, screen, time, program, virtual desktop or
  activity; export and import.
- A peek key: hold it to see everything for a moment.
- Balloons and previews: Plasma's balloons on or off, the pop-up of a program with or without
  its preview (or only the preview), and both floating above the panel.
- Restore everything; switching Tidy off or quitting leaves Plasma as it is without Tidy.
- A welcome window on the first start.

**Under the hood**
- Lighter: about 24 MB of memory, no processor time at rest.
- Tidy checks what it reaches into in Plasma and KWin and says once what does not work in a new
  Plasma version; `plasma-tidy --check` lists it all.
- `plasma-tidy --report` for bug reports, without personal data.
- A package specification for Fedora (COPR), and 99 tests.

## 0.2.0 — 2026-10-01

- Panel drawers: an arrow in the panel that tucks the programs and widgets you choose away.

## 0.1.0 — 2026-09-30

- First version: hides the desktop icons when you are not using them and brings them back on
  mouse movement, a click on the desktop, a screen corner or a shortcut; organises the system
  tray.
