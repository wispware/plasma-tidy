# Changes

## 0.3.2 — not released yet

- Tidy's widgets no longer fill Plasma's log with "No signal handler" lines.

## 0.3.1 — 2026-10-06

- The drawer that the welcome window adds starts closed: the programs are tucked away at once.
- In a drawer's settings the list of programs keeps its rows together; room to spare stays
  below the list instead of between the rows.

## 0.3.0 — 2026-10-06

The first version meant for others. Since 0.2.0:

**Desktop icons**
- Icons that fade stay where they are: a panel that hides with them waits until they are gone.
- Fading, hiding the desktop widgets along with the icons (each widget can stay), a double-click
  on an empty spot hides them, and moving over the panel can count as activity.
- Hiding is done by a small helper on the desktop: instant, without reloading the desktop.
  The old way (an empty folder) stays as a fallback.
- Tidy no longer polls: it sleeps until something happens.

**Panel drawers**
- Open with a click on an empty spot of the panel; close when the pointer leaves, after use,
  when a window fills the screen, or when the panel slides out of view.
- A pop-up drawer that leaves the panel as it is (also for panels as long as their contents),
  in a row, column, grid or list, with or without a background, above the arrow or at the
  start, in the middle or at the end of the panel. It ends where the panel ends; at the edge
  of the screen a pointer pushed against that edge is on the icons.
- A row or a column in a pop-up is as thick as the panel, with icons as large as the panel's.
- Drag a program in a pop-up to another place, as in the panel.
- With open programs sent to the front or the back, a pinned program is back on its own spot
  when you close it, and dragging no longer moves the spot of a program that is open.
- An arrow without room stays out of the panel while its pop-up is open (the panel no longer
  shifts a little), and the pop-up lines up with the widget beside it.
- Which programs go in a drawer, where open programs stand, animations (slide, grow, one by
  one, fade), a mark on a closed drawer, names, and an arrow that can take no room at all.
- A drawer stays open under a program's pop-up or a menu, and while you drag a program to
  another place.
- Close a program from its pop-up and the panel and the drawer stay three seconds, to choose
  something else. Start a program from a drawer and the panel can stay a time you set.

**More**
- The panel can come into view by itself after you minimise (or close) a window.
- Focus mode: everything away until you switch it off.
- Rules and profiles: switch settings by power, screen, time, program, virtual desktop or
  activity; export and import.
- A peek key: hold it to see everything for a moment.
- Balloons and previews: Plasma's balloons on or off, the pop-up of a program with or without
  its preview (or only the preview), and both floating above the panel.
- Restore everything; switching Tidy off or quitting leaves Plasma as it is without Tidy.
- A welcome window on the first start.

**Look**
- Tidy's own icon: three slanted bars on a green tile, for the menu, Discover and the windows,
  and a one-colour version in the system tray that follows the theme, with its own look when
  the icons are hidden.
- The settings window fits a low screen: the Panel tab scrolls where it has no room. The
  list of programs of a drawer fills its box, without an empty strip or half a row.

**Under the hood**
- Lighter: about 24 MB of memory, no processor time at rest.
- Tidy checks what it reaches into in Plasma and KWin and says once what does not work in a new
  Plasma version; `plasma-tidy --check` lists it all.
- `plasma-tidy --report` for bug reports, without personal data.
- A package for Fedora, on COPR (`wispware/plasma-tidy`), and 102 tests.
- A page for software centres such as Discover (AppStream), with screenshots; the README
  shows Tidy at work.

## 0.2.0 — 2026-10-01

- Panel drawers: an arrow in the panel that tucks the programs and widgets you choose away.

## 0.1.0 — 2026-09-30

- First version: hides the desktop icons when you are not using them and brings them back on
  mouse movement, a click on the desktop, a screen corner or a shortcut; organises the system
  tray.
