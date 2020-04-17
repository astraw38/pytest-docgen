import logging

log = logging.getLogger(__name__)


def test_passing_module_level():
    """
    This is a passing module-level test.
    """
    log.info("In module test")


def test_failing_module_level():
    """
    This is a failing module-level test.
    """
    log.info("In failing module test")
    assert "pass" == "fail"


class TestClass:
    def test_passing_class_level(self):
        """
        This is a passing class-level test.
        """
        log.info("In class test")
        pass

    def test_failing_class_level(self):
        """
        This is a failing class-level test.
        """
        log.info("In failing class test")
        assert "pass" == "fail"
