# Release 0.2 Test Plan

## Installation

- `./setup.command` completes without errors.
- `./start.command` opens the menu.

## Browser test

- Choose menu option 1.
- Browser opens.
- CentralReach tab opens.
- Outlook tab opens.
- Log in manually where needed.
- Confirm `debug/current/screenshots/centralreach_ready.png` exists.
- Confirm `debug/current/screenshots/outlook_ready.png` exists.
- Confirm `debug/current/browser_state.json` exists.
- Confirm a daily file exists in `logs/`.

## Persistence test

- Close the browser by pressing Enter in Terminal.
- Run browser test again.
- Confirm the previous login is retained where the site permits it.

## Debug replacement test

- Note files inside `debug/current/`.
- Run the browser test again.
- Confirm the old debug package was replaced rather than accumulated.
