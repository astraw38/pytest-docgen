import pytest
from pytest_docgen.pytest_docgen import doc_prep


DOCPREP_TESTDATA =[
    ("""""", []),
    ("""    hi
        test""", ["hi", "    test"]),
    (
    """
    hello
    """, ["hello"])
]


@pytest.mark.parametrize("inval,outval", DOCPREP_TESTDATA, ids=["empty docstring", "simple", "newline, doc, newline"])
def test_docprep(inval, outval):
    assert outval == doc_prep(inval)
