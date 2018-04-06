"""


 A bonus option would be to have a link to captured logs for a given test. Should we store it for all
 tests or just failed/skipped? not sure. I think all should be an option.

"""
import os
from collections import OrderedDict

import pytest
import inspect

import shutil

import re
from _pytest.main import Session
from _pytest.python import Instance
from os import path
from rstcloth.rstcloth import RstCloth

# There are 4 levels we care about
# Level 0 ::    session     :: =====
# Level 1 ::    module      :: ------
# Level 2 ::    class       :: ~~~~~~
# Level 3 ::    function    :: ++++++
from tabulate import tabulate

SESSION_HEADER_MAP = {
    "session": "h1",
    "module": "h2",
    "class": "h3",
    "function": "h4"
}
RESULTS_HEADER = ['Test Name', 'Setup', "Call", "Teardown"]


def _pop_top_dir(path):
    return os.path.join(*(path.split(os.path.sep)[1:]))


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
    indented_docs = [x[min_indent:] for x in doclines]
    # Remove leading and trailing 'empty lines'.
    # this is to ensure we *always* have same data format coming into the doc writer.
    # It's important for sorting out RST spacing.
    if not indented_docs[0] or indented_docs[0].isspace():
        indented_docs.pop(0)
    if not indented_docs[-1] or indented_docs[-1].isspace():
        indented_docs.pop(-1)
    return indented_docs


class NodeDocCollector(object):
    def __init__(self,
                 node_name,
                 node_doc,
                 node_id,
                 level="session",
                 write_toc=False,
                 source_file=None,
                 source_obj=None,
                 log_location=None):
        cut_dir = pytest.config.getoption("rst_cut_dir")
        if cut_dir:
            rex = re.compile(r"^{}[.\\/]".format(cut_dir))
            node_name = rex.sub("", node_name, 1)
            node_id = rex.sub("", node_id, 1)

        self.node_id = node_id.replace(":", "_")
        self.node_name = node_name
        self.node_doc = node_doc
        self.write_toc = write_toc
        self.source_file = source_file
        self.source_obj = source_obj
        self.write_logs = level == "function"
        # Children should be a list of NodeDocCollectors of a smaller level.
        # Can be chained on down.
        self.children = []
        self._fixtures = []
        self._results = []
        self.level = level

        self.log_location = path.splitext(log_location)[0] if log_location else None
        self.log_data = OrderedDict()
        self.capture_start = 0
        self.capture_end = 0
        if log_location:
            log_dir = os.path.dirname(self.log_location)
            os.makedirs(log_dir, exist_ok=True)

    def __str__(self):
        return "NodeDocCollector(name=%s, level=%s, children=%d)" % (self.node_name, self.level, len(self.children))

    def _build_toc(self, rst):
        rst.directive(name="toctree",
                      fields=[('hidden', ''),
                              ('includehidden', '')])
        rst.newline()

        rst.directive(name="contents")
        rst.newline(2)

    def _build_fixtures(self, rst):
        rst.directive(name="topic",
                      arg="{}{} Preconditions".format(self.level[0].upper(), self.level[1:]))
        rst.newline()

        for fixture_name, fixture_doc, fixture_result in self._fixtures:
            rst.definition(name=fixture_name,
                           text="\n".join(fixture_doc),
                           indent=3,
                           wrap=False)  # Note: indent is 3 here so that it shows up under the Fixtures panel.

            if fixture_result:
                rst.content(["", "**Fixture Result Value**:", ""], indent=3)
                rst.codeblock(str(fixture_result),
                              indent=6)  # indent = 6, 3 from fixture panel, 3 from definition
        rst.newline()

    def _build_source_link(self, rst):

        rst.h5("Source Code")
        rst.newline()
        rst.directive("literalinclude",
                      arg=self.source_file,
                      # Just do raw lines. We could do the pyobject though....
                      fields=[("pyobject", self.source_obj)],
                      indent=3)
        rst.newline()

    def _build_results(self, rst):
        res = self.get_simple_results()
        table_results = [[res['setup'], res.get('call', "NOTRUN"), res.get('teardown', "NOTRUN")]]
        rst_table = tabulate(table_results, ["Setup", "Call", "Teardown"],
                             tablefmt="rst")
        rst.h5("Results")
        rst.newline()
        rst._add(rst_table)
        rst.newline()

        for when, outcome in self._results:
            if outcome == "PASSED":
                continue
            else:
                rst.h5("{} Failure Details".format(when))
                rst.codeblock(content=outcome,
                              language="python")
        rst.newline()

    def _build_logs(self, rst):
        rst.h5("Test Output")
        rst.newline()

        for when, data in self.log_data.items():
            rst.content(rst.bold(when))
            rst.newline()
            rst.codeblock(content=data.splitlines(),
                          language="none")
            rst.newline()

        if self.capture_start != self.capture_end:
            rst.content(rst.bold("Captured Output"))
            rst.newline()
            rst.directive("literalinclude",
                          # Note: popping off the top-level directory, as that's the top level rst_dir
                          arg="{}.log".format(_pop_top_dir(self.log_location)),
                          # Just do raw lines. We could do the pyobject though....
                          fields=[("lines", "{}-{}".format(self.capture_start, self.capture_end))],
                          indent=3)
            rst.newline()

    def _build(self):
        """
        Build the RST doc for the current collector.

        :return: rstcloth.rst object.
        """
        rst = RstCloth()
        if self.write_toc:
            self._build_toc(rst)

        # Write ref target with full node ID
        # because test names might not be unique, but full IDs should be.
        rst.ref_target(self.node_id)
        rst.newline()
        getattr(rst, SESSION_HEADER_MAP[self.level])(self.node_name)
        rst.newline()
        rst.content(doc_prep(self.node_doc))
        rst.newline()

        if self._fixtures:
            self._build_fixtures(rst)

        if self._results:
            self._build_results(rst)

        if self.write_logs:
            self._build_logs(rst)

        if self.source_file:
            self._build_source_link(rst)

        for subdoc in self.children:
            rst._add(subdoc.emit())
            rst.newline(2)
        return rst

    def emit(self):
        """
        Return internal *raw-string* representation of this node's rst doc
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

    def add_fixture(self, fixturedef, param_index=0, result=None):
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
        fixture_info = (fixturedef.argname, doc_prep(doc), result)
        if fixture_info not in self._fixtures:
            self._fixtures.append(fixture_info)

    # Logging notes:
    # caplog doesn't always work with get_records. I assume it's order of ops, since i'm kind of creating the fixture
    # as needed. I should probably copy some of the internal stuff instead.
    #
    # Caplog != captured stdout/stderr. Caplog is specifically for LOGGING output.
    #
    # Captured stdout/stderr seems to accumulate across the setup/call/teardown. This means you can't just
    # grab the result.stdout/stderr at the given test point. It should only be done probably once-per test.

    def add_logdata(self, log_data, when):
        if log_data:
            self.log_data[when] = log_data

    def add_capture(self, capstdout=None, capstderr=None):
        # Todo: sort out whether the result stdout capture cares about the when.
        # It looks like it should only be done once, thus the check for teardown.

        # Module or Class DocCollectors don't have a log location set, however they
        # *also* don't have a result to add. So this is safe... for now.
        with open("{}.log".format(self.log_location), "a+") as log:
            # Seek to end of file.
            log.seek(0)
            self.capture_start = log.read().count("\n") + 1
            self.capture_end = self.capture_start
            if capstdout:
                log.write("{0} Captured stdout {0}\n".format("=" * 20))
                log.write(capstdout)
                log.write("{0} End stdout {0}\n".format("=" * 20))
                self.capture_end += capstdout.count('\n') + 1
            if capstderr:
                log.write("{0} Captured stdout {0}\n".format("=" * 20))
                log.write(capstderr)
                log.write("{0} End stdout {0}\n".format("=" * 20))
                self.capture_end += capstderr.count('\n') + 1

    def add_result(self, result):
        """
        Add a test result to the documentation.

        This will be called 3x for each test -- 1x for setup, 1x for call, 1x for teardown.

        :param result: Pytest result object
        """
        if result.outcome != "passed":
            # Store the longrepr
            # TODO: This might need to do some munging on the data.
            outcome = ["".join(["   ", x]) for x in result.longreprtext.split('\n')]
        else:
            outcome = result.outcome.upper()

        self._results.append((result.when, outcome))

    def get_all_results(self):
        all_results = []
        local_result = self.get_simple_results()
        if local_result:
            all_results.append(self.get_simple_results())
        for x in self.children:
            all_results.extend(x.get_all_results())
        return all_results

    def get_simple_results(self):
        """
        Get a simple representation of the results. This should NOT include longrepr or repr of the failure.

        :return:
        """
        # thie should ideally call any sub-collectors... right?
        # We want the node name to also include a link ideally.
        if self._results:
            results = {'name': ':ref:`{} <{}>`'.format(self.node_name, self.node_id)}
            for when, outcome in self._results:
                simple_outcome = "".join(outcome)
                if "PASSED" in simple_outcome:
                    simple_outcome = "|passed|"
                else:
                    simple_outcome = "|failed|"
                results[when] = simple_outcome
            return results
        else:
            return None


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

    This is a recursive call.

    This is initially called on a test Function. If the test is at the module level,
    then its parent will be a Module, and it's parent the Session. If the test is in a class, the structure will look
    like::

        Function
        Instance
        Class
        Module
        Session

    We skip Instance, since it should have no difference in content than the Class.

    Because there can be multiple test Functions under one Class or Module (or Classes under a Module, etc),
    when we step up a level, we check to see if there is already a pre-existing DocCollector.

    If there is a pre-existing parent DocCollector, we will append the *current* DocCollector as a child of the parent.
    This ensures that structure of the final documents is correct.

    Sample final structure::

        Session
            Module1
                Function
                Class
                    Function
                Class
                    Function
                    Function
            Module2
                Class
                    Function
                    Function
                    Function
    """
    if not prev_item:
        prev_item = item
    if isinstance(item.parent, Session):
        # End recursion -- we hit the top level
        if prev_item._doccol not in item.parent.doc_collectors:
            item.parent.doc_collectors.append(prev_item._doccol)
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
                                  parent.nodeid,
                                  level=level,
                                  write_toc=level == "module", )
        parent._doccol = doccol

    if prev_item._doccol not in doccol.children:
        doccol.children.append(prev_item._doccol)
    doccollect_parent(parent)


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(session, config, items):
    """
    Add NodeDocCollectors to each level of test collectors:

        * Function
        * Class
        * Module
        * Session (note: session keeps track of the sub-collectors for output at end of
        test session)
    """
    yield
    if config.getoption("rst_dir"):
        # Note: we shouldn't need to modify the item list, but we should
        # run *after* list has been pared down.
        for test in items:
            # TBD: not completely sure if this is correct call
            if test.cls:
                prefix = test.cls.__name__ + "."
            else:
                prefix = ""
            test_doccol = NodeDocCollector(node_name=test.name,
                                           node_doc=test.obj.__doc__,
                                           node_id=test.nodeid,
                                           level="function",
                                           source_file=path.relpath(str(test.fspath),
                                                                    test.session.config.getoption("rst_dir")),
                                           source_obj="{}{}".format(prefix, test.obj.__name__),
                                           # Log location right now is **directory printing_tests**.
                                           # That's because we use the test.location, which is a direct path to the
                                           # test file from the test root.
                                           # This could be changed to be a flat structure if we wanted.
                                           log_location=path.join(test.session.config.getoption("rst_dir"),
                                                                  "logs",
                                                                  test.location[0].replace('.py', '.log')))
            test._doccol = test_doccol
            doccollect_parent(test)


@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    """
    We can use this pytest hook to add in fixture doc info into each
    NodeDocCollector
    """
    outcome = yield
    res = None
    if request.config.getoption("rst_dir"):
        if request.config.getoption("rst_fixture_results", None) or getattr(fixturedef.func, "_doc_result", False):
            # Note: force the result to be a string. We don't want to be keeping around possibly very large
            # objects that might be returned by fixtures. Also it ensures that we capture the state of the fixture
            # *now* after setup is done, rather than what it might be at the time of the doc generation (end of test run)
            res = str(outcome.get_result())
        try:
            doccol = request.node._doccol
            doccol.add_fixture(fixturedef, request.param_index, outcome.result)
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
    if item.session.config.getoption("rst_dir"):
        res = outcome.get_result()
        doccol = item._doccol
        doccol.add_result(res)
        if res.when == "teardown":
            doccol.add_capture(capstdout=res.capstdout,
                               capstderr=res.capstderr)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    yield
    if item.session.config.getoption("rst_dir"):
        item._doccol.add_logdata(item.catch_log_handler.stream.getvalue(),
                                 'setup')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    yield
    if item.session.config.getoption("rst_dir"):
        item._doccol.add_logdata(item.catch_log_handler.stream.getvalue(),
                                 'call')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    yield
    if item.session.config.getoption("rst_dir"):
        item._doccol.add_logdata(item.catch_log_handler.stream.getvalue(),
                                 'teardown')


def pytest_sessionstart(session):
    """
    Used to keep track of all doc collectors.
    """
    if session.config.getoption("rst_dir"):
        session.doc_collectors = []


def pytest_sessionfinish(session):
    """
    Write out results for each doc collector.
    """
    if session.config.getoption("rst_dir"):
        if session.config.getoption("rst_write_index"):
            index = RstCloth()
            index.title(session.config.getoption("rst_title", "Test Results"))
            index.newline()
            index.content(session.config.getoption("rst_desc", ""))
            index.newline()
            index.directive(name="toctree",
                            fields=[("includehidden", ""), ("glob", "")])
            index.newline()
            index.content(["*"], 3)
            index.newline(2)

        results = []

        for doc_collector in getattr(session, "doc_collectors", []):
            results.extend(doc_collector.get_all_results())
            doc_collector.write(
                os.path.join(session.config.getoption("rst_dir"),
                             doc_collector.node_name + ".rst"))

        # Writes the Overview.rst file.
        result_rst = RstCloth()
        result_rst.title("Test Result Table")
        result_rst.newline()
        result_rst._add(tabulate([(x['name'], x['setup'], x.get('call', "NOTRUN"), x.get('teardown', "NOTRUN"))
                                  for x in results],
                                 headers=RESULTS_HEADER,
                                 tablefmt='rst'))
        result_rst.newline(2)
        result_rst.write(os.path.join(session.config.getoption("rst_dir"),
                                      "overview.rst"))

        # Todo: Write a test log data rst.
        # Theoretically, this should let us put it as an appendix in Latext. Having it generate
        # single RST files like overview & logdata will allow users (aka me) to customize how the generated TOC
        # and such is done.


def pytest_addoption(parser):
    """
    Add in options for generating docs.

    """
    group = parser.getgroup("RST Writer",
                            description="RST documentation generator options")
    group.addoption("--rst-write-index",
                    help="Write an RST index.rst file",
                    action="store_true",
                    default=False, )
    group.addoption("--rst-title",
                    help="RST Document Title",
                    default="Test Documentation",
                    dest="rst_title")
    group.addoption("--rst-desc",
                    help="RST Document description",
                    dest="rst_desc",
                    default="Test case results")
    group.addoption("--rst-dir",
                    help="Destination directory for generated RST documentation",
                    default="_docs",
                    dest="rst_dir")
    group.addoption("--rst-fixture-results",
                    help="Force writing of the value of fixture results to the generated RST documentation. Note: this "
                         "can be enabled on a per-fixture bases with the `@doc_result` decorator",
                    dest="rst_fixture_results",
                    action="store_true",
                    default=True)
    group.addoption("--rst-include-src",
                    help="Include source code for the test itself.",
                    action="store_true",
                    default=True)
    group.addoption("--rst-cut-dir",
                    dest="rst_cut_dir",
                    help="Trim document node names",
                    action="store")


def pytest_configure(config):
    if config.getoption("rst_dir"):
        if os.path.exists(path.join(config.getoption('rst_dir'), "logs")):
            shutil.rmtree(path.join(config.getoption('rst_dir'), "logs"))


def doc_result(fixture):
    """
    Function decorator applied to a fixture that will force the result of a fixture
    to be written to the doc generator.
    """
    fixture._doc_result = True
    return fixture
