from __future__ import annotations

from typing import Any

import streamlit as st

try:
    from .orchestrator import JobApplicationOrchestrator, JobRecord
except ImportError:  # pragma: no cover - Streamlit sometimes runs the file as a standalone script.
    from job_search_app.orchestrator import JobApplicationOrchestrator, JobRecord


st.set_page_config(page_title="Local Job Search Dashboard", layout="wide")


def render_dashboard() -> None:
    st.title("Local Job Search Dashboard")
    st.caption("Human-in-the-loop automation for job discovery, scoring, and review")

    profile = {
        "name": "Alex Smith",
        "skills": ["python", "fastapi", "sql", "postgresql", "aws"],
        "experience_years": 5,
        "remote_ok": True,
    }

    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = JobApplicationOrchestrator(profile=profile)

    orchestrator: JobApplicationOrchestrator = st.session_state.orchestrator

    with st.sidebar:
        st.subheader("Add sample role")
        job_title = st.text_input("Title", "Senior Python Engineer")
        company = st.text_input("Company", "Acme Labs")
        location = st.text_input("Location", "Remote")
        description = st.text_area(
            "Description",
            "We are hiring a senior python engineer with fastapi, sql, and aws experience in a remote-first environment.",
        )
        if st.button("Add job"):
            job = JobRecord(
                id=f"job-{len(orchestrator.jobs) + 1}",
                title=job_title,
                company=company,
                description=description,
                location=location,
                remote=location.lower().startswith("remote") or "remote" in location.lower(),
                salary="$145k",
            )
            orchestrator.add_job(job)
            orchestrator.score_job(job.id)
            orchestrator.generate_tailored_draft(job.id)
            st.success(f"Added {job.title} at {job.company}")

    if not orchestrator.jobs:
        st.info("No jobs discovered yet. Add a role to review the local pipeline.")
        return

    for job in orchestrator.jobs.values():
        with st.container(border=True):
            st.subheader(f"{job.company} — {job.title}")
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(job.description)
            col2.metric("Fit score", f"{job.score}/100")
            col3.write(f"Status: {job.status}")

            if job.drafts:
                st.markdown("### Tailored draft")
                st.code(job.drafts["cover_letter"], language="text")

            action_col1, action_col2 = st.columns(2)
            if action_col1.button("Approve", key=f"approve-{job.id}"):
                orchestrator.approve_application(job.id)
                st.rerun()
            if action_col2.button("Reject", key=f"reject-{job.id}"):
                orchestrator.reject_application(job.id)
                st.rerun()


if __name__ == "__main__":
    render_dashboard()
