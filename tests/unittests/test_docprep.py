import pytest
from pytest_docgen.pytest_docgen import doc_prep


DOCPREP_TESTDATA =[
    ("""""", []),
    ("""    hi
        test""", ["hi", "    test"]),
]


@pytest.mark.parametrize("inval,outval", DOCPREP_TESTDATA, ids=["empty docstring", "simple"])
def test_docprep(inval, outval):
    assert doc_prep(inval) == outval
