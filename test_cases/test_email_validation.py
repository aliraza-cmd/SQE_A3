import pytest
import validators


@pytest.mark.email
@pytest.mark.order(1)
class TestEmailValidation:

    @pytest.mark.ecp
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "email_input",
        [
            pytest.param("ali@gmail.com", id="standard_gmail"),
            pytest.param("user123@example.org", id="org_domain_with_numbers"),
            pytest.param("first.last@test.co", id="dot_in_username"),
            pytest.param("developer+filter@fast.edu.pk", id="plus_tag_and_subdomain"),
            pytest.param("1234567890@numeric.net", id="numeric_username"),
            pytest.param("support-team@company-hq.com", id="hyphenated_user_and_domain"),
        ],
    )
    def test_valid_emails_ecp(self, email_input: str):
        # Valid email formats should always pass
        assert validators.email(email_input) is True

    @pytest.mark.ecp
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "email_input",
        [
            pytest.param("plainaddress", id="no_at_or_domain"),
            pytest.param("@missinguser.com", id="missing_username"),
            pytest.param("user@", id="missing_domain"),
            pytest.param("user@.com", id="missing_domain_name"),
            pytest.param("user@domain..com", id="double_dot_in_domain"),
            pytest.param("user space@domain.com", id="space_in_username"),
            pytest.param("user@domain name.com", id="space_in_domain"),
            pytest.param("user@@domain.com", id="double_at_sign"),
        ],
    )
    def test_invalid_emails_ecp(self, email_input: str):
        # Badly structured emails should be caught and rejected
        assert not validators.email(email_input)

    @pytest.mark.bva
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "email_input,expected",
        [
            # RFC 5321: username can be up to 64 chars max
            pytest.param("u" * 64 + "@domain.com", True, id="username_exactly_64_chars"),
            # 65 chars is boundary + 1, must be rejected
            pytest.param("u" * 65 + "@domain.com", False, id="username_65_chars_too_long"),
            # Minimum allowed username length is 1 character
            pytest.param("a@b.com", True, id="username_1_char_min"),
            # 0 chars in username
            pytest.param("@domain.com", False, id="username_0_chars"),
            # Completely empty input
            pytest.param("", False, id="empty_input"),
        ],
    )
    def test_email_boundary_value_analysis(self, email_input: str, expected: bool):
        assert bool(validators.email(email_input)) is expected