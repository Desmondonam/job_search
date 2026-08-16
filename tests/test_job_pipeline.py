from job_search_app.orchestrator import JobApplicationOrchestrator, JobRecord
from job_search_app.scoring import score_job_fit


def test_score_job_fit_matches_candidate_profile():
    profile = {
        "name": "Alex Smith",
        "skills": ["python", "fastapi", "sql", "postgresql", "aws"],
        "experience_years": 5,
        "remote_ok": True,
    }

    job = {
        "title": "Senior Python Engineer",
        "company": "Acme Labs",
        "description": (
            "We are hiring a senior python engineer with fastapi, sql, and aws experience. "
            "Remote-first role for a backend engineer."
        ),
        "location": "Remote",
        "remote": True,
    }

    score = score_job_fit(profile, job)

    assert score >= 80
    assert score <= 100


def test_orchestrator_tracks_job_statuses():
    orchestrator = JobApplicationOrchestrator(profile={
        "name": "Alex Smith",
        "skills": ["python", "fastapi", "sql", "postgresql", "aws"],
        "experience_years": 5,
        "remote_ok": True,
    })

    job = JobRecord(
        id="job-1",
        title="Backend Engineer",
        company="Northwind",
        description="Build APIs with Python, FastAPI, and SQL.",
        location="Remote",
        remote=True,
        salary="$140k",
    )

    record = orchestrator.add_job(job)
    assert record.status == "discovered"

    orchestrator.score_job(record.id)
    assert record.score >= 0
    assert record.status == "scored"

    orchestrator.generate_tailored_draft(record.id)
    assert "cover_letter" in record.drafts
    assert record.status == "ready_for_review"

    orchestrator.approve_application(record.id)
    assert record.status == "approved"
