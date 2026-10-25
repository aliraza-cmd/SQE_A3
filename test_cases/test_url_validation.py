"""Automated Unit Test Cases for URL Validation Module.

Course: SE-3002 Software Quality Engineering
Assignment 3 - Task 2 & Task 4

Module Under Test: validators.url
Testing Techniques Applied:
- Equivalence Class Partitioning (ECP)
- Boundary Value Analysis (BVA)
"""

import pytest
import validators


@pytest.mark.url
@pytest.mark.order(3)
class TestURLValidation:
    """Test suite for validators.url function using ECP and BVA techniques."""

    @pytest.mark.ecp
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "url_input",
        [
            pytest.param("https://google.com", id="ECP_URL_Valid_StandardHTTPS"),
            pytest.param("http://example.org", id="ECP_URL_Valid_StandardHTTP"),
            pytest.param("ftp://files.example.com", id="ECP_URL_Valid_FTPScheme"),
            pytest.param("https://fast.edu.pk:8080", id="ECP_URL_Valid_CustomPort"),
            pytest.param(
                "https://example.com/api/v1?search=test&sort=asc",
                id="ECP_URL_Valid_PathAndQueryParameters",
            ),
            pytest.param("https://example.com/home#section2", id="ECP_URL_Valid_Fragment"),
        ],
    )
    def test_url_valid_ecp(self, url_input: str):
        """Test valid equivalence classes for diverse URL schemes, ports, and parameters."""
        result = validators.url(url_input)
        assert result is True, f"Valid URL '{url_input}' failed validation. Got: {result}"

    @pytest.mark.ecp
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "url_input",
        [
            pytest.param("not-a-url", id="ECP_URL_Invalid_MissingSchemeAndNetloc"),
            pytest.param("htp://wrong-scheme.com", id="ECP_URL_Invalid_UnsupportedTypoScheme"),
            pytest.param("http://", id="ECP_URL_Invalid_MissingHostname"),
            pytest.param("https://exam ple.com", id="ECP_URL_Invalid_WhitespaceInDomain"),
            pytest.param("javascript:alert(1)", id="ECP_URL_Invalid_JavaScriptPseudoScheme"),
            pytest.param("http://-leading-hyphen.com", id="ECP_URL_Invalid_LeadingHyphenInHost"),
        ],
    )
    def test_url_invalid_ecp(self, url_input: str):
        """Test invalid equivalence classes for malformed URLs and unsupported protocols."""
        result = validators.url(url_input)
        assert not result, f"Invalid URL '{url_input}' should have failed validation, but passed."

    @pytest.mark.bva
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "url_input,expected",
        [
            # Minimal domain length (single character second-level domain)
            pytest.param("http://a.io", True, id="BVA_URL_Valid_MinDomainLength"),
            # Port lower valid bound: 1
            pytest.param("http://example.com:1", True, id="BVA_URL_Valid_PortMinBound1"),
            # Port upper valid bound: 65535
            pytest.param("http://example.com:65535", True, id="BVA_URL_Valid_PortMaxBound65535"),
            # Port upper bound + 1: 65536 (invalid)
            pytest.param("http://example.com:65536", False, id="BVA_URL_Invalid_PortExceeds65535"),
            # Port lower bound - 1: 0 (invalid)
            pytest.param("http://example.com:0", False, id="BVA_URL_Invalid_PortZero"),
            # Empty input boundary
            pytest.param("", False, id="BVA_URL_Invalid_EmptyString"),
        ],
    )
    def test_url_bva(self, url_input: str, expected: bool):
        """Test boundary value analysis for port boundaries and length constraints."""
        actual = bool(validators.url(url_input))
        assert actual is expected, (
            f"URL BVA test failed for '{url_input}'. Expected: {expected}, Got: {actual}"
        )
