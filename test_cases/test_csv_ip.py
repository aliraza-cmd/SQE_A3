"""Data-driven unit tests for IP validation consuming external CSV.

Course: SE-3002 Software Quality Engineering
Assignment 3 - Task 3 & Task 4
"""

import csv
from pathlib import Path
import pytest
import validators

CSV_FILE = Path(__file__).resolve().parent.parent / "test_data" / "ip_data.csv"


def load_ip_test_data():
    """Load test cases dynamically from ip_data.csv."""
    with open(CSV_FILE, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


IP_RECORDS = load_ip_test_data()


@pytest.mark.ip
@pytest.mark.csv
@pytest.mark.regression
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "row",
    IP_RECORDS,
    ids=[f"{r['test_id']}_{r['function']}_{r.get('technique', 'CSV')}" for r in IP_RECORDS],
)
def test_ip_from_csv(row):
    """Execute data-driven IP address validation loaded from external CSV resource.

    Dispatches to validators.ipv4 or validators.ipv6 dynamically based on CSV record.
    """
    func_name = row["function"].strip()
    test_input = row["input"].strip()
    expected = row["expected"].strip().upper() == "TRUE"

    validator_fn = getattr(validators, func_name, None)
    assert validator_fn is not None, f"Validator function '{func_name}' not found in validators module."

    actual = bool(validator_fn(test_input))
    assert actual is expected, (
        f"Test case {row['test_id']} failed for function {func_name} with input '{test_input}'. "
        f"Expected: {expected}, Actual: {actual} (Technique: {row.get('technique', 'N/A')})"
    )