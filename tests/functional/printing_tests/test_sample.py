"""
Test file for preconditions & the like
"""
import pytest

from pytest_docgen.pytest_docgen import doc_result


@pytest.fixture(scope="module", autouse=True)
def yield_nothing_fixture():
    yield b""


@doc_result
@pytest.fixture(scope="class")
def auth_session(request):
    """
    Allocates a ClientNode based off of the following specs in order:

       1. ped/pwd/rped class markers (multiple for parametrization) - used for HSM allocation.
       2. CLIENT_NODE_PARAMS class constant (for Client allocation)
       3. HSM_PARAMS class constant - for HSM allocation -- can be a list or a dictionary.
       4. Command line client specifications (--os, --bus, etc)

    .. note:: For HSM allocation & parameters

        * If `HSM_PARAMS` is set on test class
            * If it is a list, it will look for a client with HSMs matching each dictionary
              parameters (e.g. `[{'auth': PED}, {'auth': PED}]` will attempt to allocate a client
              node with 2 PED-auth HSMs attached)
            * If it is a dictionary, it will look for a client with at least ONE HSM matching
              the dictionary parameters. (e.g. `{'auth': PED}` will attempt to allocate a client
              node with at least one PED-auth HSM attached)
        * If the class is marked w/ ped or pwd, it will allocate an HSM of the current product
          type with the specified auth (if both are marked, test will be parametrized)


    :return: Allocated :class:`~LunaTAP.core.client.node.ClientNode`
    """
    print("Fixture setup: auth_session")
    yield "This is a test fixture"
    print("Fixture teardown: auth_session")

def test_module_level_test():
    print("Call: test_module_level_test")
    pass

def test_module_level_test2():
    pass

class TestRSABounds(object):
    """
    RSA Bound checking.
    """
    def test_bad_modulus(self, auth_session):
        """
        When modulus bits < 2048 using only FIPS primes, should return CKR_KEY_SIZE_RANGE
        """
        print("Call: test_bad_modulus")


    @pytest.mark.parametrize('mech', [1,
                                      2],
                             ids=["186_3_PRIMES", "186_3_AUX_PRIMES"])
    def test_largest_valid_exponent(self, auth_session, mech):
        """
        Validate that AUX primes & regular primes sign/verify correctly
        with the largest possible valid exponent.
        """
        print("Call: test_largest_valid_exponent, mech: %s" % mech)

    def test_bad_modulus_failing(self, auth_session):
        """
        Fail this test, cause I want to see decent output.
        """
        print("Call: test_bad_modulus_failing")
        assert "False" == "This isn't really false"
