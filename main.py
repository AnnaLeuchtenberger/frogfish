from filters import filter_location
from models import Job

jobs = [
    Job(
        company="Acme",
        title="Solutions Engineer",
        location="New York, NY",
        url="https://example.com/jobs/1",
        description="Provide technical solutions for coyotes.",
    ),
    Job(
        company="West Coast Tech",
        title="Implementation Engineer",
        location="San Francisco, CA",
        url="https://example.com/jobs/2",
        description="Implement enterprise software for large customers.",
    ),
    Job(
        company="Revolutionary AI",
        title="Customer Engineer",
        location="Remote - US",
        url="https://example.com/jobs/3",
        description="Work directly with customers deploying AI systems.",
    ),
    Job(
        company="Very New Startup",
        title="Solutions Architect",
        location="New York, NY (Hybrid)",
        url="https://example.com/jobs/4",
        description="Design technical solutions for enterprise customers.",
    ),
]
for job in jobs:
    passed, reason = filter_location(job.location)

    print(f"{job.title} @ {job.company}")
    print(f"  Location: {job.location}")
    print(f"  Result: {'PASS' if passed else 'REJECT'} — {reason}")
