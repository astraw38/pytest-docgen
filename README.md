# pytest-docgen
Automatic Test Documentation generator for pytest


## Overview

1. Choose a directory for your documentation
2. Create a conf.py file (as for a regular sphinx project)
3. Create an index.rst
    ```rst

    ==================
    Test Documentation
    ==================

    Test case results

    .. toctree::
       :includehidden:
       :glob:

       *
    ```

4. Run your tests with the ``--rst-dir=path/to/docs``


This will generate rst files from the tests.

## What it does

From a test file setup like this::

```python
    """
    This is the docstring of the Module.
    """
    
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
```

An RST file would be generated on test execution::

```rst
    .. toctree::
       :hidden:
       :includehidden:


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

             self = <test_precons.TestRSABounds object at 0xb4176e0c>, auth_session = 0

                 def test_bad_modulus_failing(self, auth_session):
                     '''
                     Fail this test, cause I want to see decent output.
                     '''
             >       assert "False" == "This isn't really false"
             E       assert 'False' == "This isn't really false"
             E         - False
             E         + This isn't really false

             CC/test_precons.py:42: AssertionError
```


## Todos

1. Possibly store captured logs that can be downloaded on a per-test basis
2. Better config options:
    * Autogenerate index.rst?
    * Generated RST options (maybe module name slicing)
3. Skip information
