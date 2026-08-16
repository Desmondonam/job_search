import re
from typing import Any


def _normalize(text: str | None) -> set[str]:
    if not text:
        return set()
    return {
        token.lower()
        for token in re.findall(r"[a-zA-Z0-9+#.]+", text)
        if len(token) > 2
    }


def score_job_fit(profile: dict[str, Any], job: dict[str, Any]) -> int:
    """Score a job fit using a weighted heuristic tailored to typical software-role signals."""
    profile_skills = {skill.lower() for skill in profile.get("skills", [])}
    title_tokens = _normalize(job.get("title", ""))
    job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('location', '')}"
    job_tokens = _normalize(job_text)

    overlap = profile_skills & job_tokens
    title_overlap = profile_skills & title_tokens

    skill_score = min(50, len(overlap) * 12)
    title_bonus = min(25, len(title_overlap) * 10)

    if "python" in profile_skills and "python" in title_tokens:
        title_bonus += 10

    experience_years = int(profile.get("experience_years", 0) or 0)
    exp_bonus = min(20, max(0, experience_years - 2) * 4)

    remote_match = 10 if profile.get("remote_ok") and (job.get("remote") or "remote" in str(job.get("location", "")).lower()) else 0

    total = min(100, skill_score + title_bonus + exp_bonus + remote_match)
    return int(total)
