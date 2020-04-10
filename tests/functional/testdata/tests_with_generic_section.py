import pytest
from collections import namedtuple

from pytest_docgen.pytest_docgen import DocSection


def doc_generic(funcarg, funcval):
    return [":{}: {}".format(funcarg, funcval)]


@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    outcome = yield
    # If we're using pytest-docgen, we'll have a doc collector
    try:
        if hasattr(request.node, "_doccol"):
            doccol = request.node._doccol
            doccol.add_section(
                "preconditions",
                DocSection("Parameters", doc_generic(fixturedef.argname, outcome.get_result())),
            )
    except Exception:
        # failed to add doc section.
        raise


@pytest.fixture(scope="module")
def module_fixture(request):
    """
    Module fixture in use!
    """

    if hasattr(request.node, "_doccol"):
        doccol = request.node._doccol
        doccol.add_section(
            "preconditions",
            DocSection("Parameters", [":module_fixture: Module"])),
    yield "Module"


@pytest.fixture(scope="class")
def class_fixture():
    """
    Class fixture in use!
    """
    yield "Class"


@pytest.fixture()
def func_fixture():
    """
    Function fixture in use!"
    """
    yield


@pytest.fixture()
def failing_fixture():
    assert False, "Precondition failed!"


def test_passing_module_level(module_fixture):
    """
    This is a passing module-level test.
    """
    pass


def test_failing_module_level():
    """
    This is a failing module-level test.
    """
    assert "pass" == "fail"


class TestClass:
    def test_passing_class_level(self, class_fixture):
        """
        This is a passing class-level test.
        """
        pass

    def test_failing_class_level(self):
        """
        This is a failing class-level test.
        """
        assert "pass" == "fail"

    def test_func_fixture(self, func_fixture):
        pass

    def test_failing_fixture(self, failing_fixture):
        pass
