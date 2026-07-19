# CentralReach Automation — Release 0.2.0

This release adds the first working feature: a persistent Playwright browser manager.

## What it does

- Opens CentralReach and Outlook in a Playwright-controlled browser.
- Uses a persistent project browser profile so logins can survive between runs.
- Captures startup screenshots.
- Creates daily logs.
- Deletes the previous debug package before making a new one.
- Captures a failure screenshot, page HTML, traceback, and browser state when startup fails.

## First-time setup on macOS

1. Extract the ZIP.
2. Copy the new files into your existing Git project, replacing files when prompted.
3. In Terminal, enter the project folder.
4. Run:

   chmod +x setup.command start.command
   ./setup.command

5. Start the app:

   ./start.command

You can also run it manually:

   source .venv/bin/activate
   python3 main.py

## Test

Choose `1) Test browser and login persistence`.

Expected result:

- A browser opens.
- CentralReach opens in one tab.
- Outlook opens in another tab.
- You can log in manually.
- Screenshots appear under `debug/current/screenshots/`.
- A log appears under `logs/`.

After logging in, press Enter in Terminal so the browser closes cleanly. Run the test again. The project browser profile should remember the sessions.

## Important

Do not store real payment spreadsheets in GitHub. The `.gitignore` excludes Excel files in `input/`, browser profile data, logs, debug files, invoices, and recovery state.
