import pytest


@pytest.fixture(scope="module")
def module_fixture():
    """
    Module fixture in use!
    """
    yield


@pytest.fixture(scope="class")
def class_fixture():
    """
    Class fixture in use!
    """
    yield


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
