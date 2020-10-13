import os

from pathlib import Path
import pytest

FUNC_TESTDATA = Path(os.path.join(os.path.relpath(os.path.split(__file__)[0]), "testdata"))

pytest_plugins = ("pytester",)


@pytest.fixture(scope="module")
def basic_file():
    yield (FUNC_TESTDATA / "basic.py").read_text()


@pytest.fixture(scope="module")
def fixture_file():
    yield (FUNC_TESTDATA / "tests_with_fixtures.py").read_text()


@pytest.fixture(scope="module")
def generic_file():
    yield (FUNC_TESTDATA / "tests_with_generic_section.py").read_text()


@pytest.fixture(scope="module")
def logging_file():
    yield (FUNC_TESTDATA / "tests_with_logging.py").read_text()


class TestDocgenOptions:
    def test_no_rst_dir(self, basic_file, testdir):
        testdir.makepyfile(basic_file)
        result = testdir.runpytest_inprocess()
        result.assert_outcomes(2, 0, 2)

        # Verify that we created documents in the specified location.
        loc = testdir.tmpdir
        assert "_docs" not in os.listdir(loc)

    def test_rst_dir(self, basic_file, testdir):
        testdir.makepyfile(basic_file)
        result = testdir.runpytest_inprocess("--rst-dir=_docs")
        result.assert_outcomes(2, 0, 2)

        # Verify that we created documents in the specified location.
        loc = testdir.tmpdir
        assert "_docs" in os.listdir(loc)

    def test_rst_index(self, basic_file, testdir):
        testdir.makepyfile(basic_file)
        result = testdir.runpytest_inprocess("--rst-dir=_docs", "--rst-write-index")
        result.assert_outcomes(2, 0, 2)

        # Verify that we created documents in the specified location.
        loc = testdir.tmpdir
        assert "index.rst" in os.listdir(os.path.join(loc, "_docs"))

    def test_rst_title(self, basic_file, testdir):
        testdir.makepyfile(basic_file)
        result = testdir.runpytest_inprocess(
            "--rst-dir=_docs", "--rst-write-index", "--rst-title=UniqueTitle"
        )
        result.assert_outcomes(2, 0, 2)

        # Verify that we created documents in the specified location.
        loc = testdir.tmpdir
        assert "index.rst" in os.listdir(os.path.join(loc, "_docs"))
        with open(os.path.join(loc, "_docs", "index.rst")) as f:
            data = f.read()
        assert "UniqueTitle" in data

    def test_rst_desc(self, basic_file, testdir):
        testdir.makepyfile(basic_file)
        result = testdir.runpytest_inprocess(
            "--rst-dir=_docs", "--rst-write-index", "--rst-desc=UniqueDesc"
        )
        result.assert_outcomes(2, 0, 2)

        # Verify that we created documents in the specified location.
        loc = testdir.tmpdir
        assert "index.rst" in os.listdir(os.path.join(loc, "_docs"))
        with open(os.path.join(loc, "_docs", "index.rst")) as f:
            data = f.read()
        assert "UniqueDesc" in data

    def test_rst_with_fixtures(self, testdir, fixture_file):
        testdir.makepyfile(fixture_file)
        result = testdir.runpytest_inprocess("--rst-dir=_docs", "--rst-fixture-results")
        result.assert_outcomes(3, 0, 2, 1)

        # note: pytester makes a test file w/ the unittest name as the name of the file.
        # that gets translated to the final .rst too.
        test_rst_file = "test_rst_with_fixtures.rst"
        loc = testdir.tmpdir
        assert test_rst_file in os.listdir(os.path.join(loc, "_docs"))

        with open(os.path.join(loc, "_docs", test_rst_file)) as f:
            data = f.read()
        assert "Module fixture in use!" in data

    def test_rst_with_added_section(self, testdir, generic_file):
        testdir.makepyfile(generic_file)
        result = testdir.runpytest_inprocess(
            "--rst-dir=_docs",
        )
        result.assert_outcomes(3, 0, 2, 1)

        # note: pytester makes a test file w/ the unittest name as the name of the file.
        # that gets translated to the final .rst too.
        test_rst_file = "test_rst_with_added_section.rst"
        loc = testdir.tmpdir
        assert test_rst_file in os.listdir(os.path.join(loc, "_docs"))

        with open(os.path.join(loc, "_docs", test_rst_file)) as f:
            data = f.read()
        assert ":module_fixture: Module" in data

    @pytest.mark.xfail(reason="Need to sort out why logging not showing up in output")
    def test_logging(self, testdir, logging_file):
        testdir.makepyfile(logging_file)
        result = testdir.runpytest_inprocess("--rst-dir=_docs", "-o log_level=INFO")
        result.assert_outcomes(2, 0, 2)

        # note: pytester makes a test file w/ the unittest name as the name of the file.
        # that gets translated to the final .rst too.
        test_rst_file = "test_logging.rst"
        loc = testdir.tmpdir
        assert test_rst_file in os.listdir(os.path.join(loc, "_docs"))

        with open(os.path.join(loc, "_docs", test_rst_file)) as f:
            data = f.read()
        assert "INFO     test_logging:test_logging.py:8 In module test" in data
