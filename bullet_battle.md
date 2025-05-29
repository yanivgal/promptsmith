# Bullet Battle

This is a simple Streamlit app built to compare two versions of bulletized text based on original input text. It allows easy navigation, visualization, and selection of the better version.

## Files

- `bullet_battle.py`: The Streamlit app.
- `bulletized_results.csv`: The dataset used in the app.

## Dataset (`bulletized_results.csv`)

The CSV contains:
- `text`: The original input text.
- `v1 bullets`: The first version of bulletized text.
- `v2 bullets`: The second version of bulletized text.
- `who_is_better` (optional): Stores the user's choice (`v1 is better`, `v2 is better`, or `both are bad`).
- `reason` (optional): A free-text explanation for the choice.

## What the App Does

- Loads the CSV and displays one example at a time.
- Shows the full original text and both bulletized versions side by side.
- Lets the user choose which version is better.
- Optionally lets the user write a reason for their choice.
- Saves the results (choice and reason) back into the CSV.

## How to Run

1. Make sure you have [Python](https://www.python.org/) installed.
2. Install Streamlit (if not already installed):
   ```bash
   pip install streamlit
   ```
3. Make sure both `bullet_battle.py` and `bulletized_results.csv` are in the same folder.
4. From that folder, run:
   ```bash
   streamlit run bullet_battle.py
   ```