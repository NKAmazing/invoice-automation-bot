# Automation Bot

Minimal bot to load invoice rows from a CSV into a web or desktop form using **PyAutoGUI**.

## Flow

1. Read the CSV
2. Loop over each row
3. Wait until the UI is ready
4. Fill the fields
5. Submit
6. Log the result

## Layout

```text
automation-bot/
├── main.py
├── demo.html
├── data/
│   └── invoices.csv
├── utils/
│   ├── screen.py
│   └── actions.py
├── config.py
└── README.md
```

## Execution

From the **repository root**, create and activate a virtual environment, install dependencies, then run the bot **from this folder** (`automation-bot/`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
cd automation-bot
python main.py
```

Before the countdown ends, focus the target form (for the local demo, open `demo.html` in a browser and click the **Name** field). See the root [README.md](../README.md) for full setup, macOS notes, and future improvements.
