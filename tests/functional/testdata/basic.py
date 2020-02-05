def test_passing_module_level():
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
    def test_passing_class_level(self):
        """
        This is a passing class-level test.
        """
        pass

    def test_failing_class_level(self):
        """
        This is a failing class-level test.
        """
        assert "pass" == "fail"
