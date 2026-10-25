import csv
from pathlib import Path
import pytest
import validators

CSV_FILE = Path(__file__).resolve().parent.parent / "test_data" / "ip_data.csv"


def load_ip_data():
    with open(CSV_FILE, mode="r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


IP_RECORDS = load_ip_data()


@pytest.mark.ip
@pytest.mark.csv
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "row",
    IP_RECORDS,
    ids=[f"{r['test_id']}_{r['function']}_{r['input']}" for r in IP_RECORDS],
)
def test_ip_from_csv(row):
    # Dynamically pick validators.ipv4 or validators.ipv6 from the CSV row
    func = getattr(validators, row["function"].strip())
    expected = row["expected"].strip().upper() == "TRUE"
    assert bool(func(row["input"].strip())) is expected