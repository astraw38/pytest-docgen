"""
From a test file setup like this::


    @pytest.fixture(scope='class')
    def a():
        '''
        This is a's fixture doc
        '''
        pass

    @pytest.fixture(scope='function')
    def b():
        '''
        This is b's fixture doc
        '''
        pass

    class TestMe(object):
        '''
        This is the docstring of the TestMe class
        '''
        def test_one(self, a, b):
            '''
            This is test_one's docstring.
            '''
            pass


An RST file would be generated on test execution::


    =====
    Title
    =====

    Test run description. The title & this description can either be preset, or
    pulled from pytest runtime configuration via commandline.


    .. topic:: Session Fixtures

        fixture1
            Fixture1's documentation

        fixture 2
            Fixture2's documentation


    Module.path.test_sample
    -----------------------

    This is the docstring of the Module.

    .. topic:: Module Fixtures

        mod1
            mod1's documentation

        mod2
            mod2's documentation

    TestMe
    ~~~~~~

    This is the docstring of the TestMe class


    .. topic:: Class Fixtures

        a
            a's documentation


    test_one
    ++++++++

    This is test_one's docstring.

    .. topic:: Function Fixtures

        b
            b's documentation

    .. topic:: Test Result

    setup
        PASSED|FAILED|SKIPPED
    call
        PASSED|FAILED|SKIPPED
    teardown
        PASSED|FAILED|SKIPPED

    # Note: if one of these were a failure, it should look like:


       call
          FAILED

          .. code-block:: none

             self = <CC.test_precons.TestRSABounds object at 0xb4176e0c>, auth_session = 0

                 def test_bad_modulus_failing(self, auth_session):
                     '''
                     Fail this test, cause I want to see decent output.
                     '''
             >       assert "False" == "This isn't really false"
             E       assert 'False' == "This isn't really false"
             E         - False
             E         + This isn't really false

             CC/test_precons.py:42: AssertionError


 A bonus option would be to have a link to captured logs for a given test. Should we store it for all
 tests or just failed/skipped? not sure. I think all should be an option.

"""
import os

import pytest
import inspect

from _pytest.main import Session
from _pytest.python import Instance
from rstcloth.rstcloth import RstCloth

# There are 4 levels we care about
# Level 0 ::    session     :: =====
# Level 1 ::    module      :: ------
# Level 2 ::    class       :: ~~~~~~
# Level 3 ::    function    :: ++++++

SESSION_HEADER_MAP = {
    "session": "h1",
    "module": "h2",
    "class": "h3",
    "function": "h4"
}


def doc_prep(docstring):
    """
    Splits a docstring by newlines, and finds the minimum indent level, then lstrips that much
    indentation off each line of the docstring.

    :param docstring:
    :return: Docstring linesplit.
    :rtype: list
    """
    if not docstring:
        return []
    doclines = docstring.splitlines()
    indents = [len(x) - len(x.lstrip()) for x in doclines if x and not x.isspace()]
    if not indents:
        return []
    min_indent = min(indents)
    return [x[min_indent:] for x in doclines]


class NodeDocCollector(object):
    def __init__(self,
                 node_name,
                 node_doc,
                 level="session",
                 write_toc=False,
                 ):
        self.node_name = node_name
        self.node_doc = node_doc
        self.write_toc = write_toc
        # Children should be a list of NodeDocCollectors of a smaller level.
        # Can be chained on down.
        self.children = []
        self._fixtures = []
        self._results = []
        self.level = level

    def __str__(self):
        return "NodeDocCollector(name=%s, level=%s, children=%d)" % (self.node_name, self.level, len(self.children))

    def _build(self):
        rst = RstCloth()
        if self.write_toc:
            rst.directive(name="toctree",
                          fields=[('hidden', ''),
                                  ('includehidden', '')])
            rst.newline()

        getattr(rst, SESSION_HEADER_MAP[self.level])(self.node_name)
        rst.newline()
        rst.content(doc_prep(self.node_doc))
        rst.newline()

        rst.directive(name="topic",
                      arg="{}{} Fixtures".format(self.level[0].upper(), self.level[1:]))
        rst.newline()

        if self._fixtures:
            for fixture_name, fixture_doc in self._fixtures:
                rst.definition(name=fixture_name,
                               text="\n".join(fixture_doc),
                               indent=3,
                               wrap=False)  # Note: indent is 3 here so that it shows up under the Fixtures panel.
        else:
            rst.content("None!",
                        indent=3)
        rst.newline(2)

        if self._results:
            rst.directive("topic",
                          arg="Test Results")
            rst.newline()
            for when, outcome in self._results:
                rst.definition(name=when,
                               text="\n".join(outcome),
                               indent=3,
                               bold=True,
                               wrap=False)

        for subdoc in self.children:
            rst._add(subdoc.emit())
            rst.newline(2)
        return rst

    def emit(self):
        """
        Return internal representation of what a given node's rst doc output should be.
        """
        rst = self._build()
        return rst.data

    def write(self, filename):
        """
        Write the internal RST document to given filename.

        :param str filename: File to write.
        """
        rst = self._build()
        rst.write(filename)

    def add_fixture(self, fixturedef, param_index=0):
        """
        Add a fixture to the RST documentation.

        :param fixturedef: Pytest Fixture definition object
        :param param_index: For parameterized tests, there is an internal pytest
            fixture. No docstring to pull from that (that would be relevant), so
            we need the parameter index that we're at to at least give us some decent
            output.
        """
        if fixturedef.func.__name__ == "get_direct_param_fixture_func":
            # TODO: the param index typically comes from the request. Might need to add that into args.
            doc = str(fixturedef.params[param_index])
        else:
            doc = fixturedef.func.__doc__ or "empty docstring"
        fixture_info = (fixturedef.argname, doc_prep(doc))
        if fixture_info not in self._fixtures:
            self._fixtures.append(fixture_info)

    def add_result(self, result):
        """
        Add a test result to the documentation.

        This should be called 3x for each test -- 1x for setup, 1x for call, 1x for teardown.

        :param result: Pytest result object
        """
        if result.outcome != "passed":
            # Store the longrepr
            # TODO: This might need to do some munging on the data.
            outcome = ['FAILED',
                       '::'
                       ] + ["".join(["   ", x]) for x in result.longreprtext.split('\n')]
        else:
            outcome = [result.outcome.upper()]
        self._results.append((result.when, outcome))


def get_level(item):
    """
    Return the current pytest collection level an item is at.

    :param item: Pytest item
    :return: Collection level (as string)
    """
    if inspect.isfunction(item.obj):
        return "function"
    if inspect.isclass(item.obj):
        return "class"
    elif inspect.ismodule(item.obj):
        return "module"
    else:
        raise Exception("Unknown level of item!")


def doccollect_parent(item, prev_item=None):
    """
    Set up doc collectors for each level.
    This is the time we have to do this, because it's really hard to get
    a given object's docstring w/o using fixtures.
    """
    if not prev_item:
        prev_item = item
    if isinstance(item.parent, Session):
        # End recursion -- we hit the top level
        if prev_item._doccol not in item.parent.doc_collectors:
            item.parent.doc_generators.append(prev_item._doccol)
        return
    if isinstance(item.parent, Instance):
        # Skip pytest Instances
        doccollect_parent(item.parent, item)
        return
    parent = item.parent
    doccol = getattr(parent, "_doccol", None)
    if doccol is None:
        level = get_level(parent)
        doccol = NodeDocCollector(parent.obj.__name__,
                                  parent.obj.__doc__,
                                  level=level,
                                  write_toc=level == "module")
        parent._doccol = doccol

    if prev_item._doccol not in doccol.children:
        doccol.children.append(prev_item._doccol)
    doccollect_parent(parent)


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(items):
    """
    Add NodeDocCollectors to each level of test collectors:

        * Function
        * Class
        * Module
        * Session (note: session keeps track of the sub-collectors for output at end of
        test session)
    """
    yield
    # Note: we shouldn't need to modify the item list, but we should
    # run *after* list has been pared down.
    for test in items:
        # TBD: not completely sure if this is correct call
        test_doccol = NodeDocCollector(node_name=test.name,
                                       node_doc=test.obj.__doc__,
                                       level="function")
        test._doccol = test_doccol
        doccollect_parent(test)


def pytest_fixture_setup(fixturedef, request):
    """
    We can use this pytest hook to add in fixture doc info into each
    NodeDocCollector
    """
    try:
        doccol = request.node._doccol
        doccol.add_fixture(fixturedef, request.param_index)
    except Exception as exc:
        # TODO: Ignoring exceptions for now, but we should probably handle
        # them more gracefully.
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Add in test results to doc collectors.
    """
    outcome = yield
    res = outcome.get_result()
    doccol = item._doccol
    doccol.add_result(res)


def pytest_sessionstart(session):
    """
    Used to keep track of all doc collectors.
    """
    session.doc_collector = []


def pytest_sessionfinish(session):
    """
    Write out results for each doc collector.
    """
    for doc_collector in session.doc_collectors:
        doc_collector.write(
            os.path.join(session.config.getoption("rst_dir"),
                         doc_collector.node_name + ".rst"))


def pytest_addoption(parser):
    """
    Add in options for generating docs.

    """
    group = parser.getgroup("RST Writer",
                            description="Generates RST documentation for tests")
    group.addoption("--title",
                    help="Title for the Documentation",
                    default="Test Documentation")
    group.addoption("--doc-desc",
                    help="Description for these documented results",
                    dest="doc_desc",
                    default="Test case results")
    group.addoption("--rst-dir",
                    help="Destination directory for the RST documentation",
                    default="_docs",
                    dest="rst_dir")
