import csv
from pathlib import Path
import pytest
import validators

CSV_FILE = Path(__file__).resolve().parent.parent / "test_data" / "email_data.csv"


def load_email_data():
    with open(CSV_FILE, mode="r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


EMAIL_RECORDS = load_email_data()


@pytest.mark.email
@pytest.mark.csv
@pytest.mark.order(3)
@pytest.mark.parametrize(
    "row",
    EMAIL_RECORDS,
    ids=[f"{r.get('test_id', 'E')}_{r['email']}" for r in EMAIL_RECORDS],
)
def test_email_from_csv(row):
    email = row["email"].strip()
    expected = row["expected"].strip().lower() == "valid"
    assert bool(validators.email(email)) is expected
