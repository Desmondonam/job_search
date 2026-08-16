# Local Job Search Pipeline

A local-first human-in-the-loop job application assistant for discovering roles, scoring them against your resume, drafting tailored materials, and approving final submissions before sending them.

## Included in this MVP

- Job tracking with status transitions
- Local fit scoring against a candidate profile
- Tailored cover-letter and resume-summary drafts
- Streamlit dashboard for review and approval
- Regression tests covering the core scoring flow

## Run locally

1. Create and activate a virtual environment if needed.
2. Install dependencies:
   python3 -m pip install -e '.[dev]'
3. Launch the dashboard:
   streamlit run src/job_search_app/dashboard.py

## Project structure

- src/job_search_app/orchestrator.py: job lifecycle and approval logic
- src/job_search_app/scoring.py: fit-based scoring heuristic
- src/job_search_app/dashboard.py: review UI for jobs and drafts
- tests/test_job_pipeline.py: regression tests for fit scoring and status flow

## Safety notes

This is intentionally a human-in-the-loop workflow. It helps automate discovery, tailoring, and form preparation, but final decisions still remain with the user before submitting an application anywhere.
