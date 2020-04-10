import pytest


def doc_generic(funcarg, funcval):
    return [":{}: {}".format(funcarg, funcval)]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    # If we're using pytest-docgen, we'll have a doc collector
    func_args = item.funcargs
    try:
        if hasattr(item, "_doccol"):
            doccol = item._doccol
            for fixture, funcval in func_args.items():
                if doccol.has_section("Parameters"):
                    doccol.append_to_section("Parameters", doc_generic(fixture, funcval))
                else:
                    doccol.add_section("Parameters", doc_generic(fixture, funcval), loc=1)
    except Exception as exc:
        # failed to add doc section.
        raise
    yield


@pytest.fixture(scope="module")
def module_fixture(request):
    """
    Module fixture in use!
    """
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
    yield "Function"


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
    def test_passing_class_level(self, class_fixture, module_fixture):
        """
        This is a passing class-level test.
        """
        pass

    def test_failing_class_level(self, func_fixture):
        """
        This is a failing class-level test.
        """
        assert "pass" == "fail"

    def test_func_fixture(self, func_fixture):
        pass

    def test_failing_fixture(self, failing_fixture):
        pass
