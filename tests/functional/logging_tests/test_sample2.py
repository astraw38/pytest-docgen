"""
Test file for preconditions & the like
"""
import logging
import pytest

from pytest_docgen.pytest_docgen import doc_result

LOG = logging.getLogger(__name__)


@doc_result
@pytest.fixture(scope="class", params=["p1", "p2"])
def auth_session(request):
    """
    Login to a Token and return the authenticated session handle.

    :param: request
    :return: Session handle.
    """
    LOG.debug("Creating auth_session w/ param %s", request.param)
    yield 1
    LOG.debug("Destroying auth_session w/ param %s", request.param)


@pytest.fixture()
def failing_fixture():
    """
    THis fixture will fail during setup.
    """
    assert False, "Failed!"
    yield
    assert False, "Failed in teardown!"


class TestRSABounds(object):
    """
    RSA Bound checking.
    """
    def test_bad_modulus(self, auth_session):
        """
        When modulus bits < 2048 using only FIPS primes, should return CKR_KEY_SIZE_RANGE
        """
        LOG.debug("Call: test_bad_modulus")

    @pytest.mark.parametrize('mech', [1,
                                      2],
                             ids=["186_3_PRIMES", "186_3_AUX_PRIMES"])
    def test_largest_valid_exponent(self, auth_session, mech):
        """
        Validate that AUX primes & regular primes sign/verify correctly
        with the largest possible valid exponent.
        """
        LOG.debug("Call: test_largest_valid_exponent, mech: %s" % mech)

    def test_bad_modulus_failing(self, auth_session):
        """
        Fail this test, cause I want to see decent output.
        """
        LOG.debug("Call: test_bad_modulus_failing")
        assert "False" == "This isn't really false"

