# ECP & BVA Test Design Notes

**Course:** SE-3002 Software Quality Engineering  
**Assignment:** Assignment 3 – Build Unit Test Automation Solution  
**Target Open-Source Project:** `validators` (Python)  
**Repository Location:** `src/validators/`  

---

## 1. Group Member Allocation & Task Distribution

| Member Name | Role & Responsibility | Assigned Modules / Tasks |
|:---|:---|:---|
| **Ali Raza** | Lead QA Engineer & Automation Architect | Module 1 (`validators.email`), Task 4 Test Suite Configuration & Ordering |
| **Ali Asif** | Test Automation Engineer | Module 2 (`validators.ip_address`), Task 3 CSV Data-Driven Testing (`email_data.csv` & `ip_data.csv`) |

---

## 2. Identified Application Modules

We selected core validation modules from the `validators` library:

1. **Module 1: Email Address Validation (`validators.email`)**
   - Implements email format and syntax checking adhering to RFC 5321, RFC 5322, and RFC 1034.
   - Validates local part (max 64 characters) and domain part (max 253 characters).

2. **Module 2: IP Address Validation (`validators.ip_address`)**
   - Validates IPv4 (`validators.ipv4`) addresses, CIDR notation, and private/public address rules.
   - Validates IPv6 (`validators.ipv6`) addresses including IPv4-mapped, compressed notations, and hextet boundaries.

---

## 3. Module 1: Email Validation (`validators.email`)

### 3.1 Equivalence Class Partitioning (ECP)

| Partition ID | Partition Description | Class Type | Sample Input | Expected Result |
|:---|:---|:---:|:---|:---:|
| **ECP-EM-01** | Standard well-formed email | Valid | `ali@gmail.com` | `True` |
| **ECP-EM-02** | Alphanumeric username with `.org` domain | Valid | `user123@example.org` | `True` |
| **ECP-EM-03** | Dot-separated local part | Valid | `first.last@test.co` | `True` |
| **ECP-EM-04** | Subaddressing (`+` tag) with subdomain | Valid | `developer+filter@fast.edu.pk` | `True` |
| **ECP-EM-05** | Numeric local part | Valid | `1234567890@numeric.net` | `True` |
| **ECP-EM-06** | Hyphenated username and domain | Valid | `support-team@company-hq.com` | `True` |
| **ECP-EM-07** | Missing `@` and domain entirely | Invalid | `plainaddress` | `False` |
| **ECP-EM-08** | Missing username (starts with `@`) | Invalid | `@missinguser.com` | `False` |
| **ECP-EM-09** | Missing domain (ends with `@`) | Invalid | `user@` | `False` |
| **ECP-EM-10** | Missing domain name label before TLD | Invalid | `user@.com` | `False` |
| **ECP-EM-11** | Consecutive dots in domain part | Invalid | `user@domain..com` | `False` |
| **ECP-EM-12** | Whitespace within local part | Invalid | `user space@domain.com` | `False` |
| **ECP-EM-13** | Whitespace within domain part | Invalid | `user@domain name.com` | `False` |
| **ECP-EM-14** | Multiple `@` symbols present | Invalid | `user@@domain.com` | `False` |

### 3.2 Boundary Value Analysis (BVA)

RFC 5321 specifies that the local part of an email address cannot exceed 64 octets.

| Boundary ID | Boundary Under Test | Tested Value | Input String | Expected Result |
|:---|:---|:---:|:---|:---:|
| **BVA-EM-01** | Max local-part length (on-boundary) | 64 chars | `"u" * 64 + "@domain.com"` | `True` |
| **BVA-EM-02** | Exceeds max local-part (off-boundary) | 65 chars | `"u" * 65 + "@domain.com"` | `False` |
| **BVA-EM-03** | Min local-part length (on-boundary) | 1 char | `a@b.com` | `True` |
| **BVA-EM-04** | Zero local-part length (off-boundary) | 0 chars | `@domain.com` | `False` |
| **BVA-EM-05** | Total input length lower bound | 0 chars | `""` | `False` |

---

## 4. Module 2: IP Address Validation (`validators.ip_address`)

### 4.1 IPv4 Equivalence Class Partitioning (ECP)

| Partition ID | Partition Description | Class Type | Sample Input | Expected Result |
|:---|:---|:---:|:---|:---:|
| **ECP-IP4-01** | Class C private network IP | Valid | `192.168.1.1` | `True` |
| **ECP-IP4-02** | Class A private network IP | Valid | `10.0.0.1` | `True` |
| **ECP-IP4-03** | Class B private network IP | Valid | `172.16.254.1` | `True` |
| **ECP-IP4-04** | Localhost loopback IP | Valid | `127.0.0.1` | `True` |
| **ECP-IP4-05** | Public DNS resolver IP | Valid | `8.8.8.8` | `True` |
| **ECP-IP4-06** | Non-numeric characters in octets | Invalid | `abc.def.ghi.jkl` | `False` |

### 4.2 IPv4 Boundary Value Analysis (BVA)

IPv4 addresses consist of 4 octets, each in the integer range `[0, 255]`.

| Boundary ID | Boundary Under Test | Tested Value | Input String | Expected Result |
|:---|:---|:---:|:---|:---:|
| **BVA-IP4-01** | Lower valid octet bound (all 0s) | 0 | `0.0.0.0` | `True` |
| **BVA-IP4-02** | Upper valid octet bound (all 255s) | 255 | `255.255.255.255` | `True` |
| **BVA-IP4-03** | Upper octet bound + 1 | 256 | `256.0.0.1` | `False` |
| **BVA-IP4-04** | Lower octet bound - 1 (negative) | -1 | `192.168.1.-1` | `False` |
| **BVA-IP4-05** | Octet count lower bound (3 octets) | 3 octets | `192.168.1` | `False` |
| **BVA-IP4-06** | Octet count upper bound (5 octets) | 5 octets | `192.168.1.1.1` | `False` |
| **BVA-IP4-07** | Empty string boundary | 0 chars | `""` | `False` |

### 4.3 IPv6 Equivalence Class Partitioning (ECP)

| Partition ID | Partition Description | Class Type | Sample Input | Expected Result |
|:---|:---|:---:|:---|:---:|
| **ECP-IP6-01** | Compressed IPv6 loopback | Valid | `::1` | `True` |
| **ECP-IP6-02** | Full uncompressed 8-hextet address | Valid | `2001:0db8:85a3:0000:0000:8a2e:0370:7334` | `True` |
| **ECP-IP6-03** | Link-local IPv6 address | Valid | `fe80::1` | `True` |
| **ECP-IP6-04** | IPv4-mapped IPv6 address | Valid | `::ffff:192.0.2.1` | `True` |
| **ECP-IP6-05** | Compressed IPv6 with max hextet | Valid | `2001:db8::ffff` | `True` |
| **ECP-IP6-06** | Double compression `::` violation | Invalid | `2001::db8::1` | `False` |

### 4.4 IPv6 Boundary Value Analysis (BVA)

IPv6 addresses consist of up to 8 hextets of 16-bit values (`[0x0000, 0xFFFF]`).

| Boundary ID | Boundary Under Test | Tested Value | Input String | Expected Result |
|:---|:---|:---:|:---|:---:|
| **BVA-IP6-01** | Hextet count limit + 1 (9 groups) | 9 groups | `1:2:3:4:5:6:7:8:9` | `False` |
| **BVA-IP6-02** | Non-hex character boundary | 'g' (off-boundary) | `gggg::1` | `False` |
| **BVA-IP6-03** | 16-bit hextet overflow (> 0xFFFF) | 0x10000 | `2001:db8::10000` | `False` |
| **BVA-IP6-04** | Empty string boundary | 0 chars | `""` | `False` |

---

## 5. Summary of Test Coverage

- **Total Unit Test Cases Implemented:** 55
- **Test Modules Covered:** `email`, `ip_address` (`ipv4` & `ipv6`)
- **Techniques Applied:** Equivalence Class Partitioning (ECP) & Boundary Value Analysis (BVA)
- **External Data-Driven Tests:** 13 (Consuming `email_data.csv` and `ip_data.csv`)
- **Pass Rate:** 100% (55/55 passed)
