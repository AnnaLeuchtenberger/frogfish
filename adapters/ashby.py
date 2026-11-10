from models import Job


def normalize_ashby_job(raw_job: dict, company: str) -> Job:
    return Job(
        company=company,
        title=raw_job["title"],
        location=raw_job.get("location") or "",
        url=raw_job["jobUrl"],
        description=raw_job.get("descriptionPlain") or "",
    )
