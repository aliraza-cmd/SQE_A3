"""Data-driven unit tests for Email validation consuming external CSV.

Course: SE-3002 Software Quality Engineering
Assignment 3 - Task 3 & Task 4
"""

import csv
from pathlib import Path
import pytest
import validators

CSV_FILE = Path(__file__).resolve().parent.parent / "test_data" / "email_data.csv"


def load_email_test_data():
    """Load test cases dynamically from email_data.csv."""
    with open(CSV_FILE, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


EMAIL_RECORDS = load_email_test_data()


@pytest.mark.email
@pytest.mark.csv
@pytest.mark.regression
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "row",
    EMAIL_RECORDS,
    ids=[f"{r.get('test_id', 'E')}_{r.get('technique', 'CSV')}_{r['email']}" for r in EMAIL_RECORDS],
)
def test_email_from_csv(row):
    """Execute data-driven email validation loaded from external CSV resource."""
    email_input = row["email"].strip()
    expected_status = row["expected"].strip().lower()
    expected_valid = expected_status in ("valid", "true", "1")

    actual_valid = bool(validators.email(email_input))

    assert actual_valid is expected_valid, (
        f"Test case {row.get('test_id', 'N/A')} failed for email '{email_input}'. "
        f"Expected: {expected_status} ({expected_valid}), Actual: {actual_valid} "
        f"(Technique: {row.get('technique', 'N/A')})"
    )