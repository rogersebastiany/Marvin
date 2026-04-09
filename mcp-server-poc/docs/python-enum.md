enum — Support for enumerations — Python 3.12.13 documentation

@media only screen {
table.full-width-table {
width: 100%;
}
}

Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [`enum` — Support for enumerations](#)
  + [Module Contents](#module-contents)
  + [Data Types](#data-types)
    - [Supported `__dunder__` names](#supported-dunder-names)
    - [Supported `_sunder_` names](#supported-sunder-names)
  + [Utilities and Decorators](#utilities-and-decorators)
  + [Notes](#notes)

#### Previous topic

[`reprlib` — Alternate `repr()` implementation](reprlib.html "previous chapter")

#### Next topic

[`graphlib` — Functionality to operate with graph-like structures](graphlib.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/enum.rst)

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](graphlib.html "graphlib — Functionality to operate with graph-like structures") |
* [previous](reprlib.html "reprlib — Alternate repr() implementation") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Data Types](datatypes.html) »
* `enum` — Support for enumerations
* |
* Theme
  Auto
  Light
  Dark
   |

# `enum` — Support for enumerations[¶](#module-enum "Link to this heading")

Added in version 3.4.

**Source code:** [Lib/enum.py](https://github.com/python/cpython/tree/3.12/Lib/enum.py)

Important

This page contains the API reference information. For tutorial
information and discussion of more advanced topics, see

* [Basic Tutorial](../howto/enum.html#enum-basic-tutorial)
* [Advanced Tutorial](../howto/enum.html#enum-advanced-tutorial)
* [Enum Cookbook](../howto/enum.html#enum-cookbook)

---

An enumeration:

* is a set of symbolic names (members) bound to unique values
* can be iterated over to return its canonical (i.e. non-alias) members in
  definition order
* uses *call* syntax to return members by value
* uses *index* syntax to return members by name

Enumerations are created either by using [`class`](../reference/compound_stmts.html#class) syntax, or by
using function-call syntax:

```
>>> from enum import Enum

>>> # class syntax
>>> class Color(Enum):
...     RED = 1
...     GREEN = 2
...     BLUE = 3

>>> # functional syntax
>>> Color = Enum('Color', [('RED', 1), ('GREEN', 2), ('BLUE', 3)])
```

Even though we can use [`class`](../reference/compound_stmts.html#class) syntax to create Enums, Enums
are not normal Python classes. See
[How are Enums different?](../howto/enum.html#enum-class-differences) for more details.

Note

Nomenclature

* The class `Color` is an *enumeration* (or *enum*)
* The attributes `Color.RED`, `Color.GREEN`, etc., are
  *enumeration members* (or *members*) and are functionally constants.
* The enum members have *names* and *values* (the name of
  `Color.RED` is `RED`, the value of `Color.BLUE` is
  `3`, etc.)

---

## Module Contents[¶](#module-contents "Link to this heading")

> [`EnumType`](#enum.EnumType "enum.EnumType")
>
> > The `type` for Enum and its subclasses.
>
> [`Enum`](#enum.Enum "enum.Enum")
>
> > Base class for creating enumerated constants.
>
> [`IntEnum`](#enum.IntEnum "enum.IntEnum")
>
> > Base class for creating enumerated constants that are also
> > subclasses of [`int`](functions.html#int "int"). ([Notes](#notes))
>
> [`StrEnum`](#enum.StrEnum "enum.StrEnum")
>
> > Base class for creating enumerated constants that are also
> > subclasses of [`str`](stdtypes.html#str "str"). ([Notes](#notes))
>
> [`Flag`](#enum.Flag "enum.Flag")
>
> > Base class for creating enumerated constants that can be combined using
> > the bitwise operations without losing their [`Flag`](#enum.Flag "enum.Flag") membership.
>
> [`IntFlag`](#enum.IntFlag "enum.IntFlag")
>
> > Base class for creating enumerated constants that can be combined using
> > the bitwise operators without losing their [`IntFlag`](#enum.IntFlag "enum.IntFlag") membership.
> > [`IntFlag`](#enum.IntFlag "enum.IntFlag") members are also subclasses of [`int`](functions.html#int "int"). ([Notes](#notes))
>
> [`ReprEnum`](#enum.ReprEnum "enum.ReprEnum")
>
> > Used by [`IntEnum`](#enum.IntEnum "enum.IntEnum"), [`StrEnum`](#enum.StrEnum "enum.StrEnum"), and [`IntFlag`](#enum.IntFlag "enum.IntFlag")
> > to keep the [`str()`](stdtypes.html#str "str") of the mixed-in type.
>
> [`EnumCheck`](#enum.EnumCheck "enum.EnumCheck")
>
> > An enumeration with the values `CONTINUOUS`, `NAMED_FLAGS`, and
> > `UNIQUE`, for use with [`verify()`](#enum.verify "enum.verify") to ensure various constraints
> > are met by a given enumeration.
>
> [`FlagBoundary`](#enum.FlagBoundary "enum.FlagBoundary")
>
> > An enumeration with the values `STRICT`, `CONFORM`, `EJECT`, and
> > `KEEP` which allows for more fine-grained control over how invalid values
> > are dealt with in an enumeration.
>
> [`auto`](#enum.auto "enum.auto")
>
> > Instances are replaced with an appropriate value for Enum members.
> > [`StrEnum`](#enum.StrEnum "enum.StrEnum") defaults to the lower-cased version of the member name,
> > while other Enums default to 1 and increase from there.
>
> [`property()`](#enum.property "enum.property")
>
> > Allows [`Enum`](#enum.Enum "enum.Enum") members to have attributes without conflicting with
> > member names. The `value` and `name` attributes are implemented this
> > way.
>
> [`unique()`](#enum.unique "enum.unique")
>
> > Enum class decorator that ensures only one name is bound to any one value.
>
> [`verify()`](#enum.verify "enum.verify")
>
> > Enum class decorator that checks user-selectable constraints on an
> > enumeration.
>
> [`member()`](#enum.member "enum.member")
>
> > Make `obj` a member. Can be used as a decorator.
>
> [`nonmember()`](#enum.nonmember "enum.nonmember")
>
> > Do not make `obj` a member. Can be used as a decorator.
>
> [`global_enum()`](#enum.global_enum "enum.global_enum")
>
> > Modify the [`str()`](stdtypes.html#str "str") and [`repr()`](functions.html#repr "repr") of an enum
> > to show its members as belonging to the module instead of its class,
> > and export the enum members to the global namespace.
>
> [`show_flag_values()`](#enum.show_flag_values "enum.show_flag_values")
>
> > Return a list of all power-of-two integers contained in a flag.

Added in version 3.6: `Flag`, `IntFlag`, `auto`

Added in version 3.11: `StrEnum`, `EnumCheck`, `ReprEnum`, `FlagBoundary`, `property`, `member`, `nonmember`, `global_enum`, `show_flag_values`

---

## Data Types[¶](#data-types "Link to this heading")

*class* enum.EnumType[¶](#enum.EnumType "Link to this definition")
:   *EnumType* is the [metaclass](../glossary.html#term-metaclass) for *enum* enumerations. It is possible
    to subclass *EnumType* – see [Subclassing EnumType](../howto/enum.html#enumtype-examples)
    for details.

    *EnumType* is responsible for setting the correct `__repr__()`,
    `__str__()`, `__format__()`, and `__reduce__()` methods on the
    final *enum*, as well as creating the enum members, properly handling
    duplicates, providing iteration over the enum class, etc.

    \_\_call\_\_(*cls*, *value*, *names=None*, *\**, *module=None*, *qualname=None*, *type=None*, *start=1*, *boundary=None*)[¶](#enum.EnumType.__call__ "Link to this definition")
    :   This method is called in two different ways:

        * to look up an existing member:

          > cls:
          > :   The enum class being called.
          >
          > value:
          > :   The value to lookup.
        * to use the `cls` enum to create a new enum (only if the existing enum
          does not have any members):

          > cls:
          > :   The enum class being called.
          >
          > value:
          > :   The name of the new Enum to create.
          >
          > names:
          > :   The names/values of the members for the new Enum.
          >
          > module:
          > :   The name of the module the new Enum is created in.
          >
          > qualname:
          > :   The actual location in the module where this Enum can be found.
          >
          > type:
          > :   A mix-in type for the new Enum.
          >
          > start:
          > :   The first integer value for the Enum (used by [`auto`](#enum.auto "enum.auto")).
          >
          > boundary:
          > :   How to handle out-of-range values from bit operations ([`Flag`](#enum.Flag "enum.Flag") only).

    \_\_contains\_\_(*cls*, *member*)[¶](#enum.EnumType.__contains__ "Link to this definition")
    :   Returns `True` if member belongs to the `cls`:

        ```
        >>> some_var = Color.RED
        >>> some_var in Color
        True
        >>> Color.RED.value in Color
        True
        ```

    Changed in version 3.12: Before Python 3.12, a `TypeError` is raised if a
    non-Enum-member is used in a containment check.

    \_\_dir\_\_(*cls*)[¶](#enum.EnumType.__dir__ "Link to this definition")
    :   Returns `['__class__', '__doc__', '__members__', '__module__']` and the
        names of the members in *cls*:

        ```
        >>> dir(Color)
        ['BLUE', 'GREEN', 'RED', '__class__', '__contains__', '__doc__', '__getitem__', '__init_subclass__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__']
        ```

    \_\_getitem\_\_(*cls*, *name*)[¶](#enum.EnumType.__getitem__ "Link to this definition")
    :   Returns the Enum member in *cls* matching *name*, or raises a [`KeyError`](exceptions.html#KeyError "KeyError"):

        ```
        >>> Color['BLUE']
        <Color.BLUE: 3>
        ```

    \_\_iter\_\_(*cls*)[¶](#enum.EnumType.__iter__ "Link to this definition")
    :   Returns each member in *cls* in definition order:

        ```
        >>> list(Color)
        [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 3>]
        ```

    \_\_len\_\_(*cls*)[¶](#enum.EnumType.__len__ "Link to this definition")
    :   Returns the number of member in *cls*:

        ```
        >>> len(Color)
        3
        ```

    \_\_members\_\_[¶](#enum.EnumType.__members__ "Link to this definition")
    :   Returns a mapping of every enum name to its member, including aliases

    \_\_reversed\_\_(*cls*)[¶](#enum.EnumType.__reversed__ "Link to this definition")
    :   Returns each member in *cls* in reverse definition order:

        ```
        >>> list(reversed(Color))
        [<Color.BLUE: 3>, <Color.GREEN: 2>, <Color.RED: 1>]
        ```

    Added in version 3.11: Before 3.11 `enum` used `EnumMeta` type, which is kept as an alias.

*class* enum.Enum[¶](#enum.Enum "Link to this definition")
:   *Enum* is the base class for all *enum* enumerations.

    name[¶](#enum.Enum.name "Link to this definition")
    :   The name used to define the `Enum` member:

        ```
        >>> Color.BLUE.name
        'BLUE'
        ```

    value[¶](#enum.Enum.value "Link to this definition")
    :   The value given to the `Enum` member:

        ```
        >>> Color.RED.value
        1
        ```

        Value of the member, can be set in [`__new__()`](#enum.Enum.__new__ "enum.Enum.__new__").

        Note

        Enum member values

        Member values can be anything: [`int`](functions.html#int "int"), [`str`](stdtypes.html#str "str"), etc. If
        the exact value is unimportant you may use [`auto`](#enum.auto "enum.auto") instances and an
        appropriate value will be chosen for you. See [`auto`](#enum.auto "enum.auto") for the
        details.

        While mutable/unhashable values, such as [`dict`](stdtypes.html#dict "dict"), [`list`](stdtypes.html#list "list") or
        a mutable [`dataclass`](dataclasses.html#dataclasses.dataclass "dataclasses.dataclass"), can be used, they will have a
        quadratic performance impact during creation relative to the
        total number of mutable/unhashable values in the enum.

    \_name\_[¶](#enum.Enum._name_ "Link to this definition")
    :   Name of the member.

    \_value\_[¶](#enum.Enum._value_ "Link to this definition")
    :   Value of the member, can be set in [`__new__()`](#enum.Enum.__new__ "enum.Enum.__new__").

    \_order\_[¶](#enum.Enum._order_ "Link to this definition")
    :   No longer used, kept for backward compatibility.
        (class attribute, removed during class creation).

    \_ignore\_[¶](#enum.Enum._ignore_ "Link to this definition")
    :   `_ignore_` is only used during creation and is removed from the
        enumeration once creation is complete.

        `_ignore_` is a list of names that will not become members, and whose
        names will also be removed from the completed enumeration. See
        [TimePeriod](../howto/enum.html#enum-time-period) for an example.

    \_\_dir\_\_(*self*)[¶](#enum.Enum.__dir__ "Link to this definition")
    :   Returns `['__class__', '__doc__', '__module__', 'name', 'value']` and
        any public methods defined on *self.\_\_class\_\_*:

        ```
        >>> from datetime import date
        >>> class Weekday(Enum):
        ...     MONDAY = 1
        ...     TUESDAY = 2
        ...     WEDNESDAY = 3
        ...     THURSDAY = 4
        ...     FRIDAY = 5
        ...     SATURDAY = 6
        ...     SUNDAY = 7
        ...     @classmethod
        ...     def today(cls):
        ...         print('today is %s' % cls(date.today().isoweekday()).name)
        ...
        >>> dir(Weekday.SATURDAY)
        ['__class__', '__doc__', '__eq__', '__hash__', '__module__', 'name', 'today', 'value']
        ```

    \_generate\_next\_value\_(*name*, *start*, *count*, *last\_values*)[¶](#enum.Enum._generate_next_value_ "Link to this definition")
    :   > name:
        > :   The name of the member being defined (e.g. ‘RED’).
        >
        > start:
        > :   The start value for the Enum; the default is 1.
        >
        > count:
        > :   The number of members currently defined, not including this one.
        >
        > last\_values:
        > :   A list of the previous values.

        A *staticmethod* that is used to determine the next value returned by
        [`auto`](#enum.auto "enum.auto"):

        ```
        >>> from enum import auto
        >>> class PowersOfThree(Enum):
        ...     @staticmethod
        ...     def _generate_next_value_(name, start, count, last_values):
        ...         return 3 ** (count + 1)
        ...     FIRST = auto()
        ...     SECOND = auto()
        ...
        >>> PowersOfThree.SECOND.value
        9
        ```

    \_\_init\_\_(*self*, *\*args*, *\*\*kwds*)[¶](#enum.Enum.__init__ "Link to this definition")
    :   By default, does nothing. If multiple values are given in the member
        assignment, those values become separate arguments to `__init__`; e.g.

        ```
        >>> from enum import Enum
        >>> class Weekday(Enum):
        ...     MONDAY = 1, 'Mon'
        ```

        `Weekday.__init__()` would be called as `Weekday.__init__(self, 1, 'Mon')`

    \_\_init\_subclass\_\_(*cls*, *\*\*kwds*)[¶](#enum.Enum.__init_subclass__ "Link to this definition")
    :   A *classmethod* that is used to further configure subsequent subclasses.
        By default, does nothing.

    \_missing\_(*cls*, *value*)[¶](#enum.Enum._missing_ "Link to this definition")
    :   A *classmethod* for looking up values not found in *cls*. By default it
        does nothing, but can be overridden to implement custom search behavior:

        ```
        >>> from enum import StrEnum
        >>> class Build(StrEnum):
        ...     DEBUG = auto()
        ...     OPTIMIZED = auto()
        ...     @classmethod
        ...     def _missing_(cls, value):
        ...         value = value.lower()
        ...         for member in cls:
        ...             if member.value == value:
        ...                 return member
        ...         return None
        ...
        >>> Build.DEBUG.value
        'debug'
        >>> Build('deBUG')
        <Build.DEBUG: 'debug'>
        ```

    \_\_new\_\_(*cls*, *\*args*, *\*\*kwds*)[¶](#enum.Enum.__new__ "Link to this definition")
    :   By default, doesn’t exist. If specified, either in the enum class
        definition or in a mixin class (such as `int`), all values given
        in the member assignment will be passed; e.g.

        ```
        >>> from enum import Enum
        >>> class MyIntEnum(int, Enum):
        ...     TWENTYSIX = '1a', 16
        ```

        results in the call `int('1a', 16)` and a value of `26` for the member.

        Note

        When writing a custom `__new__`, do not use `super().__new__` –
        call the appropriate `__new__` instead.

    \_\_repr\_\_(*self*)[¶](#enum.Enum.__repr__ "Link to this definition")
    :   Returns the string used for *repr()* calls. By default, returns the
        *Enum* name, member name, and value, but can be overridden:

        ```
        >>> class OtherStyle(Enum):
        ...     ALTERNATE = auto()
        ...     OTHER = auto()
        ...     SOMETHING_ELSE = auto()
        ...     def __repr__(self):
        ...         cls_name = self.__class__.__name__
        ...         return f'{cls_name}.{self.name}'
        ...
        >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
        (OtherStyle.ALTERNATE, 'OtherStyle.ALTERNATE', 'OtherStyle.ALTERNATE')
        ```

    \_\_str\_\_(*self*)[¶](#enum.Enum.__str__ "Link to this definition")
    :   Returns the string used for *str()* calls. By default, returns the
        *Enum* name and member name, but can be overridden:

        ```
        >>> class OtherStyle(Enum):
        ...     ALTERNATE = auto()
        ...     OTHER = auto()
        ...     SOMETHING_ELSE = auto()
        ...     def __str__(self):
        ...         return f'{self.name}'
        ...
        >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
        (<OtherStyle.ALTERNATE: 1>, 'ALTERNATE', 'ALTERNATE')
        ```

    \_\_format\_\_(*self*)[¶](#enum.Enum.__format__ "Link to this definition")
    :   Returns the string used for *format()* and *f-string* calls. By default,
        returns [`__str__()`](#enum.Enum.__str__ "enum.Enum.__str__") return value, but can be overridden:

        ```
        >>> class OtherStyle(Enum):
        ...     ALTERNATE = auto()
        ...     OTHER = auto()
        ...     SOMETHING_ELSE = auto()
        ...     def __format__(self, spec):
        ...         return f'{self.name}'
        ...
        >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
        (<OtherStyle.ALTERNATE: 1>, 'OtherStyle.ALTERNATE', 'ALTERNATE')
        ```

    Note

    Using [`auto`](#enum.auto "enum.auto") with [`Enum`](#enum.Enum "enum.Enum") results in integers of increasing value,
    starting with `1`.

    Changed in version 3.12: Added [Dataclass support](../howto/enum.html#enum-dataclass-support)

*class* enum.IntEnum[¶](#enum.IntEnum "Link to this definition")
:   *IntEnum* is the same as *Enum*, but its members are also integers and can be
    used anywhere that an integer can be used. If any integer operation is performed
    with an *IntEnum* member, the resulting value loses its enumeration status.

    ```
    >>> from enum import IntEnum
    >>> class Number(IntEnum):
    ...     ONE = 1
    ...     TWO = 2
    ...     THREE = 3
    ...
    >>> Number.THREE
    <Number.THREE: 3>
    >>> Number.ONE + Number.TWO
    3
    >>> Number.THREE + 5
    8
    >>> Number.THREE == 3
    True
    ```

    Note

    Using [`auto`](#enum.auto "enum.auto") with [`IntEnum`](#enum.IntEnum "enum.IntEnum") results in integers of increasing
    value, starting with `1`.

    Changed in version 3.11: [`__str__()`](../reference/datamodel.html#object.__str__ "object.__str__") is now `int.__str__()` to
    better support the *replacement of existing constants* use-case.
    [`__format__()`](../reference/datamodel.html#object.__format__ "object.__format__") was already `int.__format__()` for that same reason.

*class* enum.StrEnum[¶](#enum.StrEnum "Link to this definition")
:   *StrEnum* is the same as *Enum*, but its members are also strings and can be used
    in most of the same places that a string can be used. The result of any string
    operation performed on or with a *StrEnum* member is not part of the enumeration.

    Note

    There are places in the stdlib that check for an exact [`str`](stdtypes.html#str "str")
    instead of a [`str`](stdtypes.html#str "str") subclass (i.e. `type(unknown) == str`
    instead of `isinstance(unknown, str)`), and in those locations you
    will need to use `str(StrEnum.member)`.

    Note

    Using [`auto`](#enum.auto "enum.auto") with [`StrEnum`](#enum.StrEnum "enum.StrEnum") results in the lower-cased member
    name as the value.

    Note

    [`__str__()`](../reference/datamodel.html#object.__str__ "object.__str__") is `str.__str__()` to better support the
    *replacement of existing constants* use-case. [`__format__()`](../reference/datamodel.html#object.__format__ "object.__format__") is likewise
    `str.__format__()` for that same reason.

    Added in version 3.11.

*class* enum.Flag[¶](#enum.Flag "Link to this definition")
:   `Flag` is the same as [`Enum`](#enum.Enum "enum.Enum"), but its members support the bitwise
    operators `&` (*AND*), `|` (*OR*), `^` (*XOR*), and `~` (*INVERT*);
    the results of those operations are (aliases of) members of the enumeration.

    \_\_contains\_\_(*self*, *value*)[¶](#enum.Flag.__contains__ "Link to this definition")
    :   Returns *True* if value is in self:

        ```
        >>> from enum import Flag, auto
        >>> class Color(Flag):
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        ...
        >>> purple = Color.RED | Color.BLUE
        >>> white = Color.RED | Color.GREEN | Color.BLUE
        >>> Color.GREEN in purple
        False
        >>> Color.GREEN in white
        True
        >>> purple in white
        True
        >>> white in purple
        False
        ```

    \_\_iter\_\_(self):
    :   Returns all contained non-alias members:

        ```
        >>> list(Color.RED)
        [<Color.RED: 1>]
        >>> list(purple)
        [<Color.RED: 1>, <Color.BLUE: 4>]
        ```

        Added in version 3.11.

    \_\_len\_\_(self):
    :   Returns number of members in flag:

        ```
        >>> len(Color.GREEN)
        1
        >>> len(white)
        3
        ```

        Added in version 3.11.

    \_\_bool\_\_(self):
    :   Returns *True* if any members in flag, *False* otherwise:

        ```
        >>> bool(Color.GREEN)
        True
        >>> bool(white)
        True
        >>> black = Color(0)
        >>> bool(black)
        False
        ```

    \_\_or\_\_(*self*, *other*)[¶](#enum.Flag.__or__ "Link to this definition")
    :   Returns current flag binary or’ed with other:

        ```
        >>> Color.RED | Color.GREEN
        <Color.RED|GREEN: 3>
        ```

    \_\_and\_\_(*self*, *other*)[¶](#enum.Flag.__and__ "Link to this definition")
    :   Returns current flag binary and’ed with other:

        ```
        >>> purple & white
        <Color.RED|BLUE: 5>
        >>> purple & Color.GREEN
        <Color: 0>
        ```

    \_\_xor\_\_(*self*, *other*)[¶](#enum.Flag.__xor__ "Link to this definition")
    :   Returns current flag binary xor’ed with other:

        ```
        >>> purple ^ white
        <Color.GREEN: 2>
        >>> purple ^ Color.GREEN
        <Color.RED|GREEN|BLUE: 7>
        ```

    \_\_invert\_\_(self):
    :   Returns all the flags in *type(self)* that are not in self:

        ```
        >>> ~white
        <Color: 0>
        >>> ~purple
        <Color.GREEN: 2>
        >>> ~Color.RED
        <Color.GREEN|BLUE: 6>
        ```

    \_numeric\_repr\_()[¶](#enum.Flag._numeric_repr_ "Link to this definition")
    :   Function used to format any remaining unnamed numeric values. Default is
        the value’s repr; common choices are [`hex()`](functions.html#hex "hex") and [`oct()`](functions.html#oct "oct").

    Note

    Using [`auto`](#enum.auto "enum.auto") with [`Flag`](#enum.Flag "enum.Flag") results in integers that are powers
    of two, starting with `1`.

    Changed in version 3.11: The *repr()* of zero-valued flags has changed. It
    is now::

    ```
    >>> Color(0)
    <Color: 0>
    ```

*class* enum.IntFlag[¶](#enum.IntFlag "Link to this definition")
:   *IntFlag* is the same as *Flag*, but its members are also integers and can be
    used anywhere that an integer can be used.

    ```
    >>> from enum import IntFlag, auto
    >>> class Color(IntFlag):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    ...
    >>> Color.RED & 2
    <Color: 0>
    >>> Color.RED | 2
    <Color.RED|GREEN: 3>
    ```

    If any integer operation is performed with an *IntFlag* member, the result is
    not an *IntFlag*:

    ```
    >>> Color.RED + 2
    3
    ```

    If a *Flag* operation is performed with an *IntFlag* member and:

    * the result is a valid *IntFlag*: an *IntFlag* is returned
    * the result is not a valid *IntFlag*: the result depends on the *FlagBoundary* setting

    The *repr()* of unnamed zero-valued flags has changed. It is now:

    ```
    >>> Color(0)
    <Color: 0>
    ```

    Note

    Using [`auto`](#enum.auto "enum.auto") with [`IntFlag`](#enum.IntFlag "enum.IntFlag") results in integers that are powers
    of two, starting with `1`.

    Changed in version 3.11: [`__str__()`](../reference/datamodel.html#object.__str__ "object.__str__") is now `int.__str__()` to better support the
    *replacement of existing constants* use-case. [`__format__()`](../reference/datamodel.html#object.__format__ "object.__format__") was
    already `int.__format__()` for that same reason.

    Inversion of an `IntFlag` now returns a positive value that is the
    union of all flags not in the given flag, rather than a negative value.
    This matches the existing [`Flag`](#enum.Flag "enum.Flag") behavior.

*class* enum.ReprEnum[¶](#enum.ReprEnum "Link to this definition")
:   `ReprEnum` uses the [`repr()`](#enum.Enum.__repr__ "enum.Enum.__repr__") of [`Enum`](#enum.Enum "enum.Enum"),
    but the [`str()`](stdtypes.html#str "str") of the mixed-in data type:

    * `int.__str__()` for [`IntEnum`](#enum.IntEnum "enum.IntEnum") and [`IntFlag`](#enum.IntFlag "enum.IntFlag")
    * `str.__str__()` for [`StrEnum`](#enum.StrEnum "enum.StrEnum")

    Inherit from `ReprEnum` to keep the [`str()`](stdtypes.html#str "str") / [`format()`](functions.html#format "format")
    of the mixed-in data type instead of using the
    [`Enum`](#enum.Enum "enum.Enum")-default [`str()`](#enum.Enum.__str__ "enum.Enum.__str__").

    Added in version 3.11.

*class* enum.EnumCheck[¶](#enum.EnumCheck "Link to this definition")
:   *EnumCheck* contains the options used by the [`verify()`](#enum.verify "enum.verify") decorator to ensure
    various constraints; failed constraints result in a [`ValueError`](exceptions.html#ValueError "ValueError").

    UNIQUE[¶](#enum.EnumCheck.UNIQUE "Link to this definition")
    :   Ensure that each value has only one name:

        ```
        >>> from enum import Enum, verify, UNIQUE
        >>> @verify(UNIQUE)
        ... class Color(Enum):
        ...     RED = 1
        ...     GREEN = 2
        ...     BLUE = 3
        ...     CRIMSON = 1
        Traceback (most recent call last):
        ...
        ValueError: aliases found in <enum 'Color'>: CRIMSON -> RED
        ```

    CONTINUOUS[¶](#enum.EnumCheck.CONTINUOUS "Link to this definition")
    :   Ensure that there are no missing values between the lowest-valued member
        and the highest-valued member:

        ```
        >>> from enum import Enum, verify, CONTINUOUS
        >>> @verify(CONTINUOUS)
        ... class Color(Enum):
        ...     RED = 1
        ...     GREEN = 2
        ...     BLUE = 5
        Traceback (most recent call last):
        ...
        ValueError: invalid enum 'Color': missing values 3, 4
        ```

    NAMED\_FLAGS[¶](#enum.EnumCheck.NAMED_FLAGS "Link to this definition")
    :   Ensure that any flag groups/masks contain only named flags – useful when
        values are specified instead of being generated by [`auto()`](#enum.auto "enum.auto"):

        ```
        >>> from enum import Flag, verify, NAMED_FLAGS
        >>> @verify(NAMED_FLAGS)
        ... class Color(Flag):
        ...     RED = 1
        ...     GREEN = 2
        ...     BLUE = 4
        ...     WHITE = 15
        ...     NEON = 31
        Traceback (most recent call last):
        ...
        ValueError: invalid Flag 'Color': aliases WHITE and NEON are missing combined values of 0x18 [use enum.show_flag_values(value) for details]
        ```

    Note

    CONTINUOUS and NAMED\_FLAGS are designed to work with integer-valued members.

    Added in version 3.11.

*class* enum.FlagBoundary[¶](#enum.FlagBoundary "Link to this definition")
:   *FlagBoundary* controls how out-of-range values are handled in *Flag* and its
    subclasses.

    STRICT[¶](#enum.FlagBoundary.STRICT "Link to this definition")
    :   Out-of-range values cause a [`ValueError`](exceptions.html#ValueError "ValueError") to be raised. This is the
        default for [`Flag`](#enum.Flag "enum.Flag"):

        ```
        >>> from enum import Flag, STRICT, auto
        >>> class StrictFlag(Flag, boundary=STRICT):
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        ...
        >>> StrictFlag(2**2 + 2**4)
        Traceback (most recent call last):
        ...
        ValueError: <flag 'StrictFlag'> invalid value 20
            given 0b0 10100
          allowed 0b0 00111
        ```

    CONFORM[¶](#enum.FlagBoundary.CONFORM "Link to this definition")
    :   Out-of-range values have invalid values removed, leaving a valid *Flag*
        value:

        ```
        >>> from enum import Flag, CONFORM, auto
        >>> class ConformFlag(Flag, boundary=CONFORM):
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        ...
        >>> ConformFlag(2**2 + 2**4)
        <ConformFlag.BLUE: 4>
        ```

    EJECT[¶](#enum.FlagBoundary.EJECT "Link to this definition")
    :   Out-of-range values lose their *Flag* membership and revert to [`int`](functions.html#int "int").

        ```
        >>> from enum import Flag, EJECT, auto
        >>> class EjectFlag(Flag, boundary=EJECT):
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        ...
        >>> EjectFlag(2**2 + 2**4)
        20
        ```

    KEEP[¶](#enum.FlagBoundary.KEEP "Link to this definition")
    :   Out-of-range values are kept, and the *Flag* membership is kept.
        This is the default for [`IntFlag`](#enum.IntFlag "enum.IntFlag"):

        ```
        >>> from enum import Flag, KEEP, auto
        >>> class KeepFlag(Flag, boundary=KEEP):
        ...     RED = auto()
        ...     GREEN = auto()
        ...     BLUE = auto()
        ...
        >>> KeepFlag(2**2 + 2**4)
        <KeepFlag.BLUE|16: 20>
        ```

Added in version 3.11.

---

### Supported `__dunder__` names[¶](#supported-dunder-names "Link to this heading")

[`__members__`](#enum.EnumType.__members__ "enum.EnumType.__members__") is a read-only ordered mapping of `member_name`:`member`
items. It is only available on the class.

[`__new__()`](#enum.Enum.__new__ "enum.Enum.__new__"), if specified, must create and return the enum members; it is
also a very good idea to set the member’s `_value_` appropriately. Once
all the members are created it is no longer used.

### Supported `_sunder_` names[¶](#supported-sunder-names "Link to this heading")

* [`_name_`](#enum.Enum._name_ "enum.Enum._name_") – name of the member
* [`_value_`](#enum.Enum._value_ "enum.Enum._value_") – value of the member; can be set in `__new__`
* [`_missing_()`](#enum.Enum._missing_ "enum.Enum._missing_") – a lookup function used when a value is not found;
  may be overridden
* [`_ignore_`](#enum.Enum._ignore_ "enum.Enum._ignore_") – a list of names, either as a [`list`](stdtypes.html#list "list") or a
  [`str`](stdtypes.html#str "str"), that will not be transformed into members, and will be removed
  from the final class
* [`_order_`](#enum.Enum._order_ "enum.Enum._order_") – no longer used, kept for backward
  compatibility (class attribute, removed during class creation)
* [`_generate_next_value_()`](#enum.Enum._generate_next_value_ "enum.Enum._generate_next_value_") – used to get an appropriate value for
  an enum member; may be overridden

  Note

  For standard [`Enum`](#enum.Enum "enum.Enum") classes the next value chosen is the last value seen
  incremented by one.

  For [`Flag`](#enum.Flag "enum.Flag") classes the next value chosen will be the next highest
  power-of-two, regardless of the last value seen.

Added in version 3.6: `_missing_`, `_order_`, `_generate_next_value_`

Added in version 3.7: `_ignore_`

---

## Utilities and Decorators[¶](#utilities-and-decorators "Link to this heading")

*class* enum.auto[¶](#enum.auto "Link to this definition")
:   *auto* can be used in place of a value. If used, the *Enum* machinery will
    call an *Enum*’s [`_generate_next_value_()`](#enum.Enum._generate_next_value_ "enum.Enum._generate_next_value_") to get an appropriate value.
    For *Enum* and *IntEnum* that appropriate value will be the last value plus
    one; for *Flag* and *IntFlag* it will be the first power-of-two greater
    than the highest value; for *StrEnum* it will be the lower-cased version of
    the member’s name. Care must be taken if mixing *auto()* with manually
    specified values.

    *auto* instances are only resolved when at the top level of an assignment:

    * `FIRST = auto()` will work (auto() is replaced with `1`);
    * `SECOND = auto(), -2` will work (auto is replaced with `2`, so `2, -2` is
      used to create the `SECOND` enum member;
    * `THREE = [auto(), -3]` will *not* work (`<auto instance>, -3` is used to
      create the `THREE` enum member)

    Changed in version 3.11.1: In prior versions, `auto()` had to be the only thing
    on the assignment line to work properly.

    `_generate_next_value_` can be overridden to customize the values used by
    *auto*.

    Note

    in 3.13 the default `_generate_next_value_` will always return
    the highest member value incremented by 1, and will fail if any
    member is an incompatible type.

@enum.property[¶](#enum.property "Link to this definition")
:   A decorator similar to the built-in *property*, but specifically for
    enumerations. It allows member attributes to have the same names as members
    themselves.

    Note

    the *property* and the member must be defined in separate classes;
    for example, the *value* and *name* attributes are defined in the
    *Enum* class, and *Enum* subclasses can define members with the
    names `value` and `name`.

    Added in version 3.11.

@enum.unique[¶](#enum.unique "Link to this definition")
:   A [`class`](../reference/compound_stmts.html#class) decorator specifically for enumerations. It searches an
    enumeration’s [`__members__`](#enum.EnumType.__members__ "enum.EnumType.__members__"), gathering any aliases it finds; if any are
    found [`ValueError`](exceptions.html#ValueError "ValueError") is raised with the details:

    ```
    >>> from enum import Enum, unique
    >>> @unique
    ... class Mistake(Enum):
    ...     ONE = 1
    ...     TWO = 2
    ...     THREE = 3
    ...     FOUR = 3
    ...
    Traceback (most recent call last):
    ...
    ValueError: duplicate values found in <enum 'Mistake'>: FOUR -> THREE
    ```

@enum.verify[¶](#enum.verify "Link to this definition")
:   A [`class`](../reference/compound_stmts.html#class) decorator specifically for enumerations. Members from
    [`EnumCheck`](#enum.EnumCheck "enum.EnumCheck") are used to specify which constraints should be checked
    on the decorated enumeration.

    Added in version 3.11.

@enum.member[¶](#enum.member "Link to this definition")
:   A decorator for use in enums: its target will become a member.

    Added in version 3.11.

@enum.nonmember[¶](#enum.nonmember "Link to this definition")
:   A decorator for use in enums: its target will not become a member.

    Added in version 3.11.

@enum.global\_enum[¶](#enum.global_enum "Link to this definition")
:   A decorator to change the [`str()`](stdtypes.html#str "str") and [`repr()`](functions.html#repr "repr") of an enum
    to show its members as belonging to the module instead of its class.
    Should only be used when the enum members are exported
    to the module global namespace (see [`re.RegexFlag`](re.html#re.RegexFlag "re.RegexFlag") for an example).

    Added in version 3.11.

enum.show\_flag\_values(*value*)[¶](#enum.show_flag_values "Link to this definition")
:   Return a list of all power-of-two integers contained in a flag *value*.

    Added in version 3.11.

---

## Notes[¶](#notes "Link to this heading")

[`IntEnum`](#enum.IntEnum "enum.IntEnum"), [`StrEnum`](#enum.StrEnum "enum.StrEnum"), and [`IntFlag`](#enum.IntFlag "enum.IntFlag")

> These three enum types are designed to be drop-in replacements for existing
> integer- and string-based values; as such, they have extra limitations:
>
> * `__str__` uses the value and not the name of the enum member
> * `__format__`, because it uses `__str__`, will also use the value of
>   the enum member instead of its name
>
> If you do not need/want those limitations, you can either create your own
> base class by mixing in the `int` or `str` type yourself:
>
> ```
> >>> from enum import Enum
> >>> class MyIntEnum(int, Enum):
> ...     pass
> ```
>
> or you can reassign the appropriate [`str()`](stdtypes.html#str "str"), etc., in your enum:
>
> ```
> >>> from enum import Enum, IntEnum
> >>> class MyIntEnum(IntEnum):
> ...     __str__ = Enum.__str__
> ```

### [Table of Contents](../contents.html)

* [`enum` — Support for enumerations](#)
  + [Module Contents](#module-contents)
  + [Data Types](#data-types)
    - [Supported `__dunder__` names](#supported-dunder-names)
    - [Supported `_sunder_` names](#supported-sunder-names)
  + [Utilities and Decorators](#utilities-and-decorators)
  + [Notes](#notes)

#### Previous topic

[`reprlib` — Alternate `repr()` implementation](reprlib.html "previous chapter")

#### Next topic

[`graphlib` — Functionality to operate with graph-like structures](graphlib.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/enum.rst)

«

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](graphlib.html "graphlib — Functionality to operate with graph-like structures") |
* [previous](reprlib.html "reprlib — Alternate repr() implementation") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Data Types](datatypes.html) »
* `enum` — Support for enumerations
* |
* Theme
  Auto
  Light
  Dark
   |

© [Copyright](../copyright.html) 2001-2026, Python Software Foundation.
  
This page is licensed under the Python Software Foundation License Version 2.
  
Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License.
  
See [History and License](/license.html) for more information.  
  
The Python Software Foundation is a non-profit corporation.
[Please donate.](https://www.python.org/psf/donations/)
  
  
Last updated on Mar 07, 2026 (17:44 UTC).
[Found a bug](/bugs.html)?
  
Created using [Sphinx](https://www.sphinx-doc.org/) 8.2.3.