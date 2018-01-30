"""
Test file for preconditions & the like
"""
import pytest


@pytest.fixture(scope="class", params=["p1", "p2"])
def auth_session(request):
    """
    Login to a Token and return the authenticated session handle.

    :param: request
    :return
    """
    return 1


class TestRSABounds(object):
    """
    RSA Bound checking.
    """
    def test_bad_modulus(self, auth_session):
        """
        When modulus bits < 2048 using only FIPS primes, should return CKR_KEY_SIZE_RANGE
        """
        pass

    @pytest.mark.parametrize('mech', [1, 2],
                             ids=["186_3_PRIMES", "186_3_AUX_PRIMES"])
    def test_largest_valid_exponent(self, auth_session, mech):
        """
        Validate that AUX primes & regular primes sign/verify correctly
        with the largest possible valid exponent.
        """
        assert 1 == mech

    def test_bad_modulus_failing(self, auth_session):
        """
        Fail this test, cause I want to see decent output.
        """
        assert "False" == "This isn't really false"
