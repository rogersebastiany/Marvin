# Pytest — getting started, fixtures, parametrize, assertions


---

## 1. How to write and report assertions in tests

## Asserting with the `assert` statement

`pytest` allows you to use the standard Python `assert` for verifying
expectations and values in Python tests. For example, you can write the
following:

```
# content of test_assert1.py
deff():
    return 3

deftest_function():
    assert f() == 4
```

to assert that your function returns a certain value. If this assertion fails
you will see the return value of the function call:

```
$ pytest test_assert1.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_assert1.py F                                                    [100%]

================================= FAILURES =================================
______________________________ test_function _______________________________

    def test_function():
>       assert f() == 4
E       assert 3 == 4
E        +  where 3 = f()

test_assert1.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_assert1.py::test_function - assert 3 == 4
============================ 1 failed in 0.12s =============================
```

`pytest` has support for showing the values of the most common subexpressions
including calls, attributes, comparisons, and binary and unary
operators. (See [Demo of Python failure reports with pytest](../example/reportingdemo.html#tbreportdemo)). This allows you to use the
idiomatic python constructs without boilerplate code while not losing
introspection information.

If a message is specified with the assertion like this:

```
assert a % 2 == 0, "value was odd, should be even"
```

it is printed alongside the assertion introspection in the traceback.

See [Assertion introspection details](#assert-details) for more information on assertion introspection.

## Assertions about approximate equality

When comparing floating point values (or arrays of floats), small rounding
errors are common. Instead of using `assert abs(a - b) < tol` or
`numpy.isclose`, you can use [`pytest.approx()`](../reference/reference.html#pytest.approx "pytest.approx"):

```
importpytest
importnumpyasnp

deftest_floats():
    assert (0.1 + 0.2) == pytest.approx(0.3)

deftest_arrays():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([0.9999, 2.0001, 3.0])
    assert a == pytest.approx(b)
```

`pytest.approx` works with scalars, lists, dictionaries, and NumPy arrays.
It also supports comparisons involving NaNs.

See [`pytest.approx()`](../reference/reference.html#pytest.approx "pytest.approx") for details.

## Assertions about expected exceptions

In order to write assertions about raised exceptions, you can use
[`pytest.raises()`](../reference/reference.html#pytest.raises "pytest.raises") as a context manager like this:

```
importpytest

deftest_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

and if you need to have access to the actual exception info you may use:

```
deftest_recursion_depth():
    with pytest.raises(RuntimeError) as excinfo:

        deff():
            f()

        f()
    assert "maximum recursion" in str(excinfo.value)
```

`excinfo` is an [`ExceptionInfo`](../reference/reference.html#pytest.ExceptionInfo "pytest.ExceptionInfo") instance, which is a wrapper around
the actual exception raised. The main attributes of interest are
`.type`, `.value` and `.traceback`.

Note that `pytest.raises` will match the exception type or any subclasses (like the standard `except` statement).
If you want to check if a block of code is raising an exact exception type, you need to check that explicitly:

```
deftest_foo_not_implemented():
    deffoo():
        raise NotImplementedError

    with pytest.raises(RuntimeError) as excinfo:
        foo()
    assert excinfo.type is RuntimeError
```

The [`pytest.raises()`](../reference/reference.html#pytest.raises "pytest.raises") call will succeed, even though the function raises [`NotImplementedError`](https://docs.python.org/3/library/exceptions.html#NotImplementedError "(in Python v3.14)"), because
[`NotImplementedError`](https://docs.python.org/3/library/exceptions.html#NotImplementedError "(in Python v3.14)") is a subclass of [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)"); however the following `assert` statement will
catch the problem.

### Matching exception messages

You can pass a `match` keyword parameter to the context-manager to test
that a regular expression matches on the string representation of an exception
(similar to the `TestCase.assertRaisesRegex` method from `unittest`):

```
importpytest

defmyfunc():
    raise ValueError("Exception 123 raised")

deftest_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()
```

Notes:

* The `match` parameter is matched with the [`re.search()`](https://docs.python.org/3/library/re.html#re.search "(in Python v3.14)")
  function, so in the above example `match='123'` would have worked as well.
* The `match` parameter also matches against [PEP-678](https://peps.python.org/pep-0678/) `__notes__`.

### Assertions about expected exception groups

When expecting a [`BaseExceptionGroup`](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup "(in Python v3.14)") or [`ExceptionGroup`](https://docs.python.org/3/library/exceptions.html#ExceptionGroup "(in Python v3.14)") you can use [`pytest.RaisesGroup`](../reference/reference.html#pytest.RaisesGroup "pytest.RaisesGroup"):

```
deftest_exception_in_group():
    with pytest.RaisesGroup(ValueError):
        raise ExceptionGroup("group msg", [ValueError("value msg")])
    with pytest.RaisesGroup(ValueError, TypeError):
        raise ExceptionGroup("msg", [ValueError("foo"), TypeError("bar")])
```

It accepts a `match` parameter, that checks against the group message, and a `check` parameter that takes an arbitrary callable which it passes the group to, and only succeeds if the callable returns `True`.

```
deftest_raisesgroup_match_and_check():
    with pytest.RaisesGroup(BaseException, match="my group msg"):
        raise BaseExceptionGroup("my group msg", [KeyboardInterrupt()])
    with pytest.RaisesGroup(
        Exception, check=lambda eg: isinstance(eg.__cause__, ValueError)
    ):
        raise ExceptionGroup("", [TypeError()]) fromValueError()
```

It is strict about structure and unwrapped exceptions, unlike [except\*](https://docs.python.org/3/reference/compound_stmts.html#except-star "(in Python v3.14)"), so you might want to set the `flatten_subgroups` and/or `allow_unwrapped` parameters.

```
deftest_structure():
    with pytest.RaisesGroup(pytest.RaisesGroup(ValueError)):
        raise ExceptionGroup("", (ExceptionGroup("", (ValueError(),)),))
    with pytest.RaisesGroup(ValueError, flatten_subgroups=True):
        raise ExceptionGroup("1st group", [ExceptionGroup("2nd group", [ValueError()])])
    with pytest.RaisesGroup(ValueError, allow_unwrapped=True):
        raise ValueError
```

To specify more details about the contained exception you can use [`pytest.RaisesExc`](../reference/reference.html#pytest.RaisesExc "pytest.RaisesExc")

```
deftest_raises_exc():
    with pytest.RaisesGroup(pytest.RaisesExc(ValueError, match="foo")):
        raise ExceptionGroup("", (ValueError("foo")))
```

They both supply a method [`pytest.RaisesGroup.matches()`](../reference/reference.html#pytest.RaisesGroup.matches "pytest.RaisesGroup.matches") [`pytest.RaisesExc.matches()`](../reference/reference.html#pytest.RaisesExc.matches "pytest.RaisesExc.matches") if you want to do matching outside of using it as a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers "(in Python v3.14)"). This can be helpful when checking `.__context__` or `.__cause__`.

```
deftest_matches():
    exc = ValueError()
    exc_group = ExceptionGroup("", [exc])
    if RaisesGroup(ValueError).matches(exc_group):
        ...
    # helpful error is available in `.fail_reason` if it fails to match
    r = RaisesExc(ValueError)
    assert r.matches(e), r.fail_reason
```

Check the documentation on [`pytest.RaisesGroup`](../reference/reference.html#pytest.RaisesGroup "pytest.RaisesGroup") and [`pytest.RaisesExc`](../reference/reference.html#pytest.RaisesExc "pytest.RaisesExc") for more details and examples.

### `ExceptionInfo.group_contains()`

Warning

This helper makes it easy to check for the presence of specific exceptions, but it is very bad for checking that the group does *not* contain *any other exceptions*. So this will pass:

> ```
> classEXTREMELYBADERROR(BaseException):
> """This is a very bad error to miss"""
>
>
> deftest_for_value_error():
>     with pytest.raises(ExceptionGroup) as excinfo:
>         excs = [ValueError()]
>         if very_unlucky():
>             excs.append(EXTREMELYBADERROR())
>         raise ExceptionGroup("", excs)
>     # This passes regardless of if there's other exceptions.
>     assert excinfo.group_contains(ValueError)
>     # You can't simply list all exceptions you *don't* want to get here.
> ```

There is no good way of using [`excinfo.group_contains()`](../reference/reference.html#pytest.ExceptionInfo.group_contains "pytest.ExceptionInfo.group_contains") to ensure you’re not getting *any* other exceptions than the one you expected.
You should instead use [`pytest.RaisesGroup`](../reference/reference.html#pytest.RaisesGroup "pytest.RaisesGroup"), see [Assertions about expected exception groups](#assert-matching-exception-groups).

You can also use the [`excinfo.group_contains()`](../reference/reference.html#pytest.ExceptionInfo.group_contains "pytest.ExceptionInfo.group_contains")
method to test for exceptions returned as part of an [`ExceptionGroup`](https://docs.python.org/3/library/exceptions.html#ExceptionGroup "(in Python v3.14)"):

```
deftest_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        raise ExceptionGroup(
            "Group message",
            [
                RuntimeError("Exception 123 raised"),
            ],
        )
    assert excinfo.group_contains(RuntimeError, match=r".* 123 .*")
    assert not excinfo.group_contains(TypeError)
```

The optional `match` keyword parameter works the same way as for
[`pytest.raises()`](../reference/reference.html#pytest.raises "pytest.raises").

By default `group_contains()` will recursively search for a matching
exception at any level of nested `ExceptionGroup` instances. You can
specify a `depth` keyword parameter if you only want to match an
exception at a specific level; exceptions contained directly in the top
`ExceptionGroup` would match `depth=1`.

```
deftest_exception_in_group_at_given_depth():
    with pytest.raises(ExceptionGroup) as excinfo:
        raise ExceptionGroup(
            "Group message",
            [
                RuntimeError(),
                ExceptionGroup(
                    "Nested group",
                    [
                        TypeError(),
                    ],
                ),
            ],
        )
    assert excinfo.group_contains(RuntimeError, depth=1)
    assert excinfo.group_contains(TypeError, depth=2)
    assert not excinfo.group_contains(RuntimeError, depth=2)
    assert not excinfo.group_contains(TypeError, depth=1)
```

### Alternate `pytest.raises` form (legacy)

There is an alternate form of [`pytest.raises()`](../reference/reference.html#pytest.raises "pytest.raises") where you pass
a function that will be executed, along with `*args` and `**kwargs`. [`pytest.raises()`](../reference/reference.html#pytest.raises "pytest.raises")
will then execute the function with those arguments and assert that the given exception is raised:

```
deffunc(x):
    if x <= 0:
        raise ValueError("x needs to be larger than zero")

pytest.raises(ValueError, func, x=-1)
```

The reporter will provide you with helpful output in case of failures such as *no
exception* or *wrong exception*.

This form was the original [`pytest.raises()`](../reference/reference.html#pytest.raises "pytest.raises") API, developed before the `with` statement was
added to the Python language. Nowadays, this form is rarely used, with the context-manager form (using `with`)
being considered more readable.
Nonetheless, this form is fully supported and not deprecated in any way.

### xfail mark and pytest.raises

It is also possible to specify a `raises` argument to
[pytest.mark.xfail](../reference/reference.html#pytest-mark-xfail-ref), which checks that the test is failing in a more
specific way than just having any exception raised:

```
deff():
    raise IndexError()

@pytest.mark.xfail(raises=IndexError)
deftest_f():
    f()
```

This will only “xfail” if the test fails by raising `IndexError` or subclasses.

* Using [pytest.mark.xfail](../reference/reference.html#pytest-mark-xfail-ref) with the `raises` parameter is probably better for something
  like documenting unfixed bugs (where the test describes what “should” happen) or bugs in dependencies.
* Using [`pytest.raises()`](../reference/reference.html#pytest.raises "pytest.raises") is likely to be better for cases where you are
  testing exceptions your own code is deliberately raising, which is the majority of cases.

You can also use [`pytest.RaisesGroup`](../reference/reference.html#pytest.RaisesGroup "pytest.RaisesGroup"):

```
deff():
    raise ExceptionGroup("", [IndexError()])

@pytest.mark.xfail(raises=RaisesGroup(IndexError))
deftest_f():
    f()
```

## Assertions about expected warnings

You can check that code raises a particular warning using
[pytest.warns](capture-warnings.html#warns).

## Making use of context-sensitive comparisons

`pytest` has rich support for providing context-sensitive information
when it encounters comparisons. For example:

```
# content of test_assert2.py
deftest_set_comparison():
    set1 = set("1308")
    set2 = set("8035")
    assert set1 == set2
```

if you run this module:

```
$ pytest test_assert2.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_assert2.py F                                                    [100%]

================================= FAILURES =================================
___________________________ test_set_comparison ____________________________

    def test_set_comparison():
        set1 = set("1308")
        set2 = set("8035")
>       assert set1 == set2
E       AssertionError: assert {'0', '1', '3', '8'} == {'0', '3', '5', '8'}
E
E         Extra items in the left set:
E         '1'
E         Extra items in the right set:
E         '5'
E         Use -v to get more diff

test_assert2.py:4: AssertionError
========================= short test summary info ==========================
FAILED test_assert2.py::test_set_comparison - AssertionError: assert {'0'...
============================ 1 failed in 0.12s =============================
```

Special comparisons are done for a number of cases:

* comparing long strings: a context diff is shown
* comparing long sequences: first failing indices
* comparing dicts: different entries

In string context diffs, lines prefixed with `-` come from the left-hand side
of `assert left == right`, while lines prefixed with `+` come from the
right-hand side.

See the [reporting demo](../example/reportingdemo.html#tbreportdemo) for many more examples.

## Defining your own explanation for failed assertions

It is possible to add your own detailed explanations by implementing
the `pytest_assertrepr_compare` hook.

pytest\_assertrepr\_compare(*config*, *op*, *left*, *right*)[[source]](../_modules/_pytest/hookspec.html#pytest_assertrepr_compare)
:   Return explanation for comparisons in failing assert expressions.

    Return None for no custom explanation, otherwise return a list
    of strings. The strings will be joined by newlines but any newlines
    *in* a string will be escaped. Note that all but the first line will
    be indented slightly, the intention is for the first line to be a summary.

    Parameters:
    :   * **config** ([*Config*](../reference/reference.html#pytest.Config "pytest.Config")) – The pytest config object.
        * **op** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The operator, e.g. `"=="`, `"!="`, `"not in"`.
        * **left** ([*object*](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")) – The left operand.
        * **right** ([*object*](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")) – The right operand.

    ### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item’s directory and its parent directories are consulted.

As an example consider adding the following hook in a [conftest.py](../reference/fixtures.html#conftest-py)
file which provides an alternative explanation for `Foo` objects:

```
# content of conftest.py
fromtest_foocompareimport Foo

defpytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "Comparing Foo instances:",
            f"   vals: {left.val} != {right.val}",
        ]
```

now, given this test module:

```
# content of test_foocompare.py
classFoo:
    def__init__(self, val):
        self.val = val

    def__eq__(self, other):
        return self.val == other.val

deftest_compare():
    f1 = Foo(1)
    f2 = Foo(2)
    assert f1 == f2
```

you can run the test module and get the custom output defined in
the conftest file:

```
$ pytest -q test_foocompare.py
F                                                                    [100%]
================================= FAILURES =================================
_______________________________ test_compare _______________________________

    def test_compare():
        f1 = Foo(1)
        f2 = Foo(2)
>       assert f1 == f2
E       assert Comparing Foo instances:
E            vals: 1 != 2

test_foocompare.py:12: AssertionError
========================= short test summary info ==========================
FAILED test_foocompare.py::test_compare - assert Comparing Foo instances:
1 failed in 0.12s
```

## Returning non-None value in test functions

A [`pytest.PytestReturnNotNoneWarning`](../reference/reference.html#pytest.PytestReturnNotNoneWarning "pytest.PytestReturnNotNoneWarning") is emitted when a test function returns a value other than `None`.

This helps prevent a common mistake made by beginners who assume that returning a `bool` (e.g., `True` or `False`) will determine whether a test passes or fails.

Example:

```
@pytest.mark.parametrize(
    ["a", "b", "result"],
    [
        [1, 2, 5],
        [2, 3, 8],
        [5, 3, 18],
    ],
)
deftest_foo(a, b, result):
    return foo(a, b) == result  # Incorrect usage, do not do this.
```

Since pytest ignores return values, it might be surprising that the test will never fail based on the returned value.

The correct fix is to replace the `return` statement with an `assert`:

```
@pytest.mark.parametrize(
    ["a", "b", "result"],
    [
        [1, 2, 5],
        [2, 3, 8],
        [5, 3, 18],
    ],
)
deftest_foo(a, b, result):
    assert foo(a, b) == result
```

## Assertion introspection details

Reporting details about a failing assertion is achieved by rewriting assert
statements before they are run. Rewritten assert statements put introspection
information into the assertion failure message. `pytest` only rewrites test
modules directly discovered by its test collection process, so **asserts in
supporting modules which are not themselves test modules will not be rewritten**.

You can manually enable assertion rewriting for an imported module by calling
[register\_assert\_rewrite](writing_plugins.html#assertion-rewriting)
before you import it (a good place to do that is in your root `conftest.py`).

For further information, Benjamin Peterson wrote up [Behind the scenes of pytest’s new assertion rewriting](http://pybites.blogspot.com/2011/07/behind-scenes-of-pytests-new-assertion.html).

### Assertion rewriting caches files on disk

`pytest` will write back the rewritten modules to disk for caching. You can disable
this behavior (for example to avoid leaving stale `.pyc` files around in projects that
move files around a lot) by adding this to the top of your `conftest.py` file:

```
importsys

sys.dont_write_bytecode = True
```

Note that you still get the benefits of assertion introspection, the only change is that
the `.pyc` files won’t be cached on disk.

Additionally, rewriting will silently skip caching if it cannot write new `.pyc` files,
e.g. in a read-only filesystem or a zipfile.

### Disabling assert rewriting

`pytest` rewrites test modules on import by using an import
hook to write new `pyc` files. Most of the time this works transparently.
However, if you are working with the import machinery yourself, the import hook may
interfere.

If this is the case you have two options:

* Disable rewriting for a specific module by adding the string
  `PYTEST_DONT_REWRITE` to its docstring.
* Disable rewriting for all modules by using [`--assert=plain`](../reference/reference.html#cmdoption-assert).

---

## 2. Get Started

## Install `pytest`

1. Run the following command in your command line:

```
pipinstall-Upytest
```

2. Check that you installed the correct version:

```
$pytest--version
pytest9.0.3
```

## Create your first test

Create a new file called `test_sample.py`, containing a function, and a test:

```
# content of test_sample.py
deffunc(x):
    return x + 1

deftest_answer():
    assert func(3) == 5
```

The test

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_sample.py::test_answer - assert 4 == 5
============================ 1 failed in 0.12s =============================
```

The `[100%]` refers to the overall progress of running all test cases. After it finishes, pytest then shows a failure report because `func(3)` does not return `5`.

Note

You can use the `assert` statement to verify test expectations. pytest’s [Advanced assertion introspection](https://docs.python.org/3/reference/simple_stmts.html#assert "(in Python v3.14)") will intelligently report intermediate values of the assert expression so you can avoid the many names [of JUnit legacy methods](https://docs.python.org/3/library/unittest.html#testcase-objects "(in Python v3.14)").

## Run multiple tests

`pytest` will run all files of the form `test_*.py` or `*_test.py` in the current directory and its subdirectories. More generally, it follows [standard test discovery rules](explanation/goodpractices.html#test-discovery).

## Assert that a certain exception is raised

Use the [raises](how-to/assert.html#assertraises) helper to assert that some code raises an exception:

```
# content of test_sysexit.py
importpytest

deff():
    raise SystemExit(1)

deftest_mytest():
    with pytest.raises(SystemExit):
        f()
```

Execute the test function with “quiet” reporting mode:

```
$ pytest -q test_sysexit.py
.                                                                    [100%]
1 passed in 0.12s
```

Note

The `-q/--quiet` flag keeps the output brief in this and following examples.

See [Assertions about approximate equality](how-to/assert.html#assertraises) for specifying more details about the expected exception.

## Group multiple tests in a class

Once you develop multiple tests, you may want to group them into a class. pytest makes it easy to create a class containing more than one test:

```
# content of test_class.py
classTestClass:
    deftest_one(self):
        x = "this"
        assert "h" in x

    deftest_two(self):
        x = "hello"
        assert hasattr(x, "check")
```

`pytest` discovers all tests following its [Conventions for Python test discovery](explanation/goodpractices.html#test-discovery), so it finds both `test_` prefixed functions. There is no need to subclass anything, but make sure to prefix your class with `Test` otherwise the class will be skipped. We can simply run the module by passing its filename:

```
$ pytest -q test_class.py
.F                                                                   [100%]
================================= FAILURES =================================
____________________________ TestClass.test_two ____________________________

self = <test_class.TestClass object at 0xdeadbeef0001>

    def test_two(self):
        x = "hello"
>       assert hasattr(x, "check")
E       AssertionError: assert False
E        +  where False = hasattr('hello', 'check')

test_class.py:8: AssertionError
========================= short test summary info ==========================
FAILED test_class.py::TestClass::test_two - AssertionError: assert False
1 failed, 1 passed in 0.12s
```

The first test passed and the second failed. You can easily see the intermediate values in the assertion to help you understand the reason for the failure.

Grouping tests in classes can be beneficial for the following reasons:

> * Test organization
> * Sharing fixtures for tests only in that particular class
> * Applying marks at the class level and having them implicitly apply to all tests

Something to be aware of when grouping tests inside classes is that each test has a unique instance of the class.
Having each test share the same class instance would be very detrimental to test isolation and would promote poor test practices.
This is outlined below:

```
# content of test_class_demo.py
classTestClassDemoInstance:
    value = 0

    deftest_one(self):
        self.value = 1
        assert self.value == 1

    deftest_two(self):
        assert self.value == 1
```

```
$ pytest -k TestClassDemoInstance -q
.F                                                                   [100%]
================================= FAILURES =================================
______________________ TestClassDemoInstance.test_two ______________________

self = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>

    def test_two(self):
>       assert self.value == 1
E       assert 0 == 1
E        +  where 0 = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>.value

test_class_demo.py:9: AssertionError
========================= short test summary info ==========================
FAILED test_class_demo.py::TestClassDemoInstance::test_two - assert 0 == 1
1 failed, 1 passed in 0.12s
```

Note that attributes added at class level are *class attributes*, so they will be shared between tests.

## Compare floating-point values with pytest.approx

`pytest` also provides a number of utilities to make writing tests easier.
For example, you can use [`pytest.approx()`](reference/reference.html#pytest.approx "pytest.approx") to compare floating-point
values that may have small rounding errors:

```
# content of test_approx.py
importpytest

deftest_sum():
    assert (0.1 + 0.2) == pytest.approx(0.3)
```

This avoids the need for manual tolerance checks or using
`math.isclose` and works with scalars, lists, and NumPy arrays.

## Request a unique temporary directory for functional tests

`pytest` provides [Builtin fixtures/function arguments](builtin.html) to request arbitrary resources, like a unique temporary directory:

```
# content of test_tmp_path.py
deftest_needsfiles(tmp_path):
    print(tmp_path)
    assert 0
```

List the name `tmp_path` in the test function signature and `pytest` will lookup and call a fixture factory to create the resource before performing the test function call. Before the test runs, `pytest` creates a unique-per-test-invocation temporary directory:

```
$ pytest -q test_tmp_path.py
F                                                                    [100%]
================================= FAILURES =================================
_____________________________ test_needsfiles ______________________________

tmp_path = PosixPath('PYTEST_TMPDIR/test_needsfiles0')

    def test_needsfiles(tmp_path):
        print(tmp_path)
>       assert 0
E       assert 0

test_tmp_path.py:3: AssertionError
--------------------------- Captured stdout call ---------------------------
PYTEST_TMPDIR/test_needsfiles0
========================= short test summary info ==========================
FAILED test_tmp_path.py::test_needsfiles - assert 0
1 failed in 0.12s
```

More info on temporary directory handling is available at [Temporary directories and files](how-to/tmp_path.html#tmp-path-handling).

Find out what kind of builtin [pytest fixtures](reference/fixtures.html#fixtures) exist with the command:

```
pytest--fixtures# shows builtin and custom fixtures
```

Note that this command omits fixtures with leading `_` unless the [`-v`](reference/reference.html#cmdoption-v) option is added.

## Continue reading

Check out additional pytest resources to help you customize tests for your unique workflow:

* “[How to invoke pytest](how-to/usage.html#usage)” for command line invocation examples
* “[How to use pytest with an existing test suite](how-to/existingtestsuite.html#existingtestsuite)” for working with preexisting tests
* “[How to mark test functions with attributes](how-to/mark.html#mark)” for information on the `pytest.mark` mechanism
* “[Fixtures reference](reference/fixtures.html#fixtures)” for providing a functional baseline to your tests
* “[Writing plugins](how-to/writing_plugins.html#plugins)” for managing and writing plugins
* “[Good Integration Practices](explanation/goodpractices.html#goodpractices)” for virtualenv and test layouts

---

## 3. How to parametrize fixtures and test functions

pytest enables test parametrization at several levels:

* [`pytest.fixture()`](../reference/reference.html#pytest.fixture "pytest.fixture") allows one to [parametrize fixture
  functions](fixtures.html#fixture-parametrize).

* [@pytest.mark.parametrize](#pytest-mark-parametrize) allows one to define multiple sets of
  arguments and fixtures at the test function or class.
* [pytest\_generate\_tests](#pytest-generate-tests) allows one to define custom parametrization
  schemes or extensions.

Note

See [How to use subtests](subtests.html#subtests) for an alternative to parametrization.

## `@pytest.mark.parametrize`: parametrizing test functions

The builtin [pytest.mark.parametrize](../reference/reference.html#pytest-mark-parametrize-ref) decorator enables
parametrization of arguments for a test function. Here is a typical example
of a test function that implements checking that a certain input leads
to an expected output:

```
# content of test_expectation.py
importpytest

@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
deftest_eval(test_input, expected):
    assert eval(test_input) == expected
```

Here, the `@parametrize` decorator defines three different `(test_input,expected)`
tuples so that the `test_eval` function will run three times using
them in turn:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_expectation.py ..F                                              [100%]

================================= FAILURES =================================
____________________________ test_eval[6*9-42] _____________________________

test_input = '6*9', expected = 42

    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       AssertionError: assert 54 == 42
E        +  where 54 = eval('6*9')

test_expectation.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_expectation.py::test_eval[6*9-42] - AssertionError: assert 54...
======================= 1 failed, 2 passed in 0.12s ========================
```

Note

Parameter values are passed as-is to tests (no copy whatsoever).

For example, if you pass a list or a dict as a parameter value, and
the test case code mutates it, the mutations will be reflected in subsequent
test case calls.

Note

pytest by default escapes any non-ascii characters used in unicode strings
for the parametrization because it has several downsides.
If however you would like to use unicode strings in parametrization
and see them in the terminal as is (non-escaped), use this option
in your configuration file:

```
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support=true
```

```
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support=true
```

Keep in mind however that this might cause unwanted side effects and
even bugs depending on the OS used and plugins currently installed,
so use it at your own risk.

As designed in this example, only one pair of input/output values fails
the simple test function. And as usual with test function arguments,
you can see the `input` and `output` values in the traceback.

Note that you could also use the parametrize marker on a class or a module
(see [How to mark test functions with attributes](mark.html#mark)) which would invoke several functions with the argument sets,
for instance:

```
importpytest

@pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
classTestClass:
    deftest_simple_case(self, n, expected):
        assert n + 1 == expected

    deftest_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected
```

To parametrize all tests in a module, you can assign to the [`pytestmark`](../reference/reference.html#globalvar-pytestmark) global variable:

```
importpytest

pytestmark = pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])

classTestClass:
    deftest_simple_case(self, n, expected):
        assert n + 1 == expected

    deftest_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected
```

It is also possible to mark individual test instances within parametrize,
for example with the builtin `mark.xfail`:

```
# content of test_expectation.py
importpytest

@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
deftest_eval(test_input, expected):
    assert eval(test_input) == expected
```

Let’s run this:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_expectation.py ..x                                              [100%]

======================= 2 passed, 1 xfailed in 0.12s =======================
```

The one parameter set which caused a failure previously now
shows up as an “xfailed” (expected to fail) test.

In case the values provided to `parametrize` result in an empty list - for
example, if they’re dynamically generated by some function - the behaviour of
pytest is defined by the [`empty_parameter_set_mark`](../reference/reference.html#confval-empty_parameter_set_mark) option.

To get all combinations of multiple parametrized arguments you can stack
`parametrize` decorators:

```
importpytest

@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
deftest_foo(x, y):
    pass
```

This will run the test with the arguments set to `x=0/y=2`, `x=1/y=2`,
`x=0/y=3`, and `x=1/y=3` exhausting parameters in the order of the decorators.

## Basic `pytest_generate_tests` example

Sometimes you may want to implement your own parametrization scheme
or implement some dynamism for determining the parameters or scope
of a fixture. For this, you can use the `pytest_generate_tests` hook
which is called when collecting a test function. Through the passed in
`metafunc` object you can inspect the requesting test context and, most
importantly, you can call `metafunc.parametrize()` to cause
parametrization.

For example, let’s say we want to run a test taking string inputs which
we want to set via a new `pytest` command line option. Let’s first write
a simple test accepting a `stringinput` fixture function argument:

```
# content of test_strings.py

deftest_valid_string(stringinput):
    assert stringinput.isalpha()
```

Now we add a `conftest.py` file containing the addition of a
command line option and the parametrization of our test function:

```
# content of conftest.py

defpytest_addoption(parser):
    parser.addoption(
        "--stringinput",
        action="append",
        default=[],
        help="list of stringinputs to pass to test functions",
    )

defpytest_generate_tests(metafunc):
    if "stringinput" in metafunc.fixturenames:
        metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))
```

Note

The [`pytest_generate_tests`](../reference/reference.html#std-hook-pytest_generate_tests) hook can also be implemented directly in a test
module or inside a test class; unlike other hooks, pytest will discover it there
as well. Other hooks must live in a [conftest.py](writing_plugins.html#localplugin) or a plugin.
See [Writing hook functions](writing_hook_functions.html#writinghooks).

If we now pass two stringinput values, our test will run twice:

```
$ pytest -q --stringinput="hello" --stringinput="world" test_strings.py
..                                                                   [100%]
2 passed in 0.12s
```

Let’s also run with a stringinput that will lead to a failing test:

```
$ pytest -q --stringinput="!" test_strings.py
F                                                                    [100%]
================================= FAILURES =================================
___________________________ test_valid_string[!] ___________________________

stringinput = '!'

    def test_valid_string(stringinput):
>       assert stringinput.isalpha()
E       AssertionError: assert False
E        +  where False = <built-in method isalpha of str object at 0xdeadbeef0001>()
E        +    where <built-in method isalpha of str object at 0xdeadbeef0001> = '!'.isalpha

test_strings.py:4: AssertionError
========================= short test summary info ==========================
FAILED test_strings.py::test_valid_string[!] - AssertionError: assert False
1 failed in 0.12s
```

As expected our test function fails.

If you don’t specify a stringinput it will be skipped because
`metafunc.parametrize()` will be called with an empty parameter
list:

```
$ pytest -q -rs test_strings.py
s                                                                    [100%]
========================= short test summary info ==========================
SKIPPED [1] test_strings.py: got empty parameter set for (stringinput)
1 skipped in 0.12s
```

Note that when calling `metafunc.parametrize` multiple times with different parameter sets, all parameter names across
those sets cannot be duplicated, otherwise an error will be raised.

## More examples

For further examples, you might want to look at [more
parametrization examples](../example/parametrize.html#paramexamples).

---

## 4. How to use fixtures

See also

[About fixtures](../explanation/fixtures.html#about-fixtures)

See also

[Fixtures reference](../reference/fixtures.html#reference-fixtures)

## “Requesting” fixtures

At a basic level, test functions request fixtures they require by declaring
them as arguments.

When pytest goes to run a test, it looks at the parameters in that test
function’s signature, and then searches for fixtures that have the same names as
those parameters. Once pytest finds them, it runs those fixtures, captures what
they returned (if anything), and passes those objects into the test function as
arguments.

### Quick example

```
importpytest

classFruit:
    def__init__(self, name):
        self.name = name
        self.cubed = False

    defcube(self):
        self.cubed = True

classFruitSalad:
    def__init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def_cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()

# Arrange
@pytest.fixture
deffruit_bowl():
    return [Fruit("apple"), Fruit("banana")]

deftest_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)
```

In this example, `test_fruit_salad` “**requests**” `fruit_bowl` (i.e.
`def test_fruit_salad(fruit_bowl):`), and when pytest sees this, it will
execute the `fruit_bowl` fixture function and pass the object it returns into
`test_fruit_salad` as the `fruit_bowl` argument.

Here’s roughly
what’s happening if we were to do it by hand:

```
deffruit_bowl():
    return [Fruit("apple"), Fruit("banana")]

deftest_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)

# Arrange
bowl = fruit_bowl()
test_fruit_salad(fruit_bowl=bowl)
```

### Fixtures can **request** other fixtures

One of pytest’s greatest strengths is its extremely flexible fixture system. It
allows us to boil down complex requirements for tests into more simple and
organized functions, where we only need to have each one describe the things
they are dependent on. We’ll get more into this further down, but for now,
here’s a quick example to demonstrate how fixtures can use other fixtures:

```
# contents of test_append.py
importpytest

# Arrange
@pytest.fixture
deffirst_entry():
    return "a"

# Arrange
@pytest.fixture
deforder(first_entry):
    return [first_entry]

deftest_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]
```

Notice that this is the same example from above, but very little changed. The
fixtures in pytest **request** fixtures just like tests. All the same
**requesting** rules apply to fixtures that do for tests. Here’s how this
example would work if we did it by hand:

```
deffirst_entry():
    return "a"

deforder(first_entry):
    return [first_entry]

deftest_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]

entry = first_entry()
the_list = order(first_entry=entry)
test_string(order=the_list)
```

### Fixtures are reusable

One of the things that makes pytest’s fixture system so powerful, is that it
gives us the ability to define a generic setup step that can be reused over and
over, just like a normal function would be used. Two different tests can request
the same fixture and have pytest give each test their own result from that
fixture.

This is extremely useful for making sure tests aren’t affected by each other. We
can use this system to make sure each test gets its own fresh batch of data and
is starting from a clean state so it can provide consistent, repeatable results.

Here’s an example of how this can come in handy:

```
# contents of test_append.py
importpytest

# Arrange
@pytest.fixture
deffirst_entry():
    return "a"

# Arrange
@pytest.fixture
deforder(first_entry):
    return [first_entry]

deftest_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]

deftest_int(order):
    # Act
    order.append(2)

    # Assert
    assert order == ["a", 2]
```

Each test here is being given its own copy of that `list` object,
which means the `order` fixture is getting executed twice (the same
is true for the `first_entry` fixture). If we were to do this by hand as
well, it would look something like this:

```
deffirst_entry():
    return "a"

deforder(first_entry):
    return [first_entry]

deftest_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]

deftest_int(order):
    # Act
    order.append(2)

    # Assert
    assert order == ["a", 2]

entry = first_entry()
the_list = order(first_entry=entry)
test_string(order=the_list)

entry = first_entry()
the_list = order(first_entry=entry)
test_int(order=the_list)
```

### A test/fixture can **request** more than one fixture at a time

Tests and fixtures aren’t limited to **requesting** a single fixture at a time.
They can request as many as they like. Here’s another quick example to
demonstrate:

```
# contents of test_append.py
importpytest

# Arrange
@pytest.fixture
deffirst_entry():
    return "a"

# Arrange
@pytest.fixture
defsecond_entry():
    return 2

# Arrange
@pytest.fixture
deforder(first_entry, second_entry):
    return [first_entry, second_entry]

# Arrange
@pytest.fixture
defexpected_list():
    return ["a", 2, 3.0]

deftest_string(order, expected_list):
    # Act
    order.append(3.0)

    # Assert
    assert order == expected_list
```

### Fixtures can be **requested** more than once per test (return values are cached)

Fixtures can also be **requested** more than once during the same test, and
pytest won’t execute them again for that test. This means we can **request**
fixtures in multiple fixtures that are dependent on them (and even again in the
test itself) without those fixtures being executed more than once.

```
# contents of test_append.py
importpytest

# Arrange
@pytest.fixture
deffirst_entry():
    return "a"

# Arrange
@pytest.fixture
deforder():
    return []

# Act
@pytest.fixture
defappend_first(order, first_entry):
    return order.append(first_entry)

deftest_string_only(append_first, order, first_entry):
    # Assert
    assert order == [first_entry]
```

If a **requested** fixture was executed once for every time it was **requested**
during a test, then this test would fail because both `append_first` and
`test_string_only` would see `order` as an empty list (i.e. `[]`), but
since the return value of `order` was cached (along with any side effects
executing it may have had) after the first time it was called, both the test and
`append_first` were referencing the same object, and the test saw the effect
`append_first` had on that object.

## Autouse fixtures (fixtures you don’t have to request)

Sometimes you may want to have a fixture (or even several) that you know all
your tests will depend on. “Autouse” fixtures are a convenient way to make all
tests automatically **request** them. This can cut out a
lot of redundant **requests**, and can even provide more advanced fixture usage
(more on that further down).

We can make a fixture an autouse fixture by passing in `autouse=True` to the
fixture’s decorator. Here’s a simple example for how they can be used:

```
# contents of test_append.py
importpytest

@pytest.fixture
deffirst_entry():
    return "a"

@pytest.fixture
deforder(first_entry):
    return []

@pytest.fixture(autouse=True)
defappend_first(order, first_entry):
    return order.append(first_entry)

deftest_string_only(order, first_entry):
    assert order == [first_entry]

deftest_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]
```

In this example, the `append_first` fixture is an autouse fixture. Because it
happens automatically, both tests are affected by it, even though neither test
**requested** it. That doesn’t mean they *can’t* be **requested** though; just
that it isn’t *necessary*.

## Scope: sharing fixtures across classes, modules, packages or session

Fixtures requiring network access depend on connectivity and are
usually time-expensive to create. Extending the previous example, we
can add a `scope="module"` parameter to the
[`@pytest.fixture`](../reference/reference.html#pytest.fixture "pytest.fixture") invocation
to cause a `smtp_connection` fixture function, responsible to create a connection to a preexisting SMTP server, to only be invoked
once per test *module* (the default is to invoke once per test *function*).
Multiple test functions in a test module will thus
each receive the same `smtp_connection` fixture instance, thus saving time.
Possible values for `scope` are: `function`, `class`, `module`, `package` or `session`.

The next example puts the fixture function into a separate `conftest.py` file
so that tests from multiple test modules in the directory can
access the fixture function:

```
# content of conftest.py
importsmtplib

importpytest

@pytest.fixture(scope="module")
defsmtp_connection():
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
```

```
# content of test_module.py

deftest_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert b"smtp.gmail.com" in msg
    assert 0  # for demo purposes

deftest_noop(smtp_connection):
    response, msg = smtp_connection.noop()
    assert response == 250
    assert 0  # for demo purposes
```

Here, the `test_ehlo` needs the `smtp_connection` fixture value. pytest
will discover and call the [`@pytest.fixture`](../reference/reference.html#pytest.fixture "pytest.fixture")
marked `smtp_connection` fixture function. Running the test looks like this:

```
$ pytest test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py FF                                                    [100%]

================================= FAILURES =================================
________________________________ test_ehlo _________________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0001>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
>       assert 0  # for demo purposes
        ^^^^^^^^
E       assert 0

test_module.py:7: AssertionError
________________________________ test_noop _________________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0001>

    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
>       assert 0  # for demo purposes
        ^^^^^^^^
E       assert 0

test_module.py:13: AssertionError
========================= short test summary info ==========================
FAILED test_module.py::test_ehlo - assert 0
FAILED test_module.py::test_noop - assert 0
============================ 2 failed in 0.12s =============================
```

You see the two `assert 0` failing and more importantly you can also see
that the **exact same** `smtp_connection` object was passed into the
two test functions because pytest shows the incoming argument values in the
traceback. As a result, the two test functions using `smtp_connection` run
as quick as a single one because they reuse the same instance.

If you decide that you rather want to have a session-scoped `smtp_connection`
instance, you can simply declare it:

```
@pytest.fixture(scope="session")
defsmtp_connection():
    # the returned fixture value will be shared for
    # all tests requesting it
    ...
```

### Fixture scopes

Fixtures are created when first requested by a test, and are destroyed based on their `scope`:

* `function`: the default scope, the fixture is destroyed at the end of the test.
* `class`: the fixture is destroyed during teardown of the last test in the class.
* `module`: the fixture is destroyed during teardown of the last test in the module.
* `package`: the fixture is destroyed during teardown of the last test in the package where the fixture is defined, including sub-packages and sub-directories within it.
* `session`: the fixture is destroyed at the end of the test session.

Note

Pytest only caches one instance of a fixture at a time, which
means that when using a parametrized fixture, pytest may invoke a fixture more than once in
the given scope.

### Dynamic scope

Added in version 5.2.

In some cases, you might want to change the scope of the fixture without changing the code.
To do that, pass a callable to `scope`. The callable must return a string with a valid scope
and will be executed only once - during the fixture definition. It will be called with two
keyword arguments - `fixture_name` as a string and `config` with a configuration object.

This can be especially useful when dealing with fixtures that need time for setup, like spawning
a docker container. You can use the command-line argument to control the scope of the spawned
containers for different environments. See the example below.

```
defdetermine_scope(fixture_name, config):
    if config.getoption("--keep-containers", None):
        return "session"
    return "function"

@pytest.fixture(scope=determine_scope)
defdocker_container():
    yield spawn_container()
```

## Teardown/Cleanup (AKA Fixture finalization)

When we run our tests, we’ll want to make sure they clean up after themselves so
they don’t mess with any other tests (and also so that we don’t leave behind a
mountain of test data to bloat the system). Fixtures in pytest offer a very
useful teardown system, which allows us to define the specific steps necessary
for each fixture to clean up after itself.

This system can be leveraged in two ways.

### 1. `yield` fixtures (recommended)

“Yield” fixtures `yield` instead of `return`. With these
fixtures, we can run some code and pass an object back to the requesting
fixture/test, just like with the other fixtures. The only differences are:

1. `return` is swapped out for `yield`.
2. Any teardown code for that fixture is placed *after* the `yield`.

Once pytest figures out a linear order for the fixtures, it will run each one up
until it returns or yields, and then move on to the next fixture in the list to
do the same thing.

Once the test is finished, pytest will go back down the list of fixtures, but in
the *reverse order*, taking each one that yielded, and running the code inside
it that was *after* the `yield` statement.

As a simple example, consider this basic email module:

```
# content of emaillib.py
classMailAdminClient:
    defcreate_user(self):
        return MailUser()

    defdelete_user(self, user):
        # do some cleanup
        pass

classMailUser:
    def__init__(self):
        self.inbox = []

    defsend_email(self, email, other):
        other.inbox.append(email)

    defclear_mailbox(self):
        self.inbox.clear()

classEmail:
    def__init__(self, subject, body):
        self.subject = subject
        self.body = body
```

Let’s say we want to test sending email from one user to another. We’ll have to
first make each user, then send the email from one user to the other, and
finally assert that the other user received that message in their inbox. If we
want to clean up after the test runs, we’ll likely have to make sure the other
user’s mailbox is emptied before deleting that user, otherwise the system may
complain.

Here’s what that might look like:

```
# content of test_emaillib.py
fromemaillibimport Email, MailAdminClient

importpytest

@pytest.fixture
defmail_admin():
    return MailAdminClient()

@pytest.fixture
defsending_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    mail_admin.delete_user(user)

@pytest.fixture
defreceiving_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    user.clear_mailbox()
    mail_admin.delete_user(user)

deftest_email_received(sending_user, receiving_user):
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(email, receiving_user)
    assert email in receiving_user.inbox
```

Because `receiving_user` is the last fixture to run during setup, it’s the first to run
during teardown.

There is a risk that even having the order right on the teardown side of things
doesn’t guarantee a safe cleanup. That’s covered in a bit more detail in
[Safe teardowns](#safe-teardowns).

```
$ pytest -q test_emaillib.py
.                                                                    [100%]
1 passed in 0.12s
```

#### Handling errors for yield fixture

If a yield fixture raises an exception before yielding, pytest won’t try to run
the teardown code after that yield fixture’s `yield` statement. But, for every
fixture that has already run successfully for that test, pytest will still
attempt to tear them down as it normally would.

### 2. Adding finalizers directly

While yield fixtures are considered to be the cleaner and more straightforward
option, there is another choice, and that is to add “finalizer” functions
directly to the test’s [request-context](#request-context) object. It brings a similar result as
yield fixtures, but requires a bit more verbosity.

In order to use this approach, we have to request the [request-context](#request-context) object
(just like we would request another fixture) in the fixture we need to add
teardown code for, and then pass a callable, containing that teardown code, to
its `addfinalizer` method.

We have to be careful though, because pytest will run that finalizer once it’s
been added, even if that fixture raises an exception after adding the finalizer.
So to make sure we don’t run the finalizer code when we wouldn’t need to, we
would only add the finalizer once the fixture would have done something that
we’d need to teardown.

Here’s how the previous example would look using the `addfinalizer` method:

```
# content of test_emaillib.py
fromemaillibimport Email, MailAdminClient

importpytest

@pytest.fixture
defmail_admin():
    return MailAdminClient()

@pytest.fixture
defsending_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    mail_admin.delete_user(user)

@pytest.fixture
defreceiving_user(mail_admin, request):
    user = mail_admin.create_user()

    defdelete_user():
        mail_admin.delete_user(user)

    request.addfinalizer(delete_user)
    return user

@pytest.fixture
defemail(sending_user, receiving_user, request):
    _email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(_email, receiving_user)

    defempty_mailbox():
        receiving_user.clear_mailbox()

    request.addfinalizer(empty_mailbox)
    return _email

deftest_email_received(receiving_user, email):
    assert email in receiving_user.inbox
```

It’s a bit longer than yield fixtures and a bit more complex, but it
does offer some nuances for when you’re in a pinch.

```
$ pytest -q test_emaillib.py
.                                                                    [100%]
1 passed in 0.12s
```

#### Note on finalizer order

Finalizers are executed in a first-in-last-out order.
For yield fixtures, the first teardown code to run is from the right-most fixture, i.e. the last test parameter.

```
# content of test_finalizers.py
importpytest

deftest_bar(fix_w_yield1, fix_w_yield2):
    print("test_bar")

@pytest.fixture
deffix_w_yield1():
    yield
    print("after_yield_1")

@pytest.fixture
deffix_w_yield2():
    yield
    print("after_yield_2")
```

```
$ pytest -s test_finalizers.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_finalizers.py test_bar
.after_yield_2
after_yield_1

============================ 1 passed in 0.12s =============================
```

For finalizers, the first fixture to run is last call to `request.addfinalizer`.

```
# content of test_finalizers.py
fromfunctoolsimport partial
importpytest

@pytest.fixture
deffix_w_finalizers(request):
    request.addfinalizer(partial(print, "finalizer_2"))
    request.addfinalizer(partial(print, "finalizer_1"))

deftest_bar(fix_w_finalizers):
    print("test_bar")
```

```
$ pytest -s test_finalizers.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_finalizers.py test_bar
.finalizer_1
finalizer_2

============================ 1 passed in 0.12s =============================
```

This is so because yield fixtures use `addfinalizer` behind the scenes: when the fixture executes, `addfinalizer` registers a function that resumes the generator, which in turn calls the teardown code.

## Safe teardowns

The fixture system of pytest is *very* powerful, but it’s still being run by a
computer, so it isn’t able to figure out how to safely teardown everything we
throw at it. If we aren’t careful, an error in the wrong spot might leave stuff
from our tests behind, and that can cause further issues pretty quickly.

For example, consider the following tests (based off of the mail example from
above):

```
# content of test_emaillib.py
fromemaillibimport Email, MailAdminClient

importpytest

@pytest.fixture
defsetup():
    mail_admin = MailAdminClient()
    sending_user = mail_admin.create_user()
    receiving_user = mail_admin.create_user()
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(email, receiving_user)
    yield receiving_user, email
    receiving_user.clear_mailbox()
    mail_admin.delete_user(sending_user)
    mail_admin.delete_user(receiving_user)

deftest_email_received(setup):
    receiving_user, email = setup
    assert email in receiving_user.inbox
```

This version is a lot more compact, but it’s also harder to read, doesn’t have a
very descriptive fixture name, and none of the fixtures can be reused easily.

There’s also a more serious issue, which is that if any of those steps in the
setup raise an exception, none of the teardown code will run.

One option might be to go with the `addfinalizer` method instead of yield
fixtures, but that might get pretty complex and difficult to maintain (and it
wouldn’t be compact anymore).

```
$ pytest -q test_emaillib.py
.                                                                    [100%]
1 passed in 0.12s
```

### Safe fixture structure

The safest and simplest fixture structure requires limiting fixtures to only
making one state-changing action each, and then bundling them together with
their teardown code, as [the email examples above](#yield-fixtures) showed.

The chance that a state-changing operation can fail but still modify state is
negligible, as most of these operations tend to be [transaction](https://en.wikipedia.org/wiki/Transaction_processing)-based (at least at the
level of testing where state could be left behind). So if we make sure that any
successful state-changing action gets torn down by moving it to a separate
fixture function and separating it from other, potentially failing
state-changing actions, then our tests will stand the best chance at leaving
the test environment the way they found it.

For an example, let’s say we have a website with a login page, and we have
access to an admin API where we can generate users. For our test, we want to:

1. Create a user through that admin API
2. Launch a browser using Selenium
3. Go to the login page of our site
4. Log in as the user we created
5. Assert that their name is in the header of the landing page

We wouldn’t want to leave that user in the system, nor would we want to leave
that browser session running, so we’ll want to make sure the fixtures that
create those things clean up after themselves.

Here’s what that might look like:

Note

For this example, certain fixtures (i.e. `base_url` and
`admin_credentials`) are implied to exist elsewhere. So for now, let’s
assume they exist, and we’re just not looking at them.

```
fromuuidimport uuid4
fromurllib.parseimport urljoin

fromselenium.webdriverimport Chrome
importpytest

fromsrc.utils.pagesimport LoginPage, LandingPage
fromsrc.utilsimport AdminApiClient
fromsrc.utils.data_typesimport User

@pytest.fixture
defadmin_client(base_url, admin_credentials):
    return AdminApiClient(base_url, **admin_credentials)

@pytest.fixture
defuser(admin_client):
    _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")
    admin_client.create_user(_user)
    yield _user
    admin_client.delete_user(_user)

@pytest.fixture
defdriver():
    _driver = Chrome()
    yield _driver
    _driver.quit()

@pytest.fixture
deflogin(driver, base_url, user):
    driver.get(urljoin(base_url, "/login"))
    page = LoginPage(driver)
    page.login(user)

@pytest.fixture
deflanding_page(driver, login):
    return LandingPage(driver)

deftest_name_on_landing_page_after_login(landing_page, user):
    assert landing_page.header == f"Welcome, {user.name}!"
```

The way the dependencies are laid out means it’s unclear if the `user`
fixture would execute before the `driver` fixture. But that’s ok, because
those are atomic operations, and so it doesn’t matter which one runs first
because the sequence of events for the test is still [linearizable](https://en.wikipedia.org/wiki/Linearizability). But what *does* matter is
that, no matter which one runs first, if the one raises an exception while the
other would not have, neither will have left anything behind. If `driver`
executes before `user`, and `user` raises an exception, the driver will
still quit, and the user was never made. And if `driver` was the one to raise
the exception, then the driver would never have been started and the user would
never have been made.

## Running multiple `assert` statements safely

Sometimes you may want to run multiple asserts after doing all that setup, which
makes sense as, in more complex systems, a single action can kick off multiple
behaviors. pytest has a convenient way of handling this and it combines a bunch
of what we’ve gone over so far.

All that’s needed is stepping up to a larger scope, then having the **act**
step defined as an autouse fixture, and finally, making sure all the fixtures
are targeting that higher level scope.

Let’s pull [an example from above](#safe-fixture-structure), and tweak it a
bit. Let’s say that in addition to checking for a welcome message in the header,
we also want to check for a sign out button, and a link to the user’s profile.

Let’s take a look at how we can structure that so we can run multiple asserts
without having to repeat all those steps again.

Note

For this example, certain fixtures (i.e. `base_url` and
`admin_credentials`) are implied to exist elsewhere. So for now, let’s
assume they exist, and we’re just not looking at them.

```
# contents of tests/end_to_end/test_login.py
fromuuidimport uuid4
fromurllib.parseimport urljoin

fromselenium.webdriverimport Chrome
importpytest

fromsrc.utils.pagesimport LoginPage, LandingPage
fromsrc.utilsimport AdminApiClient
fromsrc.utils.data_typesimport User

@pytest.fixture(scope="class")
defadmin_client(base_url, admin_credentials):
    return AdminApiClient(base_url, **admin_credentials)

@pytest.fixture(scope="class")
defuser(admin_client):
    _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")
    admin_client.create_user(_user)
    yield _user
    admin_client.delete_user(_user)

@pytest.fixture(scope="class")
defdriver():
    _driver = Chrome()
    yield _driver
    _driver.quit()

@pytest.fixture(scope="class")
deflanding_page(driver, login):
    return LandingPage(driver)

classTestLandingPageSuccess:
    @pytest.fixture(scope="class", autouse=True)
    deflogin(self, driver, base_url, user):
        driver.get(urljoin(base_url, "/login"))
        page = LoginPage(driver)
        page.login(user)

    deftest_name_in_header(self, landing_page, user):
        assert landing_page.header == f"Welcome, {user.name}!"

    deftest_sign_out_button(self, landing_page):
        assert landing_page.sign_out_button.is_displayed()

    deftest_profile_link(self, landing_page, user):
        profile_href = urljoin(base_url, f"/profile?id={user.profile_id}")
        assert landing_page.profile_link.get_attribute("href") == profile_href
```

Notice that the methods are only referencing `self` in the signature as a
formality. No state is tied to the actual test class as it might be in the
`unittest.TestCase` framework. Everything is managed by the pytest fixture
system.

Each method only has to request the fixtures that it actually needs without
worrying about order. This is because the **act** fixture is an autouse fixture,
and it made sure all the other fixtures executed before it. There’s no more
changes of state that need to take place, so the tests are free to make as many
non-state-changing queries as they want without risking stepping on the toes of
the other tests.

The `login` fixture is defined inside the class as well, because not every one
of the other tests in the module will be expecting a successful login, and the **act** may need to
be handled a little differently for another test class. For example, if we
wanted to write another test scenario around submitting bad credentials, we
could handle it by adding something like this to the test file:

```
classTestLandingPageBadCredentials:
    @pytest.fixture(scope="class")
    deffaux_user(self, user):
        _user = deepcopy(user)
        _user.password = "badpass"
        return _user

    deftest_raises_bad_credentials_exception(self, login_page, faux_user):
        with pytest.raises(BadCredentialsException):
            login_page.login(faux_user)
```

## Fixtures can introspect the requesting test context

Fixture functions can accept the [`request`](../reference/reference.html#pytest.FixtureRequest "_pytest.fixtures.FixtureRequest") object
to introspect the “requesting” test function, class or module context.
Further extending the previous `smtp_connection` fixture example, let’s
read an optional server URL from the test module which uses our fixture:

```
# content of conftest.py
importsmtplib

importpytest

@pytest.fixture(scope="module")
defsmtp_connection(request):
    server = getattr(request.module, "smtpserver", "smtp.gmail.com")
    smtp_connection = smtplib.SMTP(server, 587, timeout=5)
    yield smtp_connection
    print(f"finalizing {smtp_connection} ({server})")
    smtp_connection.close()
```

We use the `request.module` attribute to optionally obtain an
`smtpserver` attribute from the test module. If we just execute
again, nothing much has changed:

```
$ pytest -s -q --tb=no test_module.py
FFfinalizing <smtplib.SMTP object at 0xdeadbeef0002> (smtp.gmail.com)

========================= short test summary info ==========================
FAILED test_module.py::test_ehlo - assert 0
FAILED test_module.py::test_noop - assert 0
2 failed in 0.12s
```

Let’s quickly create another test module that actually sets the
server URL in its module namespace:

```
# content of test_anothersmtp.py

smtpserver = "mail.python.org"  # will be read by smtp fixture

deftest_showhelo(smtp_connection):
    assert 0, smtp_connection.helo()
```

Running it:

```
$ pytest -qq --tb=short test_anothersmtp.py
F                                                                    [100%]
================================= FAILURES =================================
______________________________ test_showhelo _______________________________
test_anothersmtp.py:6: in test_showhelo
    assert 0, smtp_connection.helo()
E   AssertionError: (250, b'mail.python.org')
E   assert 0
------------------------- Captured stdout teardown -------------------------
finalizing <smtplib.SMTP object at 0xdeadbeef0003> (mail.python.org)
========================= short test summary info ==========================
FAILED test_anothersmtp.py::test_showhelo - AssertionError: (250, b'mail....
```

voila! The `smtp_connection` fixture function picked up our mail server name
from the module namespace.

## Using markers to pass data to fixtures

Using the [`request`](../reference/reference.html#pytest.FixtureRequest "_pytest.fixtures.FixtureRequest") object, a fixture can also access
markers which are applied to a test function. This can be useful to pass data
into a fixture from a test:

```
importpytest

@pytest.fixture
deffixt(request):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        # Handle missing marker in some way...
        data = None
    else:
        data = marker.args[0]

    # Do something with the data
    return data

@pytest.mark.fixt_data(42)
deftest_fixt(fixt):
    assert fixt == 42
```

## Factories as fixtures

The “factory as fixture” pattern can help in situations where the result
of a fixture is needed multiple times in a single test. Instead of returning
data directly, the fixture instead returns a function which generates the data.
This function can then be called multiple times in the test.

Factories can have parameters as needed:

```
@pytest.fixture
defmake_customer_record():
    def_make_customer_record(name):
        return {"name": name, "orders": []}

    return _make_customer_record

deftest_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
```

If the data created by the factory requires managing, the fixture can take care of that:

```
@pytest.fixture
defmake_customer_record():
    created_records = []

    def_make_customer_record(name):
        record = models.Customer(name=name, orders=[])
        created_records.append(record)
        return record

    yield _make_customer_record

    for record in created_records:
        record.destroy()

deftest_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
```

## Parametrizing fixtures

Fixture functions can be parametrized in which case they will be called
multiple times, each time executing the set of dependent tests, i.e. the
tests that depend on this fixture. Test functions usually do not need
to be aware of their re-running. Fixture parametrization helps to
write exhaustive functional tests for components which themselves can be
configured in multiple ways.

Extending the previous example, we can flag the fixture to create two
`smtp_connection` fixture instances which will cause all tests using the fixture
to run twice. The fixture function gets access to each parameter
through the special [`request`](../reference/reference.html#pytest.FixtureRequest "pytest.FixtureRequest") object:

```
# content of conftest.py
importsmtplib

importpytest

@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
defsmtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print(f"finalizing {smtp_connection}")
    smtp_connection.close()
```

The main change is the declaration of `params` with
[`@pytest.fixture`](../reference/reference.html#pytest.fixture "pytest.fixture"), a list of values
for each of which the fixture function will execute and can access
a value via `request.param`. No test function code needs to change.
So let’s just do another run:

```
$ pytest -q test_module.py
FFFF                                                                 [100%]
================================= FAILURES =================================
________________________ test_ehlo[smtp.gmail.com] _________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0004>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
>       assert 0  # for demo purposes
        ^^^^^^^^
E       assert 0

test_module.py:7: AssertionError
________________________ test_noop[smtp.gmail.com] _________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0004>

    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
>       assert 0  # for demo purposes
        ^^^^^^^^
E       assert 0

test_module.py:13: AssertionError
________________________ test_ehlo[mail.python.org] ________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0005>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
>       assert b"smtp.gmail.com" in msg
E       AssertionError: assert b'smtp.gmail.com' in b'mail.python.org\nPIPELINING\nSIZE 51200000\nETRN\nSTARTTLS\nAUTH DIGEST-MD5 NTLM CRAM-MD5\nENHANCEDSTATUSCODES\n8BITMIME\nDSN\nSMTPUTF8\nCHUNKING'

test_module.py:6: AssertionError
-------------------------- Captured stdout setup ---------------------------
finalizing <smtplib.SMTP object at 0xdeadbeef0004>
________________________ test_noop[mail.python.org] ________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0005>

    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
>       assert 0  # for demo purposes
        ^^^^^^^^
E       assert 0

test_module.py:13: AssertionError
------------------------- Captured stdout teardown -------------------------
finalizing <smtplib.SMTP object at 0xdeadbeef0005>
========================= short test summary info ==========================
FAILED test_module.py::test_ehlo[smtp.gmail.com] - assert 0
FAILED test_module.py::test_noop[smtp.gmail.com] - assert 0
FAILED test_module.py::test_ehlo[mail.python.org] - AssertionError: asser...
FAILED test_module.py::test_noop[mail.python.org] - assert 0
4 failed in 0.12s
```

We see that our two test functions each ran twice, against the different
`smtp_connection` instances. Note also, that with the `mail.python.org`
connection the second test fails in `test_ehlo` because a
different server string is expected than what arrived.

pytest will build a string that is the test ID for each fixture value
in a parametrized fixture, e.g. `test_ehlo[smtp.gmail.com]` and
`test_ehlo[mail.python.org]` in the above examples. These IDs can
be used with [`-k`](../reference/reference.html#cmdoption-k) to select specific cases to run, and they will
also identify the specific case when one is failing. Running pytest
with [`--collect-only`](../reference/reference.html#cmdoption-collect-only) will show the generated IDs.

Numbers, strings, booleans and `None` will have their usual string
representation used in the test ID. For other objects, pytest will
make a string based on the argument name. It is possible to customise
the string used in a test ID for a certain fixture value by using the
`ids` keyword argument:

```
# content of test_ids.py
importpytest

@pytest.fixture(params=[0, 1], ids=["spam", "ham"])
defa(request):
    return request.param

deftest_a(a):
    pass

defidfn(fixture_value):
    if fixture_value == 0:
        return "eggs"
    else:
        return None

@pytest.fixture(params=[0, 1], ids=idfn)
defb(request):
    return request.param

deftest_b(b):
    pass
```

The above shows how `ids` can be either a list of strings to use or
a function which will be called with the fixture value and then
has to return a string to use. In the latter case if the function
returns `None` then pytest’s auto-generated ID will be used.

Running the above tests results in the following test IDs being used:

```
$ pytest --collect-only
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 12 items

<Dir fixtures.rst-234>
  <Module test_anothersmtp.py>
    <Function test_showhelo[smtp.gmail.com]>
    <Function test_showhelo[mail.python.org]>
  <Module test_emaillib.py>
    <Function test_email_received>
  <Module test_finalizers.py>
    <Function test_bar>
  <Module test_ids.py>
    <Function test_a[spam]>
    <Function test_a[ham]>
    <Function test_b[eggs]>
    <Function test_b[1]>
  <Module test_module.py>
    <Function test_ehlo[smtp.gmail.com]>
    <Function test_noop[smtp.gmail.com]>
    <Function test_ehlo[mail.python.org]>
    <Function test_noop[mail.python.org]>

======================= 12 tests collected in 0.12s ========================
```

## Using marks with parametrized fixtures

[`pytest.param()`](../reference/reference.html#pytest.param "pytest.param") can be used to apply marks in values sets of parametrized fixtures in the same way
that they can be used with [@pytest.mark.parametrize](parametrize.html#pytest-mark-parametrize).

Example:

```
# content of test_fixture_marks.py
importpytest

@pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
defdata_set(request):
    return request.param

deftest_data(data_set):
    pass
```

Running this test will *skip* the invocation of `data_set` with value `2`:

```
$ pytest test_fixture_marks.py -v
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 3 items

test_fixture_marks.py::test_data[0] PASSED                           [ 33%]
test_fixture_marks.py::test_data[1] PASSED                           [ 66%]
test_fixture_marks.py::test_data[2] SKIPPED (unconditional skip)     [100%]

======================= 2 passed, 1 skipped in 0.12s =======================
```

## Modularity: using fixtures from a fixture function

In addition to using fixtures in test functions, fixture functions
can use other fixtures themselves. This contributes to a modular design
of your fixtures and allows reuse of framework-specific fixtures across
many projects. As a simple example, we can extend the previous example
and instantiate an object `app` where we stick the already defined
`smtp_connection` resource into it:

```
# content of test_appsetup.py

importpytest

classApp:
    def__init__(self, smtp_connection):
        self.smtp_connection = smtp_connection

@pytest.fixture(scope="module")
defapp(smtp_connection):
    return App(smtp_connection)

deftest_smtp_connection_exists(app):
    assert app.smtp_connection
```

Here we declare an `app` fixture which receives the previously defined
`smtp_connection` fixture and instantiates an `App` object with it. Let’s run it:

```
$ pytest -v test_appsetup.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 2 items

test_appsetup.py::test_smtp_connection_exists[smtp.gmail.com] PASSED [ 50%]
test_appsetup.py::test_smtp_connection_exists[mail.python.org] PASSED [100%]

============================ 2 passed in 0.12s =============================
```

Due to the parametrization of `smtp_connection`, the test will run twice with two
different `App` instances and respective smtp servers. There is no
need for the `app` fixture to be aware of the `smtp_connection`
parametrization because pytest will fully analyse the fixture dependency graph.

Note that the `app` fixture has a scope of `module` and uses a
module-scoped `smtp_connection` fixture. The example would still work if
`smtp_connection` was cached on a `session` scope: it is fine for fixtures to use
“broader” scoped fixtures but not the other way round:
A session-scoped fixture could not use a module-scoped one in a
meaningful way.

## Automatic grouping of tests by fixture instances

pytest minimizes the number of active fixtures during test runs.
If you have a parametrized fixture, then all the tests using it will
first execute with one instance and then finalizers are called
before the next fixture instance is created. Among other things,
this eases testing of applications which create and use global state.

The following example uses two parametrized fixtures, one of which is
scoped on a per-module basis, and all the functions perform `print` calls
to show the setup/teardown flow:

```
# content of test_module.py
importpytest

@pytest.fixture(scope="module", params=["mod1", "mod2"])
defmodarg(request):
    param = request.param
    print("  SETUP modarg", param)
    yield param
    print("  TEARDOWN modarg", param)

@pytest.fixture(scope="function", params=[1, 2])
defotherarg(request):
    param = request.param
    print("  SETUP otherarg", param)
    yield param
    print("  TEARDOWN otherarg", param)

deftest_0(otherarg):
    print("  RUN test0 with otherarg", otherarg)

deftest_1(modarg):
    print("  RUN test1 with modarg", modarg)

deftest_2(otherarg, modarg):
    print(f"  RUN test2 with otherarg {otherarg} and modarg {modarg}")
```

Let’s run the tests in verbose mode and with looking at the print-output:

```
$ pytest -v -s test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 8 items

test_module.py::test_0[1]   SETUP otherarg 1
  RUN test0 with otherarg 1
PASSED  TEARDOWN otherarg 1

test_module.py::test_0[2]   SETUP otherarg 2
  RUN test0 with otherarg 2
PASSED  TEARDOWN otherarg 2

test_module.py::test_1[mod1]   SETUP modarg mod1
  RUN test1 with modarg mod1
PASSED
test_module.py::test_2[mod1-1]   SETUP otherarg 1
  RUN test2 with otherarg 1 and modarg mod1
PASSED  TEARDOWN otherarg 1

test_module.py::test_2[mod1-2]   SETUP otherarg 2
  RUN test2 with otherarg 2 and modarg mod1
PASSED  TEARDOWN otherarg 2

test_module.py::test_1[mod2]   TEARDOWN modarg mod1
  SETUP modarg mod2
  RUN test1 with modarg mod2
PASSED
test_module.py::test_2[mod2-1]   SETUP otherarg 1
  RUN test2 with otherarg 1 and modarg mod2
PASSED  TEARDOWN otherarg 1

test_module.py::test_2[mod2-2]   SETUP otherarg 2
  RUN test2 with otherarg 2 and modarg mod2
PASSED  TEARDOWN otherarg 2
  TEARDOWN modarg mod2

============================ 8 passed in 0.12s =============================
```

You can see that the parametrized module-scoped `modarg` resource caused an
ordering of test execution that led to the fewest possible “active” resources.
The finalizer for the `mod1` parametrized resource was executed before the
`mod2` resource was setup.

In particular notice that test\_0 is completely independent and finishes first.
Then test\_1 is executed with `mod1`, then test\_2 with `mod1`, then test\_1
with `mod2` and finally test\_2 with `mod2`.

The `otherarg` parametrized resource (having function scope) was set up before
and torn down after every test that used it.

## Use fixtures in classes and modules with `usefixtures`

Sometimes test functions do not directly need access to a fixture object.
For example, tests may require to operate with an empty directory as the
current working directory but otherwise do not care for the concrete
directory. Here is how you can use the standard [`tempfile`](https://docs.python.org/3/library/tempfile.html#module-tempfile "(in Python v3.14)")
and pytest fixtures to
achieve it. We separate the creation of the fixture into a `conftest.py`
file:

```
# content of conftest.py

importos
importtempfile

importpytest

@pytest.fixture
defcleandir():
    with tempfile.TemporaryDirectory() as newpath:
        old_cwd = os.getcwd()
        os.chdir(newpath)
        yield
        os.chdir(old_cwd)
```

and declare its use in a test module via a `usefixtures` marker:

```
# content of test_setenv.py
importos

importpytest

@pytest.mark.usefixtures("cleandir")
classTestDirectoryInit:
    deftest_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w", encoding="utf-8") as f:
            f.write("hello")

    deftest_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
```

Due to the `usefixtures` marker, the `cleandir` fixture
will be required for the execution of each test method, just as if
you specified a “cleandir” function argument to each of them. Let’s run it
to verify our fixture is activated and the tests pass:

```
$ pytest -q
..                                                                   [100%]
2 passed in 0.12s
```

You can specify multiple fixtures like this:

```
@pytest.mark.usefixtures("cleandir", "anotherfixture")
deftest(): ...
```

and you may specify fixture usage at the test module level using [`pytestmark`](../reference/reference.html#globalvar-pytestmark):

```
pytestmark = pytest.mark.usefixtures("cleandir")
```

It is also possible to put fixtures required by all tests in your project
into a configuration file:

```
# content of pytest.toml
[pytest]
usefixtures=["cleandir"]
```

Warning

Note this mark has no effect in **fixture functions**. For example,
this **will not work as expected**:

```
@pytest.mark.usefixtures("my_other_fixture")
@pytest.fixture
defmy_fixture_that_sadly_wont_use_my_other_fixture(): ...
```

This generates a deprecation warning, and will become an error in Pytest 8.

## Overriding fixtures on various levels

In a relatively large test suite, you may want to *override* a fixture, to augment
or change its behavior inside of certain test modules or directories.

### Override a fixture on a folder (conftest) level

Given the tests file structure is:

```
tests/
    conftest.py
        # content of tests/conftest.py
        importpytest

        @pytest.fixture
        defusername():
            return 'username'

    test_something.py
        # content of tests/test_something.py
        deftest_username(username):
            assert username == 'username'

    subfolder/
        conftest.py
            # content of tests/subfolder/conftest.py
            importpytest

            @pytest.fixture
            defusername(username):
                return 'overridden-' + username

        test_something_else.py
            # content of tests/subfolder/test_something_else.py
            deftest_username(username):
                assert username == 'overridden-username'
```

As you can see, a fixture with the same name can be overridden for a certain test directory level.
Note that the `base` or `super` fixture can be accessed from the `overriding`
fixture easily - used in the example above.

### Override a fixture on a test module level

Given the tests file structure is:

```
tests/
    conftest.py
        # content of tests/conftest.py
        importpytest

        @pytest.fixture
        defusername():
            return 'username'

    test_something.py
        # content of tests/test_something.py
        importpytest

        @pytest.fixture
        defusername(username):
            return 'overridden-' + username

        deftest_username(username):
            assert username == 'overridden-username'

    test_something_else.py
        # content of tests/test_something_else.py
        importpytest

        @pytest.fixture
        defusername(username):
            return 'overridden-else-' + username

        deftest_username(username):
            assert username == 'overridden-else-username'
```

In the example above, a fixture with the same name can be overridden for a certain test module.

### Override a fixture with direct test parametrization

Given the tests file structure is:

```
tests/
    conftest.py
        # content of tests/conftest.py
        importpytest

        @pytest.fixture
        defusername():
            return 'username'

        @pytest.fixture
        defother_username(username):
            return 'other-' + username

    test_something.py
        # content of tests/test_something.py
        importpytest

        @pytest.mark.parametrize('username', ['directly-overridden-username'])
        deftest_username(username):
            assert username == 'directly-overridden-username'

        @pytest.mark.parametrize('username', ['directly-overridden-username-other'])
        deftest_username_other(other_username):
            assert other_username == 'other-directly-overridden-username-other'
```

In the example above, a fixture value is overridden by the test parameter value. Note that the value of the fixture
can be overridden this way even if the test doesn’t use it directly (doesn’t mention it in the function prototype).

### Override a parametrized fixture with non-parametrized one and vice versa

Given the tests file structure is:

```
tests/
    conftest.py
        # content of tests/conftest.py
        importpytest

        @pytest.fixture(params=['one', 'two', 'three'])
        defparametrized_username(request):
            return request.param

        @pytest.fixture
        defnon_parametrized_username(request):
            return 'username'

    test_something.py
        # content of tests/test_something.py
        importpytest

        @pytest.fixture
        defparametrized_username():
            return 'overridden-username'

        @pytest.fixture(params=['one', 'two', 'three'])
        defnon_parametrized_username(request):
            return request.param

        deftest_username(parametrized_username):
            assert parametrized_username == 'overridden-username'

        deftest_parametrized_username(non_parametrized_username):
            assert non_parametrized_username in ['one', 'two', 'three']

    test_something_else.py
        # content of tests/test_something_else.py
        deftest_username(parametrized_username):
            assert parametrized_username in ['one', 'two', 'three']

        deftest_username(non_parametrized_username):
            assert non_parametrized_username == 'username'
```

In the example above, a parametrized fixture is overridden with a non-parametrized version, and
a non-parametrized fixture is overridden with a parametrized version for certain test module.
The same applies for the test folder level obviously.

## Using fixtures from other projects

Usually projects that provide pytest support will use [entry points](writing_plugins.html#pip-installable-plugins),
so just installing those projects into an environment will make those fixtures available for use.

In case you want to use fixtures from a project that does not use entry points, you can
define [`pytest_plugins`](../reference/reference.html#globalvar-pytest_plugins) in your top `conftest.py` file to register that module
as a plugin.

Suppose you have some fixtures in `mylibrary.fixtures` and you want to reuse them into your
`app/tests` directory.

All you need to do is to define [`pytest_plugins`](../reference/reference.html#globalvar-pytest_plugins) in `app/tests/conftest.py`
pointing to that module.

```
pytest_plugins = "mylibrary.fixtures"
```

This effectively registers `mylibrary.fixtures` as a plugin, making all its fixtures and
hooks available to tests in `app/tests`.

Note

Sometimes users will *import* fixtures from other projects for use, however this is not
recommended: importing fixtures into a module will register them in pytest
as *defined* in that module.

This has minor consequences, such as appearing multiple times in `pytest --help`,
but it is not **recommended** because this behavior might change/stop working
in future versions.

---

## Bibliography

1. [How to write and report assertions in tests](https://docs.pytest.org/en/stable/how-to/assert.html)
2. [Get Started](https://docs.pytest.org/en/stable/getting-started.html)
3. [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html)
4. [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)