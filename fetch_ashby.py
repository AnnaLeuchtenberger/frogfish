import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from adapters.ashby import normalize_ashby_job
from database import initialize_database, save_filter_result, save_job
from filters import filter_location, filter_title

ASHBY_BOARDS = {
    "OpenAI": "openai",
    "Artian": "artian",
    "Exa": "exa",
    "2501": "2501",
    "Whippy": "whippy",
    "CertifyOS": "certifyos",
    "Modal": "modal",
    "Endex": "endex",
    "Endra": "endra",
    "Globo": "globo",
}

initialize_database()

save_counts = {
    "NEW": 0,
    "CHANGED": 0,
    "UNCHANGED": 0,
}

all_jobs = []

for company, slug in ASHBY_BOARDS.items():
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"

    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    try:
        with urlopen(request, timeout=15) as response:
            data = json.load(response)

        jobs = []

        for raw_job in data["jobs"]:
            job = normalize_ashby_job(raw_job, company)

            result = save_job(
                job,
                source="ashby",
                board_slug=slug,
                source_job_id=raw_job["id"],
            )

            save_counts[result] += 1
            location_passed, location_reason = filter_location(job.location)
            title_passed, title_reason = filter_title(job.title)

            if location_passed and title_passed:
                filter_status = "PASS"
                filter_reason = "Passed location and title filters"
            else:
                filter_status = "REJECT"
                reasons = []

                if not location_passed:
                    reasons.append(location_reason)

                if not title_passed:
                    reasons.append(title_reason)

                filter_reason = "; ".join(reasons)

            save_filter_result(
                source="ashby",
                board_slug=slug,
                source_job_id=raw_job["id"],
                status=filter_status,
                reason=filter_reason,
            )
            jobs.append(job)

        all_jobs.extend(jobs)
        print(f"{company}: fetched {len(jobs)} jobs")

    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as error:
        print(f"{company}: FETCH FAILED ({error})")


print(f"\nTotal jobs retrieved: {len(all_jobs)}")
print("\nDatabase results:")
print(f"  New: {save_counts['NEW']}")
print(f"  Changed: {save_counts['CHANGED']}")
print(f"  Unchanged: {save_counts['UNCHANGED']}")
print()


location_matches = 0
title_matches = 0
final_matches = []

for job in all_jobs:
    location_passed, _ = filter_location(job.location)
    title_passed, _ = filter_title(job.title)

    if location_passed:
        location_matches += 1

    if title_passed:
        title_matches += 1

    if location_passed and title_passed:
        final_matches.append(job)

print(f"Passed location filter: {location_matches}")
print(f"Passed title filter: {title_matches}")
print(f"Passed both filters: {len(final_matches)}\n")

# for job in final_matches:
#     print(f"MATCH: {job.title}")
#     print(f"  Company: {job.company}")
#     print(f"  Location: {job.location}")
#     print(f"  URL: {job.url}")
#     print()
