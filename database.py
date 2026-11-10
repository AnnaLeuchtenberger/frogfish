import hashlib
import json
import sqlite3
from pathlib import Path

from models import Job

DB_PATH = Path(__file__).parent / "frogfish.db"


def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                source TEXT NOT NULL,
                board_slug TEXT NOT NULL,
                source_job_id TEXT NOT NULL,

                company TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT NOT NULL,

                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,

                content_hash TEXT NOT NULL,

                filter_status TEXT,
                filter_reason TEXT,

                PRIMARY KEY (
                    source,
                    board_slug,
                    source_job_id
                )
            )
        """)


def calculate_content_hash(job: Job) -> str:
    content = {
        "company": job.company,
        "title": job.title,
        "location": job.location,
        "url": job.url,
        "description": job.description,
    }

    serialized = json.dumps(content, sort_keys=True)

    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


from datetime import UTC, datetime


def save_job(
    job: Job,
    source: str,
    board_slug: str,
    source_job_id: str,
) -> str:

    now = datetime.now(UTC).isoformat()
    content_hash = calculate_content_hash(job)

    with sqlite3.connect(DB_PATH) as connection:
        existing = connection.execute(
            """
            SELECT content_hash
            FROM jobs
            WHERE source = ?
              AND board_slug = ?
              AND source_job_id = ?
            """,
            (source, board_slug, source_job_id),
        ).fetchone()

        if existing is None:
            connection.execute(
                """
                INSERT INTO jobs (
                    source, board_slug, source_job_id,
                    company, title, location, url, description,
                    first_seen, last_seen, content_hash
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source,
                    board_slug,
                    source_job_id,
                    job.company,
                    job.title,
                    job.location,
                    job.url,
                    job.description,
                    now,
                    now,
                    content_hash,
                ),
            )
            return "NEW"

        if existing[0] == content_hash:
            connection.execute(
                """
                UPDATE jobs
                SET last_seen = ?
                WHERE source = ?
                  AND board_slug = ?
                  AND source_job_id = ?
                """,
                (now, source, board_slug, source_job_id),
            )
            return "UNCHANGED"

        connection.execute(
            """
            UPDATE jobs
            SET company = ?,
                title = ?,
                location = ?,
                url = ?,
                description = ?,
                last_seen = ?,
                content_hash = ?,
                filter_status = NULL,
                filter_reason = NULL
            WHERE source = ?
              AND board_slug = ?
              AND source_job_id = ?
            """,
            (
                job.company,
                job.title,
                job.location,
                job.url,
                job.description,
                now,
                content_hash,
                source,
                board_slug,
                source_job_id,
            ),
        )

        return "CHANGED"


def save_filter_result(
    source: str,
    board_slug: str,
    source_job_id: str,
    status: str,
    reason: str,
) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            UPDATE jobs
            SET filter_status = ?,
                filter_reason = ?
            WHERE source = ?
              AND board_slug = ?
              AND source_job_id = ?
            """,
            (status, reason, source, board_slug, source_job_id),
        )


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at {DB_PATH}")
