# Assignment 3 Summary Report: Unit Test Automation Solution

**Course:** SE-3002 Software Quality Engineering  
**Submission Date:** October 2026  
**Selected Open-Source Application:** `validators` (Python)  
**Git Repository Status:** Complete & Verified  

---

## 1. Executive Summary

This project delivers a comprehensive, automated unit test automation solution for the open-source Python library **`validators`**. All requirements specified across Tasks 1, 2, 3, and 4 have been implemented, verified, and documented with 100% test pass rate.

---

## 2. Deliverables Checklist & Task Fulfillment

| Requirement | Description | Status | Verification Artifact |
|:---|:---|:---:|:---|
| **Task 1: Environment Setup** | Set up local virtual environment for open-source Python project. | Complete | `.venv/`, `pytest.ini`, `pyproject.toml` |
| **Task 2: 3 Application Modules** | Identified 3 application modules: `email`, `ip_address` (`ipv4`/`ipv6`), and `url`. | Complete | `test_cases/test_email_validation.py`<br>`test_cases/test_ip_validation.py`<br>`test_cases/test_url_validation.py` |
| **Task 2: ECP & BVA Notes** | Comprehensive test design notes applying Equivalence Class Partitioning and Boundary Value Analysis. | Complete | `documents/ECP_BVA_Test_Design_Notes.md` |
| **Task 2: Unit Test Cases** | Created 5–10 automated test cases per function/class/module. | Complete | 60 comprehensive unit tests implemented across 3 modules. |
| **Task 3: Excel Specification** | Test cases documented in an Excel sheet. | Complete | `documents/Test_Cases_Specification.xlsx` |
| **Task 3: External CSV Data** | At least 4 test cases consumed from external CSV resources. | Complete | `test_data/email_data.csv`<br>`test_data/ip_data.csv`<br>`test_cases/test_csv_email.py`<br>`test_cases/test_csv_ip.py` |
| **Task 4: Parallel Execution** | Configured multi-core parallel test execution using `pytest-xdist`. | Complete | Verified via `pytest -n auto` / `pytest -n 4` |
| **Task 4: Test Suites & Groups** | Divided tests into suites using markers (`email`, `ip`, `url`, `csv`, `ecp`, `bva`). | Complete | `pytest.ini` & marker decorators |
| **Task 4: Test Parameterization** | Parameterized test cases with descriptive IDs for data-driven testing. | Complete | `@pytest.mark.parametrize` applied in all test files |
| **Task 4: Test Execution Order** | Configured execution ordering across suites via `pytest-order`. | Complete | `@pytest.mark.order(1..5)` in place |

---

## 3. Test Execution Metrics

- **Total Test Cases Executed:** 73
- **Passed:** 73 (100%)
- **Failed:** 0 (0%)
- **Errors / Skipped:** 0
- **Execution Time (Sequential):** ~0.41 seconds
- **Execution Time (Parallel 4 Workers):** ~2.05 seconds

---

## 4. Repository Structure

```
validators/
├── documents/
│   ├── ECP_BVA_Test_Design_Notes.md        # Task 2 ECP/BVA test design notes
│   ├── Test_Execution_Guide.md             # Task 4 execution instructions
│   ├── Summary_Report.md                   # Final submission summary report
│   └── Test_Cases_Specification.xlsx       # Task 3 Excel test case matrix
├── test_cases/
│   ├── test_email_validation.py            # Task 2: Module 1 Email tests (ECP & BVA)
│   ├── test_ip_validation.py               # Task 2: Module 2 IP tests (ECP & BVA)
│   ├── test_url_validation.py              # Task 2: Module 3 URL tests (ECP & BVA)
│   ├── test_csv_email.py                   # Task 3: Email CSV data-driven tests
│   └── test_csv_ip.py                      # Task 3: IP CSV data-driven tests
├── test_data/
│   ├── email_data.csv                      # External CSV data for email validation
│   └── ip_data.csv                         # External CSV data for IP validation
├── src/                                    # Target open-source library source code
└── pytest.ini                              # Pytest test suites, markers, and path config
```
