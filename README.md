# Invoice Automation Bot

A minimal Python automation that reads invoice rows from a CSV file and types them into whatever application is currently focused (typically a web form or a desktop app), using **PyAutoGUI** for keyboard simulation and **pandas** for data loading.

## Goals and intent

The bot is meant for **repetitive data entry** where there is no API, or integrating one would be disproportionate. You maintain a spreadsheet-like source of truth (`invoices.csv`), run the script, focus the target UI, and the tool walks each row: type values, tab between fields, submit, and log the outcome.

**What it is not:** a robust integration layer. It does not parse HTML, drive a specific browser API, or guarantee field mapping beyond the tab order you assume in the target form.

---

## How it works (technical overview)

1. **`main.py`** loads `config.py` constants, reads the CSV with **pandas**, and validates that required columns exist: `name`, `amount`, `description`.
2. After a **prepare delay** (`PREPARE_DELAY_SECONDS`), it iterates each row.
3. For each row, **`utils/screen.py`** exposes `wait_for_ui_ready()`: today this is a short sleep to let the UI settle; you can extend it with image-based checks or other signals.
4. **`utils/actions.py`** calls `submit_invoice_form(...)`, which uses **PyAutoGUI** to:
   - `write(name)` → `press("tab")` → `write(amount)` → `press("tab")` → `write(description)` → `press("enter")`.
5. Success and errors are logged with Python **`logging`**. A **row delay** (`ROW_DELAY_SECONDS`) runs between rows to avoid hammering the UI.

**Critical assumption:** the focused window must have three fields in **exact tab order**: name → amount → description, and **Enter** must submit (or move to the next step you expect). If your real system differs, adjust `utils/actions.py` or the target layout.

---

## Project layout

```text
invoice-automation-bot/
├── automation-bot/
│   ├── main.py              # Entry point: CSV loop, logging, orchestration
│   ├── config.py          # Paths and timing knobs
│   ├── demo.html          # Static demo form for local testing (no server required)
│   ├── data/
│   │   └── invoices.csv   # Sample input data
│   ├── utils/
│   │   ├── screen.py      # UI readiness hook (sleep; extend as needed)
│   │   └── actions.py     # PyAutoGUI form fill + submit
│   └── README.md          # Optional local notes (Spanish in repo copy)
├── requirements.txt       # pandas, pyautogui
├── .gitignore
├── LICENSE
└── README.md                # This file
```

---

## Stack

| Piece        | Role |
| ------------ | ---- |
| **pandas**   | Read and validate CSV rows |
| **PyAutoGUI**| Simulate keyboard input to the focused application |
| **time**     | Delays between preparation, UI readiness, and rows |
| **logging**  | Structured console output per row |

---

## CSV format

The CSV must include these headers (order of columns does not matter to pandas, but the names must match):

```csv
name,amount,description
Juan Perez,1000,Servicio A
Maria Lopez,2500,Servicio B
```

---

## Setup and run

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd automation-bot
python main.py
```

Before the prepare countdown finishes, **focus the first input** of your target form (in the demo, the **Name** field). Keep that window in the foreground so keystrokes go to the right place.

---

## Trying the bundled `demo.html`

`automation-bot/demo.html` is a **static** page (no live server required). It includes a three-field form and a small list that shows each simulated submit.

1. Open `demo.html` in your browser (double-click or **File → Open**).
2. Click the **Name** input so it has keyboard focus.
3. Run `python main.py` from `automation-bot/` with your venv active.
4. After each row, the demo resets the form and refocuses **Name**, which matches the bot’s loop for multiple CSV rows.

---

## Configuration (`automation-bot/config.py`)

| Setting | Purpose |
| -------- | -------- |
| `CSV_PATH` | Relative path to the CSV from the `automation-bot/` working directory |
| `PREPARE_DELAY_SECONDS` | Time to switch to the browser/app and focus the first field |
| `ROW_DELAY_SECONDS` | Pause between rows |
| `UI_READY_DELAY_SECONDS` | Short delay before typing each row (UI stability) |

---

## Platform notes (macOS)

- **Accessibility:** PyAutoGUI may need **System Settings → Privacy & Security → Accessibility** enabled for the terminal or IDE you use to run Python.
- **Failsafe:** PyAutoGUI can abort if the mouse is moved to a screen corner (default behavior); avoid accidental corner moves during a run.
- **Dependencies:** Installing `pyautogui` on macOS may pull **PyObjC**-related packages for screen APIs; warnings about yanked or legacy builds sometimes appear from PyPI; upgrading `pip` and installing `wheel` can reduce noise.

---

## Future improvements

- **Image or coordinate-based field targeting:** use `pyautogui.locateOnScreen` (or similar) so the bot does not depend on fragile tab order.
- **Per-environment profiles:** YAML/JSON configs for different forms (different tab counts, hotkeys, or click sequences).
- **Excel input:** support `.xlsx` via `openpyxl` or `pandas.read_excel` when spreadsheets are the source of truth.
- **Stronger UI readiness:** wait for a known pixel, window title, or accessibility element instead of a fixed sleep.
- **Dry-run mode:** log intended keystrokes without sending them, for rehearsal in sensitive systems.
- **Retry and idempotency:** detect error dialogs, retry N times, or skip and log rows to a dead-letter CSV.
- **Rate limiting and backoff:** adaptive delays if the UI lags under load.
- **Headless or API path:** when the target app exposes an API or browser automation (Playwright/Selenium), prefer that over global keyboard simulation for reliability and auditability.

---

## License

See [LICENSE](LICENSE).
