# Test Execution & Automation Guide

**Course:** SE-3002 Software Quality Engineering  
**Assignment:** Assignment 3 – Build Unit Test Automation Solution  
**Framework:** Python 3 + `pytest` + `pytest-xdist` + `pytest-order`  

---

## 1. Environment Setup (Task 1)

1. **Activate Virtual Environment:**
   ```powershell
   # On Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install Required Packages:**
   ```powershell
   pip install pytest pytest-xdist pytest-order openpyxl
   ```

3. **Verify Configuration:**
   The `pytest.ini` configuration file automatically includes `src` in `pythonpath`:
   ```ini
   [pytest]
   testpaths = test_cases
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   pythonpath = src
   addopts = -v -ra
   ```

---

## 2. Running Test Cases (Task 4)

### 2.1 Parallel Execution (`pytest-xdist`)

To execute test cases in parallel across multiple CPU cores, use the `-n` flag:

```powershell
# Run across all available CPU cores automatically:
pytest -n auto

# Run across 4 parallel worker processes:
pytest -n 4
```

### 2.2 Running by Test Suite / Group (`pytest` Markers)

All tests are partitioned into logical suites using markers:

| Marker Name | Description | Command |
|:---|:---|:---|
| `email` | Runs all Email validation tests (code + CSV) | `pytest -m email` |
| `ip` | Runs all IPv4 and IPv6 validation tests (code + CSV) | `pytest -m ip` |
| `csv` | Runs all External Data-Driven CSV tests | `pytest -m csv` |
| `ecp` | Runs Equivalence Class Partitioning tests | `pytest -m ecp` |
| `bva` | Runs Boundary Value Analysis tests | `pytest -m bva` |
| `smoke` | Runs quick sanity smoke tests | `pytest -m smoke` |
| `regression`| Runs full regression suite | `pytest -m regression` |

### 2.3 Combining Suites and Conditions

```powershell
# Run ECP tests in parallel:
pytest -m ecp -n auto

# Run only IPv4/IPv6 BVA boundary tests:
pytest -m "ip and bva"

# Run all tests except CSV tests:
pytest -m "not csv"
```

### 2.4 Test Execution Ordering (`pytest-order`)

The execution order across test suites is strictly established using `@pytest.mark.order`:

1. **Order 1:** Email Validation Unit Tests (`test_cases/test_email_validation.py`)
2. **Order 2:** IP Address Validation Unit Tests (`test_cases/test_ip_validation.py`)
3. **Order 3:** Email CSV Data-Driven Tests (`test_cases/test_csv_email.py`)
4. **Order 4:** IP CSV Data-Driven Tests (`test_cases/test_csv_ip.py`)

To run the entire suite in this defined order:
```powershell
pytest -v
```

---

## 3. External CSV Data-Driven Testing (Task 3)

The project consumes test cases from external CSV files located in `test_data/`:

- `test_data/email_data.csv`: Supplies data for `test_cases/test_csv_email.py`.
- `test_data/ip_data.csv`: Supplies data for `test_cases/test_csv_ip.py`.

To run only the external CSV tests:
```powershell
pytest -m csv -v
```

---

## 4. Test Documentation & Excel Artifacts (Task 3)

The complete test specification matrix is available as an Excel spreadsheet:
- **Location:** `documents/Test_Cases_Specification.xlsx`
- **Contents:**
  - Tab 1: `Email Validation` (19 test cases)
  - Tab 2: `IP Address Validation` (23 test cases)
  - Tab 3: `CSV External Data Tests` (13 test cases)
