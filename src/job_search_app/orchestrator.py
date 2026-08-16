from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .scoring import score_job_fit


@dataclass
class JobRecord:
    id: str
    title: str
    company: str
    description: str
    location: str = ""
    remote: bool = False
    salary: str = ""
    score: int = 0
    status: str = "discovered"
    drafts: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "location": self.location,
            "remote": self.remote,
            "salary": self.salary,
            "score": self.score,
            "status": self.status,
            "drafts": self.drafts,
        }


class JobApplicationOrchestrator:
    def __init__(self, profile: dict[str, Any]):
        self.profile = profile
        self.jobs: dict[str, JobRecord] = {}

    def add_job(self, job: JobRecord) -> JobRecord:
        self.jobs[job.id] = job
        return self.jobs[job.id]

    def score_job(self, job_id: str) -> JobRecord:
        job = self.jobs[job_id]
        job.score = score_job_fit(self.profile, {
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "remote": job.remote,
        })
        job.status = "scored"
        return job

    def generate_tailored_draft(self, job_id: str) -> JobRecord:
        job = self.jobs[job_id]
        job.drafts["cover_letter"] = (
            f"Dear Hiring Team,\n\nI am excited to apply for the {job.title} role at {job.company}. "
            f"My background in {', '.join(self.profile.get('skills', [])[:4])} and my experience working with "
            "modern product teams make me a strong fit for this opportunity.\n\n"
            "I would welcome the chance to discuss how I can contribute to your team and help deliver strong results.\n\n"
            "Sincerely,\n"
            f"{self.profile.get('name', 'Applicant')}"
        )
        job.drafts["resume_summary"] = (
            f"Focused professional with experience in {', '.join(self.profile.get('skills', [])[:4])} and a track "
            "record of building reliable software products."
        )
        job.status = "ready_for_review"
        return job

    def approve_application(self, job_id: str) -> JobRecord:
        job = self.jobs[job_id]
        job.status = "approved"
        return job

    def reject_application(self, job_id: str) -> JobRecord:
        job = self.jobs[job_id]
        job.status = "rejected"
        return job
