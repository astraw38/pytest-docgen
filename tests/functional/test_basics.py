import os

import pytest

pytest_plugins = ("pytester",)


@pytest.fixture(scope="module")
def basic_file():
    with open("testdata/basic.py", "r") as f:
        data = f.read()
    yield data


@pytest.fixture(scope="module")
def fixture_file():
    with open("testdata/tests_with_fixtures.py", "r") as f:
        data = f.read()
    yield data


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
