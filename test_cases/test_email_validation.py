"""Automated Unit Test Cases for Email Validation Module.

Course: SE-3002 Software Quality Engineering
Assignment 3 - Task 2 & Task 4

Module Under Test: validators.email
Testing Techniques Applied:
- Equivalence Class Partitioning (ECP)
- Boundary Value Analysis (BVA)
"""

import pytest
import validators


@pytest.mark.email
@pytest.mark.order(1)
class TestEmailValidation:
    """Test suite for validators.email function using ECP and BVA techniques."""

    @pytest.mark.ecp
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "email_input",
        [
            pytest.param("ali@gmail.com", id="ECP_Valid_StandardGmail"),
            pytest.param("user123@example.org", id="ECP_Valid_OrgDomainWithDigits"),
            pytest.param("first.last@test.co", id="ECP_Valid_DotSeparatedUsername"),
            pytest.param("developer+filter@fast.edu.pk", id="ECP_Valid_SubdomainAndPlusTag"),
            pytest.param("1234567890@numeric.net", id="ECP_Valid_PureNumericUsername"),
            pytest.param("support-team@company-hq.com", id="ECP_Valid_HyphenatedNameAndDomain"),
        ],
    )
    def test_valid_emails_ecp(self, email_input: str):
        """Test valid equivalence classes for email addresses."""
        result = validators.email(email_input)
        assert result is True, f"Valid email '{email_input}' failed validation. Got: {result}"

    @pytest.mark.ecp
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "email_input",
        [
            pytest.param("plainaddress", id="ECP_Invalid_NoAtSymbolOrDomain"),
            pytest.param("@missinguser.com", id="ECP_Invalid_MissingLocalPart"),
            pytest.param("user@", id="ECP_Invalid_MissingDomainPart"),
            pytest.param("user@.com", id="ECP_Invalid_MissingDomainLabel"),
            pytest.param("user@domain..com", id="ECP_Invalid_ConsecutiveDotsInDomain"),
            pytest.param("user space@domain.com", id="ECP_Invalid_WhitespaceInUsername"),
            pytest.param("user@domain name.com", id="ECP_Invalid_WhitespaceInDomain"),
            pytest.param("user@@domain.com", id="ECP_Invalid_MultipleAtSymbols"),
        ],
    )
    def test_invalid_emails_ecp(self, email_input: str):
        """Test invalid equivalence classes for email addresses."""
        result = validators.email(email_input)
        assert not result, f"Invalid email '{email_input}' should have failed validation, but passed."

    @pytest.mark.bva
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "email_input,expected",
        [
            # Local-part length boundaries (RFC 5321 specifies maximum 64 octets for local-part)
            pytest.param("u" * 64 + "@domain.com", True, id="BVA_Valid_LocalPartMaxLength64"),
            pytest.param("u" * 65 + "@domain.com", False, id="BVA_Invalid_LocalPartExceedsMaxLength65"),
            # Minimum length boundary (1 char local part)
            pytest.param("a@b.com", True, id="BVA_Valid_LocalPartMinLength1"),
            # Boundary 0 chars local part
            pytest.param("@domain.com", False, id="BVA_Invalid_LocalPartLength0"),
            # Empty input boundary
            pytest.param("", False, id="BVA_Invalid_EmptyString"),
        ],
    )
    def test_email_boundary_value_analysis(self, email_input: str, expected: bool):
        """Test boundary conditions for username length, domain length, and input limits."""
        actual = bool(validators.email(email_input))
        assert actual is expected, (
            f"BVA email test failed for '{email_input[:20]}...' (length={len(email_input)}). "
            f"Expected: {expected}, Got: {actual}"
        )