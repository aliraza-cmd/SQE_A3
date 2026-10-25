import pytest
import validators


@pytest.mark.ip
@pytest.mark.order(2)
class TestIPValidation:

    # --- IPv4 Tests ---

    @pytest.mark.ecp
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "ip_input",
        [
            pytest.param("192.168.1.1", id="class_c_private"),
            pytest.param("10.0.0.1", id="class_a_private"),
            pytest.param("172.16.254.1", id="class_b_private"),
            pytest.param("127.0.0.1", id="localhost_loopback"),
            pytest.param("8.8.8.8", id="public_dns"),
        ],
    )
    def test_ipv4_valid_ecp(self, ip_input: str):
        assert validators.ipv4(ip_input) is True

    @pytest.mark.bva
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "ip_input,expected",
        [
            # Octets range from 0 to 255
            pytest.param("0.0.0.0", True, id="min_boundary_all_zeros"),
            pytest.param("255.255.255.255", True, id="max_boundary_all_255"),
            # 256 is upper bound + 1, invalid
            pytest.param("256.0.0.1", False, id="octet_over_255"),
            # Negative octet
            pytest.param("192.168.1.-1", False, id="negative_octet"),
            # Needs exactly 4 octets
            pytest.param("192.168.1", False, id="only_3_octets"),
            pytest.param("192.168.1.1.1", False, id="5_octets_too_many"),
            # Letters in place of numbers
            pytest.param("abc.def.ghi.jkl", False, id="non_numeric_chars"),
            pytest.param("", False, id="empty_input"),
        ],
    )
    def test_ipv4_bva_and_invalid(self, ip_input: str, expected: bool):
        assert bool(validators.ipv4(ip_input)) is expected

    # --- IPv6 Tests ---

    @pytest.mark.ecp
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "ip_input",
        [
            pytest.param("::1", id="compressed_loopback"),
            pytest.param(
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                id="full_8_hextets",
            ),
            pytest.param("fe80::1", id="link_local"),
            pytest.param("::ffff:192.0.2.1", id="ipv4_mapped_ipv6"),
            pytest.param("2001:db8::ffff", id="max_hextet_value_ffff"),
        ],
    )
    def test_ipv6_valid_ecp(self, ip_input: str):
        assert validators.ipv6(ip_input) is True

    @pytest.mark.bva
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "ip_input,expected",
        [
            # IPv6 only allows 8 groups max
            pytest.param("1:2:3:4:5:6:7:8:9", False, id="9_hextets_exceeds_max"),
            # Hex only allows 0-9 and a-f, 'g' is invalid
            pytest.param("gggg::1", False, id="invalid_hex_letter_g"),
            # Hextet max value is 0xFFFF (4 hex digits)
            pytest.param("2001:db8::10000", False, id="hextet_overflow_5_digits"),
            # Cannot compress with '::' more than once
            pytest.param("2001::db8::1", False, id="double_compression"),
            pytest.param("", False, id="empty_input"),
        ],
    )
    def test_ipv6_bva_and_invalid(self, ip_input: str, expected: bool):
        assert bool(validators.ipv6(ip_input)) is expected