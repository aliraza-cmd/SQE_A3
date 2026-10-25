# Assignment 3: Build Unit Test Automation Solution

**Course:** SE-3002 Software Quality Engineering  
**Target Open-Source Application:** [`validators`](https://github.com/python-validators/validators) (Python)  
**Submission Repository:** [https://github.com/aliraza-cmd/SQE_A3.git](https://github.com/aliraza-cmd/SQE_A3.git)  

---

## 1. Group Member Allocation & Task Distribution

| Member Name | Role | Assigned Modules & Tasks |
|:---|:---|:---|
| **Ali Raza** | Lead QA Engineer & Automation Architect | **Module 1** (`validators.email`), **Task 4** (Test Suite Configuration, Parallel Execution, Ordering, Markers) |
| **Ali Asif** | Test Automation Engineer | **Module 2** (`validators.ip_address` - IPv4 & IPv6), **Task 3** (External CSV Data-Driven Testing for Email & IP, Excel Test Specification) |

---

## 2. Deliverables & Required Reports Format Overview

According to the assignment specification and evaluation rubric, all deliverables and reports are structured in the following formats:

| Deliverable | Purpose | Required Format | Repository Location |
|:---|:---|:---:|:---|
| **Test Cases in Excel Sheet** *(Task 3)* | Full test matrix with Test IDs, inputs, expected outputs, techniques, and execution status. | **Excel Spreadsheet (`.xlsx`)** | [`documents/Test_Cases_Specification.xlsx`](documents/Test_Cases_Specification.xlsx) |
| **External CSV Test Data** *(Task 3)* | External datasets consumed dynamically by data-driven test cases. | **Comma-Separated Values (`.csv`)** | [`test_data/email_data.csv`](test_data/email_data.csv)<br>[`test_data/ip_data.csv`](test_data/ip_data.csv) |
| **ECP & BVA Design Notes** *(Task 2)* | Comprehensive testing design notes documenting Equivalence Classes, Boundary Values, and input partitions. | **Markdown (`.md`)** *(can also be printed to PDF)* | [`documents/ECP_BVA_Test_Design_Notes.md`](documents/ECP_BVA_Test_Design_Notes.md) |
| **Summary Report** *(Rubric Item)* | End-to-end report summarizing testing achievements, test metrics, and rubric compliance before due date. | **Markdown (`.md`) / PDF** | [`documents/Summary_Report.md`](documents/Summary_Report.md) |
| **Execution & Setup Guide** *(Task 4)* | Instructions for setting up environment, parallel execution, test suites, and markers. | **Markdown (`.md`)** | [`documents/Test_Execution_Guide.md`](documents/Test_Execution_Guide.md) |
| **Setup Video Demonstration** *(Task 1)* | Video demonstrating local environment setup and test execution. | **Video (`.mp4`) / Link** | [`documents/setup_demo.mp4`](documents/) *(or Google Drive link in docs)* |

---

## 3. Tasks Implementation Summary

### Task 1: Environment Setup
- **Project Selected:** `validators` (v0.36.0) - A Python data validation library for human readability.
- **Local Development Environment:**
  - Python virtual environment: `.venv/`
  - Core dependencies: `pytest`, `pytest-xdist` (parallelism), `pytest-order` (ordering), `openpyxl` (Excel processing).
  - Configuration file: `pytest.ini` with `pythonpath = src`.

---

### Task 2: Automated Unit Test Cases

We identified and developed comprehensive automated unit test cases applying **Equivalence Class Partitioning (ECP)** and **Boundary Value Analysis (BVA)**:

1. **Module 1: Email Validation (`validators.email`)**
   - **Test File:** [`test_cases/test_email_validation.py`](test_cases/test_email_validation.py)
   - **ECP Partitioning:** Valid standard emails, alphanumeric, subdomains, plus-tagging (`+`), numeric usernames, hyphens; Invalid addresses missing `@`, missing local-part, missing domain, consecutive dots, whitespace, and duplicate `@`.
   - **BVA Boundaries:** Local-part length maximum boundary of 64 characters (RFC 5321), local-part length 65 characters (upper bound + 1, invalid), 1-character local-part (min valid), 0-character local part (invalid), empty string.
   - **Total Tests:** 19 test cases (All passing).

2. **Module 2: IP Address Validation (`validators.ip_address`)**
   - **Test File:** [`test_cases/test_ip_validation.py`](test_cases/test_ip_validation.py)
   - **IPv4 ECP & BVA:** Network Classes A, B, C; loopback (`127.0.0.1`); public DNS; octet boundaries `0` and `255`; off-boundary `256` and negative octet `-1`; structural 3-octet and 5-octet boundaries; non-numeric inputs.
   - **IPv6 ECP & BVA:** Compressed loopback (`::1`), uncompressed 8-hextets, link-local (`fe80::1`), IPv4-mapped IPv6; boundary hextet `0xFFFF`, hextet overflow `0x10000`, 9-hextet boundary violation, non-hex character (`g`), double compression violation.
   - **Total Tests:** 23 test cases (All passing).

---

### Task 3: Excel Sheet & External CSV Data-Driven Testing

1. **Excel Test Specification:**
   - Saved as [`documents/Test_Cases_Specification.xlsx`](documents/Test_Cases_Specification.xlsx).
   - Formatted into distinct sheets: `Email Validation`, `IP Address Validation`, and `CSV External Data Tests` containing Test IDs, module names, inputs, expected outputs, techniques, and execution status (`PASS`).

2. **External CSV Data Consumption:**
   - [`test_data/email_data.csv`](test_data/email_data.csv): Consumed by [`test_cases/test_csv_email.py`](test_cases/test_csv_email.py) (7 data-driven tests).
   - [`test_data/ip_data.csv`](test_data/ip_data.csv): Consumed by [`test_cases/test_csv_ip.py`](test_cases/test_csv_ip.py) using dynamic dispatch for `validators.ipv4` and `validators.ipv6` (6 data-driven tests).

---

### Task 4: Configuration, Parallelism, Suites & Ordering

- **Configuration:** [`pytest.ini`](pytest.ini) defines `pythonpath = src`, test discovery paths, and markers.
- **Parallel Execution:** Configured using `pytest-xdist` (`pytest -n auto`).
- **Test Suites / Groups (Markers):**
  - `email`: All email validation tests.
  - `ip`: All IPv4 & IPv6 validation tests.
  - `csv`: All data-driven external CSV tests.
  - `ecp`: Equivalence Class Partitioning tests.
  - `bva`: Boundary Value Analysis tests.
- **Execution Ordering (`pytest-order`):**
  - Order 1: `test_cases/test_email_validation.py`
  - Order 2: `test_cases/test_ip_validation.py`
  - Order 3: `test_cases/test_csv_email.py`
  - Order 4: `test_cases/test_csv_ip.py`

---

## 4. How to Run the Test Automation Solution

Make sure you are in the project root directory and the virtual environment is activated:

```powershell
# Activate virtual environment (if not already active)
.\.venv\Scripts\Activate.ps1
```

### 1. Run the Entire Test Suite (Default Order 1 -> 4)
```powershell
pytest -v
```

### 2. Run Test Cases in Parallel Across CPU Cores (Task 4)
```powershell
# Automatically detect CPU cores:
pytest -n auto

# Or specify worker processes explicitly:
pytest -n 4
```

### 3. Run Specific Test Suites (Task 4)
```powershell
pytest -m email       # Run only Email validation suite
pytest -m ip          # Run only IP address suite (IPv4 & IPv6)
pytest -m csv         # Run only external CSV data-driven suite
```

### 4. Run by Testing Technique (Task 2)
```powershell
pytest -m ecp         # Run all Equivalence Class Partitioning tests
pytest -m bva         # Run all Boundary Value Analysis tests
```

### 5. Run External CSV Data-Driven Tests Only (Task 3)
```powershell
pytest test_cases/test_csv_email.py -v
pytest test_cases/test_csv_ip.py -v
```

---

## 5. Test Execution Results

```
============================= test session starts =============================
platform win32 -- Python 3.14.8, pytest-9.1.1
plugins: order-1.5.0, xdist-3.8.0
collected 55 items

test_cases/test_email_validation.py ...................                  [ 34%]
test_cases/test_ip_validation.py .......................                 [ 76%]
test_cases/test_csv_email.py .......                                     [ 89%]
test_cases/test_csv_ip.py ......                                         [100%]

============================= 55 passed in 0.23s ==============================
```

- **Total Test Cases:** 55
- **Passed:** 55 (100%)
- **Failed:** 0 (0%)
- **Errors / Skipped:** 0

---

## 6. Repository Structure

```
validators/
├── documents/
│   ├── ECP_BVA_Test_Design_Notes.md        # Task 2 ECP and BVA design notes
│   ├── Test_Execution_Guide.md             # Task 4 execution instructions & guides
│   ├── Summary_Report.md                   # Rubric summary report
│   └── Test_Cases_Specification.xlsx       # Task 3 Excel test matrix
├── test_cases/
│   ├── test_email_validation.py            # Task 2: Module 1 Email tests (ECP & BVA)
│   ├── test_ip_validation.py               # Task 2: Module 2 IP tests (ECP & BVA)
│   ├── test_csv_email.py                   # Task 3: Email CSV data-driven tests
│   └── test_csv_ip.py                      # Task 3: IP CSV data-driven tests
├── test_data/
│   ├── email_data.csv                      # External CSV data for email validation
│   └── ip_data.csv                         # External CSV data for IP validation
├── src/validators/                         # Target application source code under test
├── pytest.ini                              # Pytest configuration, suites, and markers
└── README.md                               # Project documentation & evaluation guide
```
