"""Automated Unit Test Cases for IP Address Validation Module.

Course: SE-3002 Software Quality Engineering
Assignment 3 - Task 2 & Task 4

Module Under Test: validators.ip_address (ipv4 & ipv6)
Testing Techniques Applied:
- Equivalence Class Partitioning (ECP)
- Boundary Value Analysis (BVA)
"""

import pytest
import validators


@pytest.mark.ip
@pytest.mark.order(2)
class TestIPValidation:
    """Test suite for IPv4 and IPv6 validators using ECP and BVA techniques."""

    # ==================== IPv4 Tests ====================

    @pytest.mark.ecp
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "ip_input",
        [
            pytest.param("192.168.1.1", id="ECP_IPv4_Valid_ClassC_Private"),
            pytest.param("10.0.0.1", id="ECP_IPv4_Valid_ClassA_Private"),
            pytest.param("172.16.254.1", id="ECP_IPv4_Valid_ClassB_Private"),
            pytest.param("127.0.0.1", id="ECP_IPv4_Valid_Loopback"),
            pytest.param("8.8.8.8", id="ECP_IPv4_Valid_PublicDNS"),
        ],
    )
    def test_ipv4_valid_ecp(self, ip_input: str):
        """Test valid equivalence classes across different IPv4 network classes."""
        result = validators.ipv4(ip_input)
        assert result is True, f"Valid IPv4 address '{ip_input}' failed validation. Got: {result}"

    @pytest.mark.bva
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "ip_input,expected",
        [
            # Octet boundary 0 (lower valid bound)
            pytest.param("0.0.0.0", True, id="BVA_IPv4_Valid_LowerOctetBound0"),
            # Octet boundary 255 (upper valid bound)
            pytest.param("255.255.255.255", True, id="BVA_IPv4_Valid_UpperOctetBound255"),
            # Octet boundary 256 (upper bound + 1, invalid)
            pytest.param("256.0.0.1", False, id="BVA_IPv4_Invalid_OctetExceeds255"),
            # Negative octet (lower bound - 1, invalid)
            pytest.param("192.168.1.-1", False, id="BVA_IPv4_Invalid_NegativeOctet"),
            # Structural boundaries: 3 octets (boundary - 1)
            pytest.param("192.168.1", False, id="BVA_IPv4_Invalid_TooFewOctets"),
            # Structural boundaries: 5 octets (boundary + 1)
            pytest.param("192.168.1.1.1", False, id="BVA_IPv4_Invalid_TooManyOctets"),
            # Non-numeric partition
            pytest.param("abc.def.ghi.jkl", False, id="ECP_IPv4_Invalid_NonNumeric"),
            # Empty input boundary
            pytest.param("", False, id="BVA_IPv4_Invalid_EmptyString"),
        ],
    )
    def test_ipv4_bva_and_invalid(self, ip_input: str, expected: bool):
        """Test boundary value analysis and invalid partitions for IPv4 addresses."""
        actual = bool(validators.ipv4(ip_input))
        assert actual is expected, (
            f"IPv4 test failed for '{ip_input}'. Expected: {expected}, Got: {actual}"
        )

    # ==================== IPv6 Tests ====================

    @pytest.mark.ecp
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "ip_input",
        [
            pytest.param("::1", id="ECP_IPv6_Valid_LoopbackCompressed"),
            pytest.param(
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                id="ECP_IPv6_Valid_FullUncompressed8Hextets",
            ),
            pytest.param("fe80::1", id="ECP_IPv6_Valid_LinkLocal"),
            pytest.param("::ffff:192.0.2.1", id="ECP_IPv6_Valid_IPv4MappedIPv6"),
            pytest.param("2001:db8::ffff", id="ECP_IPv6_Valid_MaxHextetValue"),
        ],
    )
    def test_ipv6_valid_ecp(self, ip_input: str):
        """Test valid equivalence classes for IPv6 addresses."""
        result = validators.ipv6(ip_input)
        assert result is True, f"Valid IPv6 address '{ip_input}' failed validation. Got: {result}"

    @pytest.mark.bva
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "ip_input,expected",
        [
            # Boundary: 9 hextets (exceeds max 8 hextet boundary)
            pytest.param("1:2:3:4:5:6:7:8:9", False, id="BVA_IPv6_Invalid_Exceeds8Hextets"),
            # Hexadecimal boundary: character 'g' (outside [0-9a-fA-F])
            pytest.param("gggg::1", False, id="BVA_IPv6_Invalid_NonHexCharacter"),
            # Hextet value boundary: 5 hex digits (exceeds 16-bit 0xFFFF boundary)
            pytest.param("2001:db8::10000", False, id="BVA_IPv6_Invalid_HextetOverflow"),
            # Multiple compression '::' boundary violation
            pytest.param("2001::db8::1", False, id="ECP_IPv6_Invalid_DoubleCompression"),
            # Empty input boundary
            pytest.param("", False, id="BVA_IPv6_Invalid_EmptyString"),
        ],
    )
    def test_ipv6_bva_and_invalid(self, ip_input: str, expected: bool):
        """Test boundary value analysis and invalid partitions for IPv6 addresses."""
        actual = bool(validators.ipv6(ip_input))
        assert actual is expected, (
            f"IPv6 test failed for '{ip_input}'. Expected: {expected}, Got: {actual}"
        )