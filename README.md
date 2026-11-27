# TeamSpark Streamlit Prototype

## What this prototype demonstrates
- Overview dashboard
- Session-only student profile builder
- Explainable event-aware matching simulator
- Student Explorer with search and filters
- Gap-Filling Team Builder
- Deadline Rescue concept view
- Beginner-friendly discovery option

## Important demo note
All student names, profiles, event details, reliability signals, metrics and match scores are illustrative sample data. The matching engine is a transparent rule-based prototype, not a trained or externally validated AI model. The app does not send invitations, use a database, or collect real student data. No API key is required.

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract the ZIP file.
3. Open the extracted `teamspark_prototype` folder.
4. Click the folder address bar, type `cmd`, and press Enter.
5. Run:
   `py -m venv .venv`
6. Activate:
   `.venv\Scripts\activate`
7. Install dependencies:
   `pip install -r requirements.txt`
8. Start the app:
   `streamlit run app.py`
9. Open the local URL printed in the terminal (normally http://localhost:8501).

## Run on macOS / Linux
1. Open Terminal in this folder.
2. Create and activate a virtual environment:
   `python3 -m venv .venv`
   `source .venv/bin/activate`
3. Install:
   `pip install -r requirements.txt`
4. Start:
   `streamlit run app.py`

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository and upload `app.py` and `requirements.txt`.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Choose **Create app**, select the repository, branch and `app.py`.
4. Deploy. Copy the live URL only after the app reports that it is running.
5. Add that verified URL to the final PPT.

This prototype has no secrets or API keys. Do not add private student information to the sample data.
