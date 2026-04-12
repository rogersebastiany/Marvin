# Pydantic v2 — Models, Fields, Validators, JSON Schema, Types


---

## 1. Models

API Documentation

[`pydantic.main.BaseModel`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel)

One of the primary ways of defining schema in Pydantic is via models. Models are simply classes which inherit from
[`BaseModel`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel) and define fields as annotated attributes.

You can think of models as similar to structs in languages like C, or as the requirements of a single endpoint
in an API.

Models share many similarities with Python’s [dataclasses](https://docs.python.org/3/library/dataclasses.html#module-dataclasses), but have been designed with some subtle-yet-important
differences that streamline certain workflows related to validation, serialization, and JSON schema generation.
You can find more discussion of this in the [Dataclasses](/docs/validation/latest/concepts/dataclasses) section of the docs.

Untrusted data can be passed to a model and, after parsing and validation, Pydantic guarantees that the fields
of the resultant model instance will conform to the field types defined on the model.

## Basic model usage

```
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
  id: int
  name: str = 'Jane Doe'

  model_config = ConfigDict(str_max_length=10)  # (1)
```

Pydantic models support a variety of [configuration values](/docs/validation/latest/concepts/config)
(see [here](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict) for the available configuration values).

In this example, `User` is a model with two fields:

* `id`, which is an integer (defined using the [`int`](https://docs.python.org/3/library/functions.html#int) type) and is required
* `name`, which is a string (defined using the [`str`](https://docs.python.org/3/library/stdtypes.html#str) type) and is not required (it has a default value).

The documentation on [types](/docs/validation/latest/concepts/types) expands on the supported types.

Fields can be customized in a number of ways using the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function.
See the [documentation on fields](/docs/validation/latest/concepts/fields) for more information.

The model can then be instantiated:

```
user = User(id='123')
```

`user` is an instance of `User`. Initialization of the object will perform all parsing and validation.
If no [`ValidationError`](/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError) exception is raised,
you know the resulting model instance is valid.

Fields of a model can be accessed as normal attributes of the `user` object:

```
assert user.name == 'Jane Doe'  # (1)
assert user.id == 123  # (2)
assert isinstance(user.id, int)
```

`name` wasn't set when `user` was initialized, so the default value was used.
The [`model_fields_set`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_fields_set) attribute can be
inspected to check the field names explicitly set during instantiation.

Note that the string `'123'` was coerced to an integer and its value is `123`.
More details on Pydantic's coercion logic can be found in the [data conversion](#data-conversion) section.

The model instance can be serialized using the [`model_dump()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump) method:

```
assert user.model_dump() == {'id': 123, 'name': 'Jane Doe'}
```

Calling [dict](https://docs.python.org/3/reference/expressions.html#dict) on the instance will also provide a dictionary, but nested fields will not be
recursively converted into dictionaries. [`model_dump()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump) also
provides numerous arguments to customize the serialization result.

By default, models are mutable and field values can be changed through attribute assignment:

```
user.id = 321
assert user.id == 321
```

### Model methods and properties

The example above only shows the tip of the iceberg of what models can do.
Model classes possess the following methods and attributes:

* [`model_validate()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate): Validates the given object against the Pydantic model. See [Validating data](#validating-data).
* [`model_validate_json()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json): Validates the given JSON data against the Pydantic model. See
  [Validating data](#validating-data).
* [`model_construct()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_construct): Creates models without running validation. See
  [Creating models without validation](#creating-models-without-validation).
* [`model_dump()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump): Returns a dictionary of the model’s fields and values. See
  [Serialization](/docs/validation/latest/concepts/serialization#python-mode).
* [`model_dump_json()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json): Returns a JSON string representation of [`model_dump()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump). See [Serialization](/docs/validation/latest/concepts/serialization#json-mode).
* [`model_copy()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_copy): Returns a copy (by default, shallow copy) of the model. See
  [Model copy](#model-copy).
* [`model_json_schema()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema): Returns a jsonable dictionary representing the model’s JSON Schema. See [JSON Schema](/docs/validation/latest/concepts/json_schema).
* [`model_fields`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_fields): A mapping between field names and their definitions ([`FieldInfo`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo) instances).
* [`model_computed_fields`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_computed_fields): A mapping between computed field names and their definitions ([`ComputedFieldInfo`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo) instances).
* [`model_parametrized_name()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_parametrized_name): Computes the class name for parametrizations of generic classes.
* [`model_post_init()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_post_init): Performs additional actions after the model is instantiated and all field validators are applied.
* [`model_rebuild()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild): Rebuilds the model schema, which also supports building recursive generic models.
  See [Rebuilding model schema](#rebuilding-model-schema).

Model instances possess the following attributes:

* [`model_extra`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_extra): The extra fields set during validation.
* [`model_fields_set`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_fields_set): The set of fields which were explicitly provided when the model was initialized.

## Data conversion

Pydantic may cast input data to force it to conform to model field types,
and in some cases this may result in a loss of information.
For example:

```
from pydantic import BaseModel

class Model(BaseModel):
    a: int
    b: float
    c: str

print(Model(a=3.000, b='2.72', c=b'binary data').model_dump())
#> {'a': 3, 'b': 2.72, 'c': 'binary data'}
```

This is a deliberate decision of Pydantic, and is frequently the most useful approach. See
[this issue](https://github.com/pydantic/pydantic/issues/578) for a longer discussion on the subject.

Nevertheless, Pydantic provides a [strict mode](/docs/validation/latest/concepts/strict_mode), where no data conversion is performed.
Values must be of the same type as the declared field type.

This is also the case for collections. In most cases, you shouldn’t make use of abstract container classes
and just use a concrete type, such as [`list`](https://docs.python.org/3/glossary.html#term-list):

```
from pydantic import BaseModel

class Model(BaseModel):
  items: list[int]  # (1)

print(Model(items=(1, 2, 3)))
#> items=[1, 2, 3]
```

In this case, you might be tempted to use the abstract [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence) type
to allow both lists and tuples. But Pydantic takes care of converting the tuple input to a list, so
in most cases this isn't necessary.

Besides, using these abstract types can also lead to [poor validation performance](/docs/validation/latest/concepts/performance#sequence-vs-list-or-tuple-with-mapping-vs-dict), and in general using concrete container types
will avoid unnecessary checks.

## Extra data

By default, Pydantic models **won’t error when you provide extra data**, and these values will simply be ignored:

```
from pydantic import BaseModel

class Model(BaseModel):
    x: int

m = Model(x=1, y='a')
assert m.model_dump() == {'x': 1}
```

The [`extra`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra) configuration value can be used to control this behavior:

```
from pydantic import BaseModel, ConfigDict

class Model(BaseModel):
  x: int

  model_config = ConfigDict(extra='allow')

m = Model(x=1, y='a')  # (1)
assert m.model_dump() == {'x': 1, 'y': 'a'}
assert m.```

If [`extra`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra) was set to `'forbid'`, this would fail.

The configuration can take three values:

* `'ignore'`: Providing extra data is ignored (the default).
* `'forbid'`: Providing extra data is not permitted.
* `'allow'`: Providing extra data is allowed and stored in the `__pydantic_extra__` dictionary attribute.
  The `__pydantic_extra__` can explicitly be annotated to provide validation for extra fields.

The validation methods (e.g. [`model_validate()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate)) have an optional `extra` argument
that will override the `extra` configuration value of the model for that validation call.

For more details, refer to the [`extra`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra) API documentation.

Pydantic dataclasses also support extra data (see the [dataclass configuration](/docs/validation/latest/concepts/dataclasses#dataclass-config) section).

## Nested models

More complex hierarchical data structures can be defined using models themselves as types in annotations.

```
from typing import Optional

from pydantic import BaseModel

class Foo(BaseModel):
    count: int
    size: Optional[float] = None

class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'

class Spam(BaseModel):
    foo: Foo
    bars: list[Bar]

m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
print(m)
"""
foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'), Bar(apple='x2', banana='y')]
"""
print(m.model_dump())
"""
{
    'foo': {'count': 4, 'size': None},
    'bars': [{'apple': 'x1', 'banana': 'y'}, {'apple': 'x2', 'banana': 'y'}],
}
"""
```

Self-referencing models are supported. For more details, see the documentation related to
[forward annotations](/docs/validation/latest/concepts/forward_annotations#self-referencing-or-recursive-models).

## Rebuilding model schema

When you define a model class in your code, Pydantic will analyze the body of the class to collect a variety of information
required to perform validation and serialization, gathered in a core schema. Notably, the model’s type annotations are evaluated to
understand the valid types for each field (more information can be found in the [Architecture](/docs/validation/latest/internals/architecture) documentation).
However, it might be the case that annotations refer to symbols not defined when the model class is being created.
To circumvent this issue, the [`model_rebuild()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild) method can be used:

```
from pydantic import BaseModel, PydanticUserError

class Foo(BaseModel):
  x: 'Bar'  # (1)

try:
  Foo.model_json_schema()
except PydanticUserError as e:
  print(e)
  """
  `Foo` is not fully defined; you should define `Bar`, then call `Foo.model_rebuild()`.

  For further information visit https://errors.pydantic.dev/2/u/class-not-fully-defined
  """

class Bar(BaseModel):
  pass

Foo.model_rebuild()
print(Foo.model_json_schema())
"""
{
  '$defs': {'Bar': {'properties': {}, 'title': 'Bar', 'type': 'object'}},
  'properties': {'x': {'$ref': '#/$defs/Bar'}},
  'required': ['x'],
  'title': 'Foo',
  'type': 'object',
}
"""
```

`Bar` is not yet defined when the `Foo` class is being created. For this reason,
a [forward annotation](/docs/validation/latest/concepts/forward_annotations) is being used.

Pydantic tries to determine when this is necessary automatically and error if it wasn’t done, but you may want to
call [`model_rebuild()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild) proactively when dealing with recursive models or generics.

In V2, [`model_rebuild()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild) replaced `update_forward_refs()` from V1. There are some slight differences with the new behavior.
The biggest change is that when calling [`model_rebuild()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild) on the outermost model, it builds a core schema used for validation of the
whole model (nested models and all), so all types at all levels need to be ready before [`model_rebuild()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild) is called.

## Validating data

Pydantic can validate data in three different modes: *Python*, *JSON* and *strings*.

The *Python* mode gets used when using:

* The `__init__()` model constructor. Field values must be provided using keyword arguments.
* [`model_validate()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate): data can be provided either as a dictionary,
  or as a model instance (by default, instances are assumed to be valid; see the [`revalidate_instances`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.revalidate_instances)
  setting). [Arbitrary objects](#arbitrary-class-instances) can also be provided if explicitly enabled.

The *JSON* and *strings* modes can be used with dedicated methods:

* [`model_validate_json()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json): data is validated as a JSON string or `bytes` object.
  If your incoming data is a JSON payload, this is generally considered faster (instead of manually parsing the data as a dictionary).
  Learn more about JSON parsing in the [JSON](/docs/validation/latest/concepts/json) documentation.
* [`model_validate_strings()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings): data is validated as a dictionary (can be nested) with
  string keys and values and validates the data in JSON mode so that said strings can be coerced into the correct types.

Compared to using the model constructor, it is possible to control several validation parameters when using the `model_validate_*()` methods
([strictness](/docs/validation/latest/concepts/strict_mode), [extra data](#extra-data), [validation context](/docs/validation/latest/concepts/validators#validation-context), etc.).

```
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None

m = User.model_validate({'id': 123, 'name': 'James'})
print(m)
#> id=123 name='James' signup_ts=None

try:
    m = User.model_validate_json('{"id": 123, "name": 123}')
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    name
      Input should be a valid string [type=string_type, input_value=123, input_type=int]
    """

m = User.model_validate_strings({'id': '123', 'name': 'James'})
print(m)
#> id=123 name='James' signup_ts=None

m = User.model_validate_strings(
    {'id': '123', 'name': 'James', 'signup_ts': '2024-04-01T12:00:00'}
)
print(m)
#> id=123 name='James' signup_ts=datetime.datetime(2024, 4, 1, 12, 0)

try:
    m = User.model_validate_strings(
        {'id': '123', 'name': 'James', 'signup_ts': '2024-04-01'}, strict=True
    )
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    signup_ts
      Input should be a valid datetime, invalid datetime separator, expected `T`, `t`, `_` or space [type=datetime_parsing, input_value='2024-04-01', input_type=str]
    """
```

### Creating models without validation

Pydantic also provides the [`model_construct()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_construct) method, which allows models to be created **without validation**.
This can be useful in at least a few cases:

* when working with complex data that is already known to be valid (for performance reasons)
* when one or more of the validator functions are non-idempotent
* when one or more of the validator functions have side effects that you don’t want to be triggered.

Note that for [root models](#rootmodel-and-custom-root-types), the root value can be passed to
[`model_construct()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_construct) positionally, instead of using a keyword argument.

Here are some additional notes on the behavior of [`model_construct()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_construct):

* When we say “no validation is performed” — this includes converting dictionaries to model instances. So if you have a field
  referring to a model type, you will need to convert the inner dictionary to a model yourself.
* If you do not pass keyword arguments for fields with defaults, the default values will still be used.
* For models with private attributes, the `__pydantic_private__` dictionary will be populated the same as it would be when
  creating the model with validation.
* No `__init__` method from the model or any of its parent classes will be called, even when a custom `__init__` method is defined.

### Defining a custom `__init__()`

Pydantic provides a default `__init__()` implementation for Pydantic models, that is called *only* when using the model constructor
(and not with the `model_validate_*()` methods). This implementation delegates validation to `pydantic-core`.

However, it is possible to define a custom `__init__()` on your models. In this case, it will be called unconditionally from all the
[validation methods](#validating-data), without performing validation (and so you should call `super().__init__(**kwargs)` in your implementation).

Defining a custom `__init__()` is not recommended, as all the validation parameters ([strictness](/docs/validation/latest/concepts/strict_mode),
[extra data behavior](#extra-data), [validation context](/docs/validation/latest/concepts/validators#validation-context)) will be lost. If you need to perform
actions after the model was initialized, you can make use of *after* [field](/docs/validation/latest/concepts/validators#field-after-validator) or
[model](/docs/validation/latest/concepts/validators#model-after-validator) validators, or define a [`model_post_init()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_post_init) implementation:

```
import logging
from typing import Any

from pydantic import BaseModel

class MyModel(BaseModel):
    id: int

    def model_post_init(self, context: Any) -> None:
        logging.info("Model initialized with id %d", self.id)
```

## Error handling

Pydantic will raise a [`ValidationError`](/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError) exception whenever it finds an error in the data it’s validating.

A single exception will be raised regardless of the number of errors found, and that validation error
will contain information about all of the errors and how they happened.

See [Error Handling](/docs/validation/latest/errors/errors) for details on standard and custom errors.

As a demonstration:

```
from pydantic import BaseModel, ValidationError

class Model(BaseModel):
    list_of_ints: list[int]
    a_float: float

data = {
    'list_of_ints': ['1', 2, 'bad'],
    'a_float': 'not a float',
}

try:
    Model(**data)
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    list_of_ints.2
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]
    a_float
      Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='not a float', input_type=str]
    """
```

## Arbitrary class instances

(Formerly known as “ORM Mode”/`from_orm()`).

When using the [`model_validate()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate) method, Pydantic can also validate arbitrary objects,
by getting attributes on the object corresponding the field names. One common application of this functionality is integration with
object-relational mappings (ORMs).

This feature need to be manually enabled, either by setting the [`from_attributes`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.from_attributes)
configuration value, or by using the `from_attributes` parameter on [`model_validate()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate).

The example here uses [SQLAlchemy](https://www.sqlalchemy.org/), but the same approach should work for any ORM.

```
from typing import Annotated

from sqlalchemy import ARRAY, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pydantic import BaseModel, ConfigDict, StringConstraints

class Base(DeclarativeBase):
    pass

class CompanyOrm(Base):
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    public_key: Mapped[str] = mapped_column(
        String(20), index=True, nullable=False, unique=True
    )
    domains: Mapped[list[str]] = mapped_column(ARRAY(String(255)))

class CompanyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    public_key: Annotated[str, StringConstraints(max_length=20)]
    domains: list[Annotated[str, StringConstraints(max_length=255)]]

co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    domains=['example.com', 'foobar.com'],
)
print(co_orm)
#> <__main__.CompanyOrm object at 0x0123456789ab>
co_model = CompanyModel.model_validate(co_orm)
print(co_model)
#> id=123 public_key='foobar' domains=['example.com', 'foobar.com']
```

### Nested attributes

When using attributes to validate models, model instances will be created from both top-level attributes and
deeper-nested attributes as appropriate.

Here is an example demonstrating the principle:

```
from pydantic import BaseModel, ConfigDict

class PetCls:
    def __init__(self, *, name: str) -> None:
        self.name = name

class PersonCls:
    def __init__(self, *, name: str, pets: list[PetCls]) -> None:
        self.name = name
        self.pets = pets

class Pet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    pets: list[Pet]

bones = PetCls(name='Bones')
orion = PetCls(name='Orion')
anna = PersonCls(name='Anna', pets=[bones, orion])
anna_model = Person.model_validate(anna)
print(anna_model)
#> name='Anna' pets=[Pet(name='Bones'), Pet(name='Orion')]
```

## Model copy

API Documentation

[`pydantic.main.BaseModel.model_copy`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_copy)

The [`model_copy()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_copy) method allows models to be duplicated (with optional updates),
which is particularly useful when working with frozen models.

```
from pydantic import BaseModel

class BarModel(BaseModel):
    whatever: int

class FooBarModel(BaseModel):
    banana: float
    foo: str
    bar: BarModel

m = FooBarModel(banana=3.14, foo='hello', bar={'whatever': 123})

print(m.model_copy(update={'banana': 0}))
#> banana=0 foo='hello' bar=BarModel(whatever=123)

# normal copy gives the same object reference for bar:
print(id(m.bar) == id(m.model_copy().bar))
#> True
# deep copy gives a new object reference for `bar`:
print(id(m.bar) == id(m.model_copy(deep=True).bar))
#> False
```

## Generic models

Pydantic supports the creation of generic models to make it easier to reuse a common model structure. Both the new
[type parameter syntax](https://docs.python.org/3/reference/compound_stmts.html#type-params) (introduced by [PEP 695](https://peps.python.org/pep-0695/) in Python 3.12)
and the old syntax are supported (refer to
[the Python documentation](https://docs.python.org/3/library/typing.html#building-generic-types-and-type-aliases)
for more details).

Here is an example using a generic Pydantic model to create an easily-reused HTTP response payload wrapper:

```
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

DataT = TypeVar('DataT')  # (1)

class DataModel(BaseModel):
  number: int

class Response(BaseModel, Generic[DataT]):  # (2)
  data: DataT  # (3)

print(Response[int](data=1))
#> data=1
print(Response[str](data='value'))
#> data='value'
print(Response[str](data='value').model_dump())
#> {'data': 'value'}

data = DataModel(number=1)
print(Response[DataModel](data=data).model_dump())
#> {'data': {'number': 1}}
try:
  Response[int](data='value')
except ValidationError as e:
  print(e)
  """
  1 validation error for Response[int]
  data
    Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='value', input_type=str]
  """
```

Declare one or more [type variables](https://docs.python.org/3/library/typing.html#typing.TypeVar) to use to parameterize your model.

Declare a Pydantic model that inherits from [`BaseModel`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel) and [`typing.Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)
(in this specific order), and add the list of type variables you declared previously as parameters to the
[`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic) parent.

Use the type variables as annotations where you will want to replace them with other types.

Any [configuration](/docs/validation/latest/concepts/config), [validation](/docs/validation/latest/concepts/validators) or [serialization](/docs/validation/latest/concepts/serialization) logic
set on the generic model will also be applied to the parametrized classes, in the same way as when inheriting from
a model class. Any custom methods or attributes will also be inherited.

Generic models also integrate properly with type checkers, so you get all the type checking
you would expect if you were to declare a distinct type for each parametrization.

To inherit from a generic model and preserve the fact that it is generic, the subclass must also inherit from
[`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic):

```
from typing import Generic, TypeVar

from pydantic import BaseModel

TypeX = TypeVar('TypeX')

class BaseClass(BaseModel, Generic[TypeX]):
    X: TypeX

class ChildClass(BaseClass[TypeX], Generic[TypeX]):
    pass

# Parametrize `TypeX` with `int`:
print(ChildClass[int](X=1))
#> X=1
```

You can also create a generic subclass of a model that partially or fully replaces the type variables in the
superclass:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

TypeX = TypeVar('TypeX')
TypeY = TypeVar('TypeY')
TypeZ = TypeVar('TypeZ')

class BaseClass(BaseModel, Generic[TypeX, TypeY]):
    x: TypeX
    y: TypeY

class ChildClass(BaseClass[int, TypeY], Generic[TypeY, TypeZ]):
    z: TypeZ

# Parametrize `TypeY` with `str`:
print(ChildClass[str, int](x='1', y='y', z='3'))
#> x=1 y='y' z=3
```

If the name of the concrete subclasses is important, you can also override the default name generation
by overriding the [`model_parametrized_name()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_parametrized_name) method:

```
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar('DataT')

class Response(BaseModel, Generic[DataT]):
    data: DataT

    @classmethod
    def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:
        return f'{params[0].__name__.title()}Response'

print(repr(Response[int](data=1)))
#> IntResponse(data=1)
print(repr(Response[str](data='a')))
#> StrResponse(data='a')
```

You can use parametrized generic models as types in other models:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    content: T

class Product(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    id: int
    product: ResponseModel[Product]

product = Product(name='Apple', price=0.5)
response = ResponseModel[Product](content=product)
order = Order(id=1, product=response)
print(repr(order))
"""
Order(id=1, product=ResponseModel[Product](content=Product(name='Apple', price=0.5)))
"""
```

Using the same type variable in nested models allows you to enforce typing relationships at different points in your model:

```
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar('T')

class InnerT(BaseModel, Generic[T]):
  inner: T

class OuterT(BaseModel, Generic[T]):
  outer: T
  nested: InnerT[T]

nested = InnerT[int](inner=1)
print(OuterT[int](outer=1, nested=nested))
#> outer=1 nested=InnerT[int](inner=1)
try:
  print(OuterT[int](outer='a', nested=InnerT(inner='a')))  # (1)
except ValidationError as e:
  print(e)
  """
  2 validation errors for OuterT[int]
  outer
    Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
  nested.inner
    Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
  """
```

The `OuterT` model is parametrized with `int`, but the data associated with the the `T` annotations during validation is of type `str`, leading to validation errors.

Implementation Details

When using nested generic models, Pydantic sometimes performs revalidation in an attempt to produce the most intuitive validation result.
Specifically, if you have a field of type `GenericModel[SomeType]` and you validate data like `GenericModel[SomeCompatibleType]` against this field,
we will inspect the data, recognize that the input data is sort of a “loose” subclass of `GenericModel`, and revalidate the contained `SomeCompatibleType` data.

This adds some validation overhead, but makes things more intuitive for cases like that shown below.

```
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class GenericModel(BaseModel, Generic[T]):
    a: T

class Model(BaseModel):
    inner: GenericModel[Any]

print(repr(Model.model_validate(Model(inner=GenericModel[int](a=1)))))
#> Model(inner=GenericModel[Any](a=1))
```

Note, validation will still fail if you, for example are validating against `GenericModel[int]` and pass in an instance `GenericModel[str](a='not an int')`.

It’s also worth noting that this pattern will re-trigger any custom validation as well, like additional model validators and the like.
Validators will be called once on the first pass, validating directly against `GenericModel[Any]`. That validation fails, as `GenericModel[int]` is not a subclass of `GenericModel[Any]`. This relates to the warning above about the complications of using parametrized generics in `isinstance()` and `issubclass()` checks.
Then, the validators will be called again on the second pass, during more lax force-revalidation phase, which succeeds.
To better understand this consequence, see below:

```
from typing import Any, Generic, Self, TypeVar

from pydantic import BaseModel, model_validator

T = TypeVar('T')

class GenericModel(BaseModel, Generic[T]):
    a: T

    @model_validator(mode='after')
    def validate_after(self: Self) -> Self:
        print('after validator running custom validation...')
        return self

class Model(BaseModel):
    inner: GenericModel[Any]

m = Model.model_validate(Model(inner=GenericModel[int](a=1)))
#> after validator running custom validation...
#> after validator running custom validation...
print(repr(m))
#> Model(inner=GenericModel[Any](a=1))
```

### Validation of unparametrized type variables

When leaving type variables unparametrized, Pydantic treats generic models similarly to how it treats built-in generic
types like [`list`](https://docs.python.org/3/glossary.html#term-list) and [`dict`](https://docs.python.org/3/reference/expressions.html#dict):

* If the type variable is [bound](https://typing.readthedocs.io/en/latest/reference/generics.html#type-variables-with-upper-bounds)
  or [constrained](https://typing.readthedocs.io/en/latest/reference/generics.html#type-variables-with-constraints) to a specific type,
  it will be used.
* If the type variable has a default type (as specified by [PEP 696](https://peps.python.org/pep-0696/)), it will be used.
* For unbound or unconstrained type variables, Pydantic will fallback to [`Any`](https://docs.python.org/3/library/typing.html#typing.Any).

```
from typing import Generic

from typing_extensions import TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar('T')
U = TypeVar('U', bound=int)
V = TypeVar('V', default=str)

class Model(BaseModel, Generic[T, U, V]):
    t: T
    u: U
    v: V

print(Model(t='t', u=1, v='v'))
#> t='t' u=1 v='v'

try:
    Model(t='t', u='u', v=1)
except ValidationError as exc:
    print(exc)
    """
    2 validation errors for Model
    u
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='u', input_type=str]
    v
      Input should be a valid string [type=string_type, input_value=1, input_type=int]
    """
```

```
from typing import Generic, TypeVar

from pydantic import BaseModel

ItemT = TypeVar('ItemT', bound='ItemBase')

class ItemBase(BaseModel): ...

class IntItem(ItemBase):
  value: int

class ItemHolder(BaseModel, Generic[ItemT]):
  item: ItemT

loaded_data = {'item': {'value': 1}}

print(ItemHolder(**loaded_data))  # (1)
#> item=ItemBase()

print(ItemHolder[IntItem](**loaded_data))  # (2)
#> item=IntItem(value=1)
```

When the generic isn't parametrized, the input data is validated against the `ItemT` upper bound.
Given that `ItemBase` has no fields, the `item` field information is lost.

In this case, the type variable is explicitly parametrized, so the input data is validated against the `IntItem` class.

### Serialization of unparametrized type variables

The behavior of serialization differs when using type variables with [upper bounds](https://typing.readthedocs.io/en/latest/reference/generics.html#type-variables-with-upper-bounds), [constraints](https://typing.readthedocs.io/en/latest/reference/generics.html#type-variables-with-constraints), or a default value:

If a Pydantic model is used in a type variable upper bound and the type variable is never parametrized, then Pydantic will use the upper bound for validation but treat the value as [`Any`](https://docs.python.org/3/library/typing.html#typing.Any) in terms of serialization:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

class ErrorDetails(BaseModel):
    foo: str

ErrorDataT = TypeVar('ErrorDataT', bound=ErrorDetails)

class Error(BaseModel, Generic[ErrorDataT]):
    message: str
    details: ErrorDataT

class MyErrorDetails(ErrorDetails):
    bar: str

# serialized as Any
error = Error(
    message='We just had an error',
    details=MyErrorDetails(foo='var', bar='var2'),
)
assert error.model_dump() == {
    'message': 'We just had an error',
    'details': {
        'foo': 'var',
        'bar': 'var2',
    },
}

# serialized using the concrete parametrization
# note that `'bar': 'var2'` is missing
error = Error[ErrorDetails](
    message='We just had an error',
    details=ErrorDetails(foo='var'),
)
assert error.model_dump() == {
    'message': 'We just had an error',
    'details': {
        'foo': 'var',
    },
}
```

Here’s another example of the above behavior, enumerating all permutations regarding bound specification and generic type parametrization:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

TBound = TypeVar('TBound', bound=BaseModel)
TNoBound = TypeVar('TNoBound')

class IntValue(BaseModel):
    value: int

class ItemBound(BaseModel, Generic[TBound]):
    item: TBound

class ItemNoBound(BaseModel, Generic[TNoBound]):
    item: TNoBound

item_bound_inferred = ItemBound(item=IntValue(value=3))
item_bound_explicit = ItemBound[IntValue](item=IntValue(value=3))
item_no_bound_inferred = ItemNoBound(item=IntValue(value=3))
item_no_bound_explicit = ItemNoBound[IntValue](item=IntValue(value=3))

# calling `print(x.model_dump())` on any of the above instances results in the following:
#> {'item': {'value': 3}}
```

However, if [constraints](https://typing.readthedocs.io/en/latest/reference/generics.html#type-variables-with-constraints)
or a default value (as per [PEP 696](https://peps.python.org/pep-0696/)) is being used, then the default type or constraints
will be used for both validation and serialization if the type variable is not parametrized. You can override this behavior
using [`SerializeAsAny`](/docs/validation/latest/concepts/serialization#serializeasany-annotation):

```
from typing import Generic

from typing_extensions import TypeVar

from pydantic import BaseModel, SerializeAsAny

class ErrorDetails(BaseModel):
    foo: str

ErrorDataT = TypeVar('ErrorDataT', default=ErrorDetails)

class Error(BaseModel, Generic[ErrorDataT]):
    message: str
    details: ErrorDataT

class MyErrorDetails(ErrorDetails):
    bar: str

# serialized using the default's serializer
error = Error(
    message='We just had an error',
    details=MyErrorDetails(foo='var', bar='var2'),
)
assert error.model_dump() == {
    'message': 'We just had an error',
    'details': {
        'foo': 'var',
    },
}
# If `ErrorDataT` was using an upper bound, `bar` would be present in `details`.

class SerializeAsAnyError(BaseModel, Generic[ErrorDataT]):
    message: str
    details: SerializeAsAny[ErrorDataT]

# serialized as Any
error = SerializeAsAnyError(
    message='We just had an error',
    details=MyErrorDetails(foo='var', bar='baz'),
)
assert error.model_dump() == {
    'message': 'We just had an error',
    'details': {
        'foo': 'var',
        'bar': 'baz',
    },
}
```

## Dynamic model creation

API Documentation

[`pydantic.main.create_model`](/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model)

There are some occasions where it is desirable to create a model using runtime information to specify the fields.
Pydantic provides the [`create_model()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model) function to allow models to be created dynamically:

```
from pydantic import BaseModel, create_model

DynamicFoobarModel = create_model('DynamicFoobarModel', foo=str, bar=(int, 123))

# Equivalent to:

class StaticFoobarModel(BaseModel):
    foo: str
    bar: int = 123
```

Field definitions are specified as keyword arguments, and should either be:

* A single element, representing the type annotation of the field.
* A two-tuple, the first element being the type and the second element the assigned value
  (either a default or the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function).

Here is a more advanced example:

```
from typing import Annotated

from pydantic import BaseModel, Field, PrivateAttr, create_model

DynamicModel = create_model(
    'DynamicModel',
    foo=(str, Field(alias='FOO')),
    bar=Annotated[str, Field(description='Bar field')],
    _private=(int, PrivateAttr(default=1)),
)

class StaticModel(BaseModel):
    foo: str = Field(alias='FOO')
    bar: Annotated[str, Field(description='Bar field')]
    _private: int = PrivateAttr(default=1)
```

The special keyword arguments `__config__` and `__base__` can be used to customize the new model.
This includes extending a base model with extra fields.

```
from pydantic import BaseModel, create_model

class FooModel(BaseModel):
    foo: str
    bar: int = 123

BarModel = create_model(
    'BarModel',
    apple=(str, 'russet'),
    banana=(str, 'yellow'),
    )
print(BarModel)
#> <class '__main__.BarModel'>
print(BarModel.model_fields.keys())
#> dict_keys(['foo', 'bar', 'apple', 'banana'])
```

You can also add validators by passing a dictionary to the `__validators__` argument.

```
from pydantic import ValidationError, create_model, field_validator

def alphanum(cls, v):
  assert v.isalnum(), 'must be alphanumeric'
  return v

validators = {
  'username_validator': field_validator('username')(alphanum)  # (1)
}

UserModel = create_model(
  'UserModel', username=(str, ...), )

user = UserModel(username='scolvin')
print(user)
#> username='scolvin'

try:
  UserModel(username='scolvi%n')
except ValidationError as e:
  print(e)
  """
  1 validation error for UserModel
  username
    Assertion failed, must be alphanumeric [type=assertion_error, input_value='scolvi%n', input_type=str]
  """
```

Make sure that the validators names do not clash with any of the field names as
internally, Pydantic gathers all members into a namespace and mimics the normal
creation of a class using the [`types` module utilities](https://docs.python.org/3/library/types.html#dynamic-type-creation).

See also: the [dynamic model example](/docs/validation/latest/examples/dynamic_models), providing guidelines to derive an optional model from another one.

## `RootModel` and custom root types

API Documentation

[`pydantic.root_model.RootModel`](/docs/validation/latest/api/pydantic/root_model/#pydantic.root_model.RootModel)

Pydantic models can be defined with a “custom root type” by subclassing [`pydantic.RootModel`](/docs/validation/latest/api/pydantic/root_model/#pydantic.root_model.RootModel).

The root type can be any type supported by Pydantic, and is specified by the generic parameter to `RootModel`.
The root value can be passed to the model `__init__` or [`model_validate`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate)
via the first and only argument.

Here’s an example of how this works:

```
from pydantic import RootModel

Pets = RootModel[list[str]]
PetsByName = RootModel[dict[str, str]]

print(Pets(['dog', 'cat']))
#> root=['dog', 'cat']
print(Pets(['dog', 'cat']).model_dump_json())
#> ["dog","cat"]
print(Pets.model_validate(['dog', 'cat']))
#> root=['dog', 'cat']
print(Pets.model_json_schema())
"""
{'items': {'type': 'string'}, 'title': 'RootModel[list[str]]', 'type': 'array'}
"""

print(PetsByName({'Otis': 'dog', 'Milo': 'cat'}))
#> root={'Otis': 'dog', 'Milo': 'cat'}
print(PetsByName({'Otis': 'dog', 'Milo': 'cat'}).model_dump_json())
#> {"Otis":"dog","Milo":"cat"}
print(PetsByName.model_validate({'Otis': 'dog', 'Milo': 'cat'}))
#> root={'Otis': 'dog', 'Milo': 'cat'}
```

If you want to access items in the `root` field directly or to iterate over the items, you can implement
custom `__iter__` and `__getitem__` functions, as shown in the following example.

```
from pydantic import RootModel

class Pets(RootModel):
    root: list[str]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

pets = Pets.model_validate(['dog', 'cat'])
print(pets[0])
#> dog
print([pet for pet in pets])
#> ['dog', 'cat']
```

You can also create subclasses of the parametrized root model directly:

```
from pydantic import RootModel

class Pets(RootModel[list[str]]):
    def describe(self) -> str:
        return f'Pets: {", ".join(self.root)}'

my_pets = Pets.model_validate(['dog', 'cat'])

print(my_pets.describe())
#> Pets: dog, cat
```

## Faux immutability

Models can be configured to be immutable via `model_config['frozen'] = True`. When this is set, attempting to change the
values of instance attributes will raise errors. See the [API reference](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.frozen) for more details.

```
from pydantic import BaseModel, ConfigDict, ValidationError

class FooBarModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    a: str
    b: dict

foobar = FooBarModel(a='hello', b={'apple': 'pear'})

try:
    foobar.a = 'different'
except ValidationError as e:
    print(e)
    """
    1 validation error for FooBarModel
    a
      Instance is frozen [type=frozen_instance, input_value='different', input_type=str]
    """

print(foobar.a)
#> hello
print(foobar.b)
#> {'apple': 'pear'}
foobar.b['apple'] = 'grape'
print(foobar.b)
#> {'apple': 'grape'}
```

Trying to change `a` caused an error, and `a` remains unchanged. However, the dict `b` is mutable, and the
immutability of `foobar` doesn’t stop `b` from being changed.

## Abstract base classes

Pydantic models can be used alongside Python’s
[Abstract Base Classes](https://docs.python.org/3/library/abc.html) (ABCs).

```
import abc

from pydantic import BaseModel

class FooBarModel(BaseModel, abc.ABC):
    a: str
    b: int

    @abc.abstractmethod
    def my_abstract_method(self):
        pass
```

## Field ordering

Field order affects models in the following ways:

* field order is preserved in the model [JSON Schema](/docs/validation/latest/concepts/json_schema)
* field order is preserved in [validation errors](#error-handling)
* field order is preserved when [serializing data](/docs/validation/latest/concepts/serialization#serializing-data)

```
from pydantic import BaseModel, ValidationError

class Model(BaseModel):
    a: int
    b: int = 2
    c: int = 1
    d: int = 0
    e: float

print(Model.model_fields.keys())
#> dict_keys(['a', 'b', 'c', 'd', 'e'])
m = Model(e=2, a=1)
print(m.model_dump())
#> {'a': 1, 'b': 2, 'c': 1, 'd': 0, 'e': 2.0}
try:
    Model(a='x', b='x', c='x', d='x', e='x')
except ValidationError as err:
    error_locations = [e['loc'] for e in err.errors()]

print(error_locations)
#> [('a',), ('b',), ('c',), ('d',), ('e',)]
```

## Automatically excluded attributes

### Class variables

Attributes annotated with [`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar) are properly treated by Pydantic as class variables, and will not
become fields on model instances:

```
from typing import ClassVar

from pydantic import BaseModel

class Model(BaseModel):
    x: ClassVar[int] = 1

    y: int = 2

m = Model()
print(m)
#> y=2
print(Model.x)
#> 1
```

### Private model attributes

API Documentation

[`pydantic.fields.PrivateAttr`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.PrivateAttr)

Attributes whose name has a leading underscore are not treated as fields by Pydantic, and are not included in the
model schema. Instead, these are converted into a “private attribute” which is not validated or even set during
calls to `__init__`, `model_validate`, etc.

Here is an example of usage:

```
from datetime import datetime
from random import randint
from typing import Any

from pydantic import BaseModel, PrivateAttr

class TimeAwareModel(BaseModel):
    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)
    _secret_value: str

    def model_post_init(self, context: Any) -> None:
        # this could also be done with `default_factory`:
        self._secret_value = randint(1, 5)

m = TimeAwareModel()
print(m._processed_at)
#> 2032-01-02 03:04:05.000006
print(m._secret_value)
#> 3
```

Private attribute names must start with underscore to prevent conflicts with model fields. However, dunder names
(such as `__attr__`) are not supported, and will be completely ignored from the model definition.

## Model signature

All Pydantic models will have their signature generated based on their fields:

```
import inspect

from pydantic import BaseModel, Field

class FooModel(BaseModel):
    id: int
    name: str = None
    description: str = 'Foo'
    apple: int = Field(alias='pear')

print(inspect.signature(FooModel))
#> (*, id: int, name: str = None, description: str = 'Foo', pear: int) -> None
```

An accurate signature is useful for introspection purposes and libraries like `FastAPI` or `hypothesis`.

The generated signature will also respect custom `__init__` functions:

```
import inspect

from pydantic import BaseModel

class MyModel(BaseModel):
    id: int
    info: str = 'Foo'

    def __init__(self, id: int = 1, *, bar: str, **data) -> None:
        """My custom init!"""
        super().__init__(id=id, bar=bar, **data)

print(inspect.signature(MyModel))
#> (id: int = 1, *, bar: str, info: str = 'Foo') -> None
```

To be included in the signature, a field’s alias or name must be a valid Python identifier.
Pydantic will prioritize a field’s alias over its name when generating the signature, but may use the field name if the
alias is not a valid Python identifier.

If a field’s alias and name are *both* not valid identifiers (which may be possible through exotic use of `create_model`),
a `**data` argument will be added. In addition, the `**data` argument will always be present in the signature if
`model_config['extra'] == 'allow'`.

## Structural pattern matching

Pydantic supports structural pattern matching for models, as introduced by [PEP 636](https://peps.python.org/pep-0636/) in Python 3.10.

```
from pydantic import BaseModel

class Pet(BaseModel):
    name: str
    species: str

a = Pet(name='Bones', species='dog')

match a:
    # match `species` to 'dog', declare and initialize `dog_name`
    case Pet(species='dog', name=dog_name):
        print(f'{dog_name} is a dog')
#> Bones is a dog
    # default case
    case _:
        print('No dog matched')
```

## Attribute copies

In many cases, arguments passed to the constructor will be copied in order to perform validation and, where necessary,
coercion.

In this example, note that the ID of the list changes after the class is constructed because it has been
copied during validation:

```
from pydantic import BaseModel

class C1:
    arr = []

    def __init__(self, in_arr):
        self.arr = in_arr

class C2(BaseModel):
    arr: list[int]

arr_orig = [1, 9, 10, 3]

c1 = C1(arr_orig)
c2 = C2(arr=arr_orig)
print(f'{id(c1.arr) == id(c2.arr)=}')
#> id(c1.arr) == id(c2.arr)=False
```

Was this page helpful?

---

## 2. Fields

API Documentation

[`pydantic.fields.Field`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field)

In this section, we will go through the available mechanisms to customize Pydantic model fields:
[default values](#default-values), [JSON Schema metadata](#customizing-json-schema),
[constraints](#field-constraints), etc.

To do so, the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function is used a lot, and behaves the same way as
the standard library [`field()`](https://docs.python.org/3/library/dataclasses.html#dataclasses.field) function for dataclasses – by assigning to the
annotated attribute:

```
from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(frozen=True)
```

## The annotated pattern

To apply constraints or attach [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) functions to a model field, Pydantic
also supports the [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) typing construct to attach metadata to an annotation:

```
from typing import Annotated

from pydantic import BaseModel, Field, WithJsonSchema

class Model(BaseModel):
    name: Annotated[str, Field(strict=True), WithJsonSchema({'extra': 'data'})]
```

As far as static type checkers are concerned, `name` is still typed as `str`, but Pydantic leverages
the available metadata to add validation logic, type constraints, etc.

Using this pattern has some advantages:

* Using the `f: <type> = Field(...)` form can be confusing and might trick users into thinking `f`
  has a default value, while in reality it is still required.
* You can provide an arbitrary amount of metadata elements for a field. As shown in the example above,
  the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function only supports a limited set of constraints/metadata,
  and you may have to use different Pydantic utilities such as [`WithJsonSchema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.WithJsonSchema)
  in some cases.
* Types can be made reusable (see the documentation on [custom types](/docs/validation/latest/concepts/types#using-the-annotated-pattern)
  using this pattern).

However, note that certain arguments to the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function (namely, `default`,
`default_factory`, and `alias`) are taken into account by static type checkers to synthesize a correct
`__init__()` method. The annotated pattern is *not* understood by them, so you should use the normal
assignment form instead.

```
class Model(BaseModel):
  field_bad: Annotated[int, Field(deprecated=True)] | None = None  # (1)
  field_ok: Annotated[int | None, Field(deprecated=True)] = None  # (2)
```

The [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function is applied to `int` type, hence the
`deprecated` flag won't have any effect. While this may be confusing given that the name of
the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function would imply it should apply to the field,
the API was designed when this function was the only way to provide metadata. You can
alternatively make use of the [`annotated_types`](https://github.com/annotated-types/annotated-types)
library which is now supported by Pydantic.

The [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function is applied to the "top-level" union type,
hence the `deprecated` flag will be applied to the field.

## Inspecting model fields

The fields of a model can be inspected using the [`model_fields`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_fields) class attribute
(or the `__pydantic_fields__` attribute for [Pydantic dataclasses](/docs/validation/latest/concepts/dataclasses)). It is a mapping of field names
to their definition (represented as [`FieldInfo`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo) instances).

```
from typing import Annotated

from pydantic import BaseModel, Field, WithJsonSchema

class Model(BaseModel):
    a: Annotated[
        int, Field(gt=1), WithJsonSchema({'extra': 'data'}), Field(alias='b')
    ] = 1

field_info = Model.model_fields['a']
print(field_info.annotation)
#> <class 'int'>
print(field_info.alias)
#> b
print(field_info.metadata)
#> [Gt(gt=1), WithJsonSchema(json_schema={'extra': 'data'}, mode=None)]
```

## Default values

Default values for fields can be provided using the normal assignment syntax or by providing a value
to the `default` argument:

```
from pydantic import BaseModel, Field

class User(BaseModel):
    # Both fields aren't required:
    name: str = 'John Doe'
    age: int = Field(default=20)
```

You can also pass a callable to the `default_factory` argument that will be called to generate a default value:

```
from uuid import uuid4

from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
```

The default factory can also take a single required argument, in which case the already validated data will be passed as a dictionary.

```
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr
    username: str = Field(default_factory=lambda data: data['email'])

user = User(email='[email protected]')
print(user.username)
#> [email protected]
```

The `data` argument will *only* contain the already validated data, based on the [order of model fields](/docs/validation/latest/concepts/models#field-ordering)
(the above example would fail if `username` were to be defined before `email`).

## Validate default values

By default, Pydantic will *not* validate default values. The `validate_default` field parameter
(or the [`validate_default`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_default) configuration value) can be used
to enable this behavior:

```
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    age: int = Field(default='twelve', validate_default=True)

try:
    user = User()
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    age
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='twelve', input_type=str]
    """
```

### Mutable default values

A common source of bugs in Python is to use a mutable object as a default value for a function or method argument,
as the same instance ends up being reused in each call.

The [`dataclasses`](https://docs.python.org/3/library/dataclasses.html#module-dataclasses) module actually raises an error in this case, indicating that you should use
a [default factory](https://docs.python.org/3/library/dataclasses.html#default-factory-functions) instead.

While the same thing can be done in Pydantic, it is not required. In the event that the default value is not hashable,
Pydantic will create a deep copy of the default value when creating each instance of the model:

```
from pydantic import BaseModel

class Model(BaseModel):
    item_counts: list[dict[str, int]] = [{}]

m1 = Model()
m1.item_counts[0]['a'] = 1
print(m1.item_counts)
#> [{'a': 1}]

m2 = Model()
print(m2.item_counts)
#> [{}]
```

## Field aliases

For validation and serialization, you can define an alias for a field.

There are three ways to define an alias:

* `Field(alias='foo')`
* `Field(validation_alias='foo')`
* `Field(serialization_alias='foo')`

The `alias` parameter is used for both validation *and* serialization. If you want to use
*different* aliases for validation and serialization respectively, you can use the `validation_alias`
and `serialization_alias` parameters, which will apply only in their respective use cases.

Here is an example of using the `alias` parameter:

```
from pydantic import BaseModel, Field

class User(BaseModel):
  name: str = Field(alias='username')

user = User(username='johndoe')  # (1)
print(user)
#> name='johndoe'
print(user.model_dump(by_alias=True))  # (2)
#> {'username': 'johndoe'}
```

The alias `'username'` is used for instance creation and validation.

We are using [`model_dump()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump) to convert the model into a serializable format.

Note that the `by_alias` keyword argument defaults to `False`, and must be specified explicitly to dump
models using the field (serialization) aliases.

You can also use [`ConfigDict.serialize_by_alias`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.serialize_by_alias) to
configure this behavior at the model level.

When `by_alias=True`, the alias `'username'` used during serialization.

If you want to use an alias *only* for validation, you can use the `validation_alias` parameter:

```
from pydantic import BaseModel, Field

class User(BaseModel):
  name: str = Field(validation_alias='username')

user = User(username='johndoe')  # (1)
print(user)
#> name='johndoe'
print(user.model_dump(by_alias=True))  # (2)
#> {'name': 'johndoe'}
```

The validation alias `'username'` is used during validation.

The field name `'name'` is used during serialization.

If you only want to define an alias for *serialization*, you can use the `serialization_alias` parameter:

```
from pydantic import BaseModel, Field

class User(BaseModel):
  name: str = Field(serialization_alias='username')

user = User(name='johndoe')  # (1)
print(user)
#> name='johndoe'
print(user.model_dump(by_alias=True))  # (2)
#> {'username': 'johndoe'}
```

The field name `'name'` is used for validation.

The serialization alias `'username'` is used for serialization.

Static type checking/IDE support

If you provide a value for the `alias` field parameter, static type checkers will use this alias instead
of the actual field name to synthesize the `__init__` method:

```
from pydantic import BaseModel, Field

class User(BaseModel):
  name: str = Field(alias='username')

user = User(username='johndoe')  # (1)
```

Accepted by type checkers.

This means that when using the [`validate_by_name`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_by_name) model setting (which allows both the field name and alias to be used during model validation), type checkers will error when the actual field name is used:

```
from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
  model_config = ConfigDict(validate_by_name=True)

  name: str = Field(alias='username')

user = User(name='johndoe')  # (1)
```

*Not* accepted by type checkers.

If you still want type checkers to use the field name and not the alias, the [annotated pattern](#the-annotated-pattern)
can be used (which is only understood by Pydantic):

```
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
  model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

  name: Annotated[str, Field(alias='username')]

user = User(name='johndoe')  # (1)
user = User(username='johndoe')  # (2)
```

Accepted by type checkers.

*Not* accepted by type checkers.

### Validation Alias

Even though Pydantic treats `alias` and `validation_alias` the same when creating model instances, type checkers
only understand the `alias` field parameter. As a workaround, you can instead specify both an `alias` and
`serialization_alias` (identical to the field name), as the `serialization_alias` will override the `alias` during
serialization:

```
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    my_field: int = Field(validation_alias='myValidationAlias')
```

with:

```
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    my_field: int = Field(
        alias='myValidationAlias',
        serialization_alias='my_field',
    )

m = MyModel(myValidationAlias=1)
print(m.model_dump(by_alias=True))
#> {'my_field': 1}
```

## Field constraints

The [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function can also be used to add constraints to specific types:

```
from decimal import Decimal

from pydantic import BaseModel, Field

class Model(BaseModel):
    positive: int = Field(gt=0)
    short_str: str = Field(max_length=3)
    precise_decimal: Decimal = Field(max_digits=5, decimal_places=2)
```

The available constraints for each type (and the way they affect the JSON Schema) are described
in the [standard library types](/docs/validation/latest/api/pydantic/standard_library_types) documentation.

## Strict fields

The `strict` parameter of the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function specifies whether the field should be validated in
[strict mode](/docs/validation/latest/concepts/strict_mode).

```
from pydantic import BaseModel, Field

class User(BaseModel):
  name: str = Field(strict=True)
  age: int = Field(strict=False)  # (1)

user = User(name='John', age='42')  # (2)
print(user)
#> name='John' age=42
```

This is the default value.

The `age` field is validated in lax mode. Therefore, it can be assigned a string.

The [standard library types](/docs/validation/latest/api/pydantic/standard_library_types) documentation describes the strict behavior for each type.

## Dataclass fields

Some parameters of the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field) function can be used on [dataclasses](/docs/validation/latest/concepts/dataclasses):

* `init`: Whether the field should be included in the synthesized `__init__()` method of the dataclass.
* `init_var`: Whether the field should be [init-only](https://docs.python.org/3/library/dataclasses.html#dataclasses-init-only-variables) in the dataclass.
* `kw_only`: Whether the field should be a keyword-only argument in the constructor of the dataclass.

Here is an example:

```
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

@dataclass
class Foo:
  bar: str
  baz: str = Field(init_var=True)
  qux: str = Field(kw_only=True)

class Model(BaseModel):
  foo: Foo

model = Model(foo=Foo('bar', baz='baz', qux='qux'))
print(model.model_dump())  # (1)
#> {'foo': {'bar': 'bar', 'qux': 'qux'}}
```

The `baz` field is not included in the serialized output, since it is an init-only field.

## Field Representation

The parameter `repr` can be used to control whether the field should be included in the string
representation of the model.

```
from pydantic import BaseModel, Field

class User(BaseModel):
  name: str = Field(repr=True)  # (1)
  age: int = Field(repr=False)

user = User(name='John', age=42)
print(user)
#> name='John'
```

This is the default value.

## Discriminator

The parameter `discriminator` can be used to control the field that will be used to discriminate between different
models in a union. It takes either the name of a field or a `Discriminator` instance. The `Discriminator`
approach can be useful when the discriminator fields aren’t the same for all the models in the `Union`.

The following example shows how to use `discriminator` with a field name:

```
from typing import Literal, Union

from pydantic import BaseModel, Field

class Cat(BaseModel):
  pet_type: Literal['cat']
  age: int

class Dog(BaseModel):
  pet_type: Literal['dog']
  age: int

class Model(BaseModel):
  pet: Union[Cat, Dog] = Field(discriminator='pet_type')

print(Model.model_validate({'pet': {'pet_type': 'cat', 'age': 12}}))  # (1)
#> pet=Cat(pet_type='cat', age=12)
```

See more about [Validating data] in the [Models] page.

The following example shows how to use the `discriminator` keyword argument with a `Discriminator` instance:

```
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Discriminator, Field, Tag

class Cat(BaseModel):
    pet_type: Literal['cat']
    age: int

class Dog(BaseModel):
    pet_kind: Literal['dog']
    age: int

def pet_discriminator(v):
    if isinstance(v, dict):
        return v.get('pet_type', v.get('pet_kind'))
    return getattr(v, 'pet_type', getattr(v, 'pet_kind', None))

class Model(BaseModel):
    pet: Union[Annotated[Cat, Tag('cat')], Annotated[Dog, Tag('dog')]] = Field(
        discriminator=Discriminator(pet_discriminator)
    )

print(repr(Model.model_validate({'pet': {'pet_type': 'cat', 'age': 12}})))
#> Model(pet=Cat(pet_type='cat', age=12))

print(repr(Model.model_validate({'pet': {'pet_kind': 'dog', 'age': 12}})))
#> Model(pet=Dog(pet_kind='dog', age=12))
```

You can also take advantage of `Annotated` to define your discriminated unions.
See the [Discriminated Unions](/docs/validation/latest/concepts/unions#discriminated-unions) docs for more details.

## Immutability

The parameter `frozen` is used to emulate the frozen dataclass behaviour. It is used to prevent the field from being
assigned a new value after the model is created (immutability).

See the [frozen dataclass documentation](https://docs.python.org/3/library/dataclasses.html#frozen-instances) for more details.

```
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
  name: str = Field(frozen=True)
  age: int

user = User(name='John', age=42)

try:
  user.name = 'Jane'  # (1)
except ValidationError as e:
  print(e)
  """
  1 validation error for User
  name
    Field is frozen [type=frozen_field, input_value='Jane', input_type=str]
  """
```

Since `name` field is frozen, the assignment is not allowed.

## Excluding fields

The `exclude` and `exclude_if` parameters can be used to control which fields should be excluded from the
model when exporting the model.

See the following example:

```
from pydantic import BaseModel, Field

class User(BaseModel):
  name: str
  age: int = Field(exclude=True)

user = User(name='John', age=42)
print(user.model_dump())  # (1)
#> {'name': 'John'}
```

The `age` field is not included in the [`model_dump()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump) output, since it is excluded.

See the dedicated [serialization section](/docs/validation/latest/concepts/serialization#field-inclusion-and-exclusion) for more details.

## Deprecated fields

The `deprecated` parameter can be used to mark a field as being deprecated. Doing so will result in:

* a runtime deprecation warning emitted when accessing the field.
* The [deprecated](https://json-schema.org/draft/2020-12/json-schema-validation#section-9.3) keyword
  being set in the generated JSON schema.

This parameter accepts different types, described below.

### `deprecated` as a string

The value will be used as the deprecation message.

```
from typing import Annotated

from pydantic import BaseModel, Field

class Model(BaseModel):
    deprecated_field: Annotated[int, Field(deprecated='This is deprecated')]

print(Model.model_json_schema()['properties']['deprecated_field'])
#> {'deprecated': True, 'title': 'Deprecated Field', 'type': 'integer'}
```

### `deprecated` via the `@warnings.deprecated` decorator

The [`@warnings.deprecated`](https://docs.python.org/3/library/warnings.html#warnings.deprecated) decorator (or the
[`typing_extensions` backport](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.deprecated) on Python
3.12 and lower) can be used as an instance.

```
from typing import Annotated

from typing_extensions import deprecated

from pydantic import BaseModel, Field

class Model(BaseModel):
    deprecated_field: Annotated[int, deprecated('This is deprecated')]

    # Or explicitly using `Field`:
    alt_form: Annotated[int, Field(deprecated=deprecated('This is deprecated'))]
```

### `deprecated` as a boolean

```
from typing import Annotated

from pydantic import BaseModel, Field

class Model(BaseModel):
    deprecated_field: Annotated[int, Field(deprecated=True)]

print(Model.model_json_schema()['properties']['deprecated_field'])
#> {'deprecated': True, 'title': 'Deprecated Field', 'type': 'integer'}
```

## Customizing JSON Schema

Some field parameters are used exclusively to customize the generated JSON schema. The parameters in question are:

* `title`
* `description`
* `examples`
* `json_schema_extra`

Read more about JSON schema customization / modification with fields in the [Customizing JSON Schema](/docs/validation/latest/concepts/json_schema#field-level-customization) section of the JSON schema docs.

## The `computed_field` decorator

API Documentation

[`computed_field`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field)

The [`computed_field`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field) decorator can be used to include [`property`](https://docs.python.org/3/library/functions.html#property) or
[`cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property) attributes when serializing a model or dataclass.
The property will also be taken into account in the JSON Schema (in serialization mode).

Here’s an example of the JSON schema (in serialization mode) generated for a model with a computed field:

```
from pydantic import BaseModel, computed_field

class Box(BaseModel):
  width: float
  height: float
  depth: float

  @computed_field
  @property  # (1)
  def volume(self) -> float:
      return self.width * self.height * self.depth

print(Box.model_json_schema(mode='serialization'))
"""
{
  'properties': {
      'width': {'title': 'Width', 'type': 'number'},
      'height': {'title': 'Height', 'type': 'number'},
      'depth': {'title': 'Depth', 'type': 'number'},
      'volume': {'readOnly': True, 'title': 'Volume', 'type': 'number'},
  },
  'required': ['width', 'height', 'depth', 'volume'],
  'title': 'Box',
  'type': 'object',
}
"""
```

If not specified, [`computed_field`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field) will implicitly convert the method
to a [`property`](https://docs.python.org/3/library/functions.html#property). However, it is preferable to explicitly use the [`@property`](https://docs.python.org/3/library/functions.html#property) decorator
for type checking purposes.

Here’s an example using the `model_dump` method with a computed field:

```
from pydantic import BaseModel, computed_field

class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    @property
    def volume(self) -> float:
        return self.width * self.height * self.depth

b = Box(width=1, height=2, depth=3)
print(b.model_dump())
#> {'width': 1.0, 'height': 2.0, 'depth': 3.0, 'volume': 6.0}
```

As with regular fields, computed fields can be marked as being deprecated:

```
from typing_extensions import deprecated

from pydantic import BaseModel, computed_field

class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    @property
    @deprecated("'volume' is deprecated")
    def volume(self) -> float:
        return self.width * self.height * self.depth
```

Was this page helpful?

---

## 3. Validators

In addition to Pydantic’s [built-in validation capabilities](/docs/validation/latest/concepts/fields#field-constraints),
you can leverage custom validators at the field and model levels to enforce more complex constraints
and ensure the integrity of your data.

## Field validators

API Documentation

[`pydantic.functional_validators.WrapValidator`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.WrapValidator)  
[`pydantic.functional_validators.PlainValidator`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.PlainValidator)  
[`pydantic.functional_validators.BeforeValidator`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.BeforeValidator)  
[`pydantic.functional_validators.AfterValidator`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.AfterValidator)  
[`pydantic.functional_validators.field_validator`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator)

In its simplest form, a field validator is a callable taking the value to be validated as an argument and
**returning the validated value**. The callable can perform checks for specific conditions (see
[raising validation errors](#raising-validation-errors)) and make changes to the validated value (coercion or mutation).

**Four** different types of validators can be used. They can all be defined using the
[annotated pattern](/docs/validation/latest/concepts/fields#the-annotated-pattern) or using the
[`field_validator()`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator) decorator, applied on a [class method](https://docs.python.org/3/library/functions.html#classmethod):

* ***After* validators**: run after Pydantic’s internal validation. They are generally more type safe and thus easier to implement.

Here is an example of a validator performing a validation check, and returning the value unchanged.

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ValidationError

def is_even(value: int) -> int:
  if value % 2 == 1:
      raise ValueError(f'{value} is not an even number')
  return value  # (1)

class Model(BaseModel):
  number: Annotated[int, AfterValidator(is_even)]

try:
  Model(number=1)
except ValidationError as err:
  print(err)
  """
  1 validation error for Model
  number
    Value error, 1 is not an even number [type=value_error, input_value=1, input_type=int]
  """
```

Note that it is important to return the validated value.

Example mutating the value

Here is an example of a validator making changes to the validated value (no exception is raised).

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel

def double_number(value: int) -> int:
    return value * 2

class Model(BaseModel):
    number: Annotated[int, AfterValidator(double_number)]

print(Model(number=2))
#> number=4
```

* ***Before* validators**: run before Pydantic’s internal parsing and validation (e.g. coercion of a `str` to an `int`).
  These are more flexible than [*after* validators](#field-after-validator), but they also have to deal with the raw input, which
  in theory could be any arbitrary object. You should also avoid mutating the value directly if you are raising a
  [validation error](#raising-validation-errors) later in your validator function, as the mutated value may be passed to other
  validators if using [unions](/docs/validation/latest/concepts/unions).

  The value returned from this callable is then validated against the provided type annotation by Pydantic.

```
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ValidationError

def ensure_list(value: Any) -> Any:  # (1)
  if not isinstance(value, list):  # (2)
      return [value]
  else:
      return value

class Model(BaseModel):
  numbers: Annotated[list[int], BeforeValidator(ensure_list)]

print(Model(numbers=2))
#> numbers=[2]
try:
  Model(numbers='str')
except ValidationError as err:
  print(err)  # (3)
  """
  1 validation error for Model
  numbers.0
    Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='str', input_type=str]
  """
```

Notice the use of [`Any`](https://docs.python.org/3/library/typing.html#typing.Any) as a type hint for `value`. *Before* validators take the raw input, which
can be anything.

Note that you might want to check for other sequence types (such as tuples) that would normally successfully
validate against the `list` type. *Before* validators give you more flexibility, but you have to account for
every possible case.

Pydantic still performs validation against the `int` type, no matter if our `ensure_list` validator
did operations on the original input type.

* ***Plain* validators**: act similarly to *before* validators but they **terminate validation immediately** after returning,
  so no further validators are called and Pydantic does not do any of its internal validation against the field type.

```
from typing import Annotated, Any

from pydantic import BaseModel, PlainValidator

def val_number(value: Any) -> Any:
  if isinstance(value, int):
      return value * 2
  else:
      return value

class Model(BaseModel):
  number: Annotated[int, PlainValidator(val_number)]

print(Model(number=4))
#> number=8
print(Model(number='invalid'))  # (1)
#> number='invalid'
```

Although `'invalid'` shouldn't validate against the `int` type, Pydantic accepts the input.

* ***Wrap* validators**: are the most flexible of all. You can run code before or after Pydantic and other validators
  process the input, or you can terminate validation immediately, either by returning the value early or by raising an
  error.

  Such validators must be defined with a **mandatory** extra *handler* parameter: a callable taking the value to be validated
  as an argument. Internally, this handler will delegate validation of the value to Pydantic. You are free to wrap the call
  to the handler in a `try..except` block, or not call it at all.

```
from typing import Any

from typing import Annotated

from pydantic import BaseModel, Field, ValidationError, ValidatorFunctionWrapHandler, WrapValidator

def truncate(value: Any, handler: ValidatorFunctionWrapHandler) -> str:
    try:
        return handler(value)
    except ValidationError as err:
        if err.errors()[0]['type'] == 'string_too_long':
            return handler(value[:5])
        else:
            raise

class Model(BaseModel):
    my_string: Annotated[str, Field(max_length=5), WrapValidator(truncate)]

print(Model(my_string='abcde'))
#> my_string='abcde'
print(Model(my_string='abcdef'))
#> my_string='abcde'
```

### Which validator pattern to use

While both approaches can achieve the same thing, each pattern provides different benefits.

#### Using the annotated pattern

One of the key benefits of using the [annotated pattern](/docs/validation/latest/concepts/fields#the-annotated-pattern) is to make
validators reusable:

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel

def is_even(value: int) -> int:
  if value % 2 == 1:
      raise ValueError(f'{value} is not an even number')
  return value

EvenNumber = Annotated[int, AfterValidator(is_even)]

class Model1(BaseModel):
  my_number: EvenNumber

class Model2(BaseModel):
  other_number: Annotated[EvenNumber, AfterValidator(lambda v: v + 2)]

class Model3(BaseModel):
  list_of_even_numbers: list[EvenNumber]  # (1)
```

As mentioned in the [annotated pattern](/docs/validation/latest/concepts/fields#the-annotated-pattern) documentation,
we can also make use of validators for specific parts of the annotation (in this case,
validation is applied for list items, but not the whole list).

It is also easier to understand which validators are applied to a type, by just looking at the field annotation.

#### Using the decorator pattern

One of the key benefits of using the [`field_validator()`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator) decorator is to apply
the function to multiple fields:

```
from pydantic import BaseModel, field_validator

class Model(BaseModel):
    f1: str
    f2: str

    @field_validator('f1', 'f2', mode='before')
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()
```

Here are a couple additional notes about the decorator usage:

* If you want the validator to apply to all fields (including the ones defined in subclasses), you can pass
  `'*'` as the field name argument.
* By default, the decorator will ensure the provided field name(s) are defined on the model. If you want to
  disable this check during class creation, you can do so by passing `False` to the `check_fields` argument.
  This is useful when the field validator is defined on a base class, and the field is expected to exist on
  subclasses.

## Model validators

API Documentation

[`pydantic.functional_validators.model_validator`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.model_validator)

Validation can also be performed on the entire model’s data using the [`model_validator()`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.model_validator)
decorator.

**Three** different types of model validators can be used:

* ***After* validators**: run after the whole model has been validated. As such, they are defined as
  *instance* methods and can be seen as post-initialization hooks. Important note: the validated instance
  should be returned.

  ```
  from typing_extensions import Self

  from pydantic import BaseModel, model_validator

  class UserModel(BaseModel):
      username: str
      password: str
      password_repeat: str

      @model_validator(mode='after')
      def check_passwords_match(self) -> Self:
          if self.password != self.password_repeat:
              raise ValueError('Passwords do not match')
          return self
  ```
* ***Before* validators**: are run before the model is instantiated. These are more flexible than *after* validators,
  but they also have to deal with the raw input, which in theory could be any arbitrary object. You should also avoid
  mutating the value directly if you are raising a [validation error](#raising-validation-errors) later in your validator
  function, as the mutated value may be passed to other validators if using [unions](/docs/validation/latest/concepts/unions).

```
from typing import Any

from pydantic import BaseModel, model_validator

class UserModel(BaseModel):
  username: str

  @model_validator(mode='before')
  @classmethod
  def check_card_number_not_present(cls, data: Any) -> Any:  # (1)
      if isinstance(data, dict):  # (2)
          if 'card_number' in data:
              raise ValueError("'card_number' should not be included")
      return data
```

Notice the use of [`Any`](https://docs.python.org/3/library/typing.html#typing.Any) as a type hint for `data`. *Before* validators take the raw input, which
can be anything.

Most of the time, the input data will be a dictionary (e.g. when calling `UserModel(username='...')`). However,
this is not always the case. For instance, if the [`from_attributes`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.from_attributes)
configuration value is set, you might receive an arbitrary class instance for the `data` argument.

* ***Wrap* validators**: are the most flexible of all. You can run code before or after Pydantic and
  other validators process the input data, or you can terminate validation immediately, either by returning
  the data early or by raising an error.

  ```
  import logging
  from typing import Any

  from typing_extensions import Self

  from pydantic import BaseModel, ModelWrapValidatorHandler, ValidationError, model_validator

  class UserModel(BaseModel):
      username: str

      @model_validator(mode='wrap')
      @classmethod
      def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
          try:
              return handler(data)
          except ValidationError:
              logging.error('Model %s failed to validate with data %s', cls, data)
              raise
  ```

## Raising validation errors

To raise a validation error, three types of exceptions can be used:

* [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError): this is the most common exception raised inside validators.
* [`AssertionError`](https://docs.python.org/3/library/exceptions.html#AssertionError): using the [assert](https://docs.python.org/3/reference/simple_stmts.html#assert) statement also works, but be aware that these statements
  are skipped when Python is run with the [-O](https://docs.python.org/3/using/cmdline.html#cmdoption-O) optimization flag.
* [`PydanticCustomError`](/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError): a bit more verbose, but provides extra flexibility:

  ```
  from pydantic_core import PydanticCustomError

  from pydantic import BaseModel, ValidationError, field_validator

  class Model(BaseModel):
      x: int

      @field_validator('x', mode='after')
      @classmethod
      def validate_x(cls, v: int) -> int:
          if v % 42 == 0:
              raise PydanticCustomError(
                  'the_answer_error',
                  '{number} is the answer!',
                  {'number': v},
              )
          return v

  try:
      Model(x=42 * 2)
  except ValidationError as e:
      print(e)
      """
      1 validation error for Model
      x
        84 is the answer! [type=the_answer_error, input_value=84, input_type=int]
      """
  ```

## Validation info

Both the field and model validators callables (in all modes) can optionally take an extra
[`ValidationInfo`](/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo) argument, providing useful extra information, such as:

* [already validated data](#validation-data)
* [user defined context](#validation-context)
* the current [validation mode](/docs/validation/latest/concepts/models#validating-data): either `'python'`, `'json'` or `'strings'` (see the [`mode`](/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.mode) property)
* the current field name, if using a [field validator](#field-validators) (see the [`field_name`](/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.field_name) property).

### Validation data

For field validators, the already validated data can be accessed using the [`data`](/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.data)
property. Here is an example than can be used as an alternative to the [*after* model validator](#model-after-validator)
example:

```
from pydantic import BaseModel, ValidationInfo, field_validator

class UserModel(BaseModel):
    password: str
    password_repeat: str
    username: str

    @field_validator('password_repeat', mode='after')
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data['password']:
            raise ValueError('Passwords do not match')
        return value
```

The [`data`](/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.data) property is `None` for [model validators](#model-validators).

### Validation context

You can pass a context object to the [validation methods](/docs/validation/latest/concepts/models#validating-data), which can be accessed
inside the validator functions using the [`context`](/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.context) property:

```
from pydantic import BaseModel, ValidationInfo, field_validator

class Model(BaseModel):
    text: str

    @field_validator('text', mode='after')
    @classmethod
    def remove_stopwords(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(info.context, dict):
            stopwords = info.context.get('stopwords', set())
            v = ' '.join(w for w in v.split() if w.lower() not in stopwords)
        return v

data = {'text': 'This is an example document'}
print(Model.model_validate(data))  # no context
#> text='This is an example document'
print(Model.model_validate(data, context={'stopwords': ['this', 'is', 'an']}))
#> text='example document'
```

Similarly, you can [use a context for serialization](/docs/validation/latest/concepts/serialization#serialization-context).

Providing context when directly instantiating a model

It is currently not possible to provide a context when directly instantiating a model
(i.e. when calling `Model(...)`). You can work around this through the use of a
[`ContextVar`](https://docs.python.org/3/library/contextvars.html#contextvars.ContextVar) and a custom `__init__` method:

```
from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from pydantic import BaseModel, ValidationInfo, field_validator

_init_context_var = ContextVar('_init_context_var', default=None)

@contextmanager
def init_context(value: dict[str, Any]) -> Generator[None]:
    token = _init_context_var.set(value)
    try:
        yield
    finally:
        _init_context_var.reset(token)

class Model(BaseModel):
    my_number: int

    def __init__(self, /, **data: Any) -> None:
        self.__pydantic_validator__.validate_python(
            data,
            self_instance=self,
            context=_init_context_var.get(),
        )

    @field_validator('my_number')
    @classmethod
    def multiply_with_context(cls, value: int, info: ValidationInfo) -> int:
        if isinstance(info.context, dict):
            multiplier = info.context.get('multiplier', 1)
            value = value * multiplier
        return value

print(Model(my_number=2))
#> my_number=2

with init_context({'multiplier': 3}):
    print(Model(my_number=2))
    #> my_number=6

print(Model(my_number=2))
#> my_number=2
```

## Ordering of validators

When using the [annotated pattern](#using-the-annotated-pattern), the order in which validators are applied
is defined as follows: [*before*](#field-before-validator) and [*wrap*](#field-wrap-validator) validators
are run from right to left, and [*after*](#field-after-validator) validators are then run from left to right:

```
from pydantic import AfterValidator, BaseModel, BeforeValidator, WrapValidator

class Model(BaseModel):
    name: Annotated[
        str,
        AfterValidator(runs_3rd),
        AfterValidator(runs_4th),
        BeforeValidator(runs_2nd),
        WrapValidator(runs_1st),
    ]
```

Internally, validators defined using [the decorator](#using-the-decorator-pattern) are converted to their annotated
form counterpart and added last after the existing metadata for the field. This means that the same ordering
logic applies.

## Special types

Pydantic provides a few special utilities that can be used to customize validation.

* [`InstanceOf`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.InstanceOf) can be used to validate that a value is an instance of a given class.

  ```
  from pydantic import BaseModel, InstanceOf, ValidationError

  class Fruit:
      def __repr__(self):
          return self.__class__.__name__

  class Banana(Fruit): ...

  class Apple(Fruit): ...

  class Basket(BaseModel):
      fruits: list[InstanceOf[Fruit]]

  print(Basket(fruits=[Banana(), Apple()]))
  #> fruits=[Banana, Apple]
  try:
      Basket(fruits=[Banana(), 'Apple'])
  except ValidationError as e:
      print(e)
      """
      1 validation error for Basket
      fruits.1
        Input should be an instance of Fruit [type=is_instance_of, input_value='Apple', input_type=str]
      """
  ```
* [`SkipValidation`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.SkipValidation) can be used to skip validation on a field.

```
from pydantic import BaseModel, SkipValidation

class Model(BaseModel):
  names: list[SkipValidation[str]]

m = Model(names=['foo', 'bar'])
print(m)
#> names=['foo', 'bar']

m = Model(names=['foo', 123])  # (1)
print(m)
#> names=['foo', 123]
```

Note that the validation of the second item is skipped. If it has the wrong type it will emit a
warning during serialization.

* [`ValidateAs`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ValidateAs) can be used to validate an custom type from a
  type natively supported by Pydantic. This is particularly useful when using custom types with multiple fields.

  ```
  from typing import Annotated

  from pydantic import BaseModel, TypeAdapter, ValidateAs

  class MyCls:
      def __init__(self, a: int) -> None:
          self.a = a

      def __repr__(self) -> str:
          return f"MyCls(a={self.a})"

  class ValModel(BaseModel):
      a: int

  ta = TypeAdapter(
      Annotated[MyCls, ValidateAs(ValModel, lambda v: MyCls(a=v.a))]
  )

  print(ta.validate_python({'a': 1}))
  #> MyCls(a=1)
  ```
* [`PydanticUseDefault`](/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticUseDefault) can be used to notify Pydantic that the default value
  should be used.

  ```
  from typing import Annotated, Any

  from pydantic_core import PydanticUseDefault

  from pydantic import BaseModel, BeforeValidator

  def default_if_none(value: Any) -> Any:
      if value is None:
          raise PydanticUseDefault()
      return value

  class Model(BaseModel):
      name: Annotated[str, BeforeValidator(default_if_none)] = 'default_name'

  print(Model(name=None))
  #> name='default_name'
  ```

## JSON Schema and field validators

When using [*before*](#field-before-validator), [*plain*](#field-plain-validator) or [*wrap*](#field-wrap-validator)
field validators, the accepted input type may be different from the field annotation.

Consider the following example:

```
from typing import Any

from pydantic import BaseModel, field_validator

class Model(BaseModel):
    value: str

    @field_validator('value', mode='before')
    @classmethod
    def cast_ints(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        else:
            return value

print(Model(value='a'))
#> value='a'
print(Model(value=1))
#> value='1'
```

While the type hint for `value` is `str`, the `cast_ints` validator also allows integers. To specify the correct
input type, the `json_schema_input_type` argument can be provided:

```
from typing import Any, Union

from pydantic import BaseModel, field_validator

class Model(BaseModel):
    value: str

    @field_validator(
        'value', mode='before', json_schema_input_type=Union[int, str]
    )
    @classmethod
    def cast_ints(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        else:
            return value

print(Model.model_json_schema()['properties']['value'])
#> {'anyOf': [{'type': 'integer'}, {'type': 'string'}], 'title': 'Value'}
```

As a convenience, Pydantic will use the field type if the argument is not provided (unless you are using
a [*plain*](#field-plain-validator) validator, in which case `json_schema_input_type` defaults to
[`Any`](https://docs.python.org/3/library/typing.html#typing.Any) as the field type is completely discarded).

Was this page helpful?

---

## 4. Types

Pydantic uses types to define how validation and serialization should be performed.
[Built-in and standard library types](/docs/validation/latest/api/pydantic/standard_library_types) (such as [`int`](https://docs.python.org/3/library/functions.html#int),
[`str`](https://docs.python.org/3/library/stdtypes.html#str), [`date`](https://docs.python.org/3/library/datetime.html#datetime.date)) can be used as is. [Strictness](/docs/validation/latest/concepts/strict_mode)
can be controlled and constraints can be applied on them.

On top of these, Pydantic provides extra types, either [directly in the library](/docs/validation/latest/api/pydantic/types)
(e.g. [`SecretStr`](/docs/validation/latest/api/pydantic/types/#pydantic.types.SecretStr)) or in the [`pydantic-extra-types`](https://github.com/pydantic/pydantic-extra-types)
external library. These are implemented using the patterns described in the [custom types](#custom-types) section.
Strictness and constraints *can’t* be applied on them.

The [built-in and standard library types](/docs/validation/latest/api/pydantic/standard_library_types) documentation goes over
the supported types: the allowed values, the possible validation constraints, and whether [strictness](/docs/validation/latest/concepts/strict_mode)
can be configured.

See also the [conversion table](/docs/validation/latest/concepts/conversion_table) for a summary of the allowed values for each type.

This page will go over defining your own custom types.

## Custom Types

There are several ways to define your custom types.

### Using the annotated pattern

The [annotated pattern](/docs/validation/latest/concepts/fields#the-annotated-pattern) can be used to make types reusable across your code base.
For example, to create a type representing a positive integer:

```
from typing import Annotated

from pydantic import Field, TypeAdapter, ValidationError

PositiveInt = Annotated[int, Field(gt=0)]  # (1)

ta = TypeAdapter(PositiveInt)

print(ta.validate_python(1))
#> 1

try:
  ta.validate_python(-1)
except ValidationError as exc:
  print(exc)
  """
  1 validation error for constrained-int
    Input should be greater than 0 [type=greater_than, input_value=-1, input_type=int]
  """
```

Note that you can also use constraints from the [annotated-types](https://github.com/annotated-types/annotated-types)
library to make this Pydantic-agnostic:

```
from annotated_types import Gt

PositiveInt = Annotated[int, Gt(0)]
```

#### Adding validation and serialization

You can add or override validation, serialization, and JSON schemas to an arbitrary type using the markers that
Pydantic exports:

```
from typing import Annotated

from pydantic import (
    AfterValidator,
    PlainSerializer,
    TypeAdapter,
    WithJsonSchema,
)

TruncatedFloat = Annotated[
    float,
    AfterValidator(lambda x: round(x, 1)),
    PlainSerializer(lambda x: f'{x:.1e}', return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]

ta = TypeAdapter(TruncatedFloat)

input = 1.02345
assert input != 1.0

assert ta.validate_python(input) == 1.0

assert ta.dump_json(input) == b'"1.0e+00"'

assert ta.json_schema(mode='validation') == {'type': 'number'}
assert ta.json_schema(mode='serialization') == {'type': 'string'}
```

#### Generics

[Type variables](https://docs.python.org/3/library/typing.html#typing.TypeVar) can be used within the [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) type:

```
from typing import Annotated, TypeVar

from annotated_types import Gt, Len

from pydantic import TypeAdapter, ValidationError

T = TypeVar('T')

ShortList = Annotated[list[T], Len(max_length=4)]

ta = TypeAdapter(ShortList[int])

v = ta.validate_python([1, 2, 3, 4])
assert v == [1, 2, 3, 4]

try:
    ta.validate_python([1, 2, 3, 4, 5])
except ValidationError as exc:
    print(exc)
    """
    1 validation error for list[int]
      List should have at most 4 items after validation, not 5 [type=too_long, input_value=[1, 2, 3, 4, 5], input_type=list]
    """

PositiveList = list[Annotated[T, Gt(0)]]

ta = TypeAdapter(PositiveList[float])

v = ta.validate_python([1.0])
assert type(v[0]) is float

try:
    ta.validate_python([-1.0])
except ValidationError as exc:
    print(exc)
    """
    1 validation error for list[constrained-float]
    0
      Input should be greater than 0 [type=greater_than, input_value=-1.0, input_type=float]
    """
```

### Named type aliases

The above examples make use of *implicit* type aliases, assigned to a variable. At runtime, Pydantic
has no way of knowing the name of the variable it was assigned to, and this can be problematic for
two reasons:

* The [JSON Schema](/docs/validation/latest/concepts/json_schema) of the alias won’t be converted into a
  [definition](https://json-schema.org/understanding-json-schema/structuring#defs).
  This is mostly useful when you are using the alias more than once in a model definition.
* In most cases, [recursive type aliases](#named-recursive-types) won’t work.

By leveraging the new [`type` statement](https://typing.readthedocs.io/en/latest/spec/aliases.html#type-statement)
(introduced in [PEP 695](https://peps.python.org/pep-0695/)), you can define aliases as follows:

```
from typing import Annotated

from annotated_types import Gt
from typing_extensions import TypeAliasType

from pydantic import BaseModel

PositiveIntList = TypeAliasType('PositiveIntList', list[Annotated[int, Gt(0)]])

class Model(BaseModel):
  x: PositiveIntList
  y: PositiveIntList

print(Model.model_json_schema())  # (1)
"""
{
  '$defs': {
      'PositiveIntList': {
          'items': {'exclusiveMinimum': 0, 'type': 'integer'},
          'type': 'array',
      }
  },
  'properties': {
      'x': {'$ref': '#/$defs/PositiveIntList'},
      'y': {'$ref': '#/$defs/PositiveIntList'},
  },
  'required': ['x', 'y'],
  'title': 'Model',
  'type': 'object',
}
"""
```

If `PositiveIntList` were to be defined as an implicit type alias, its definition
would have been duplicated in both `'x'` and `'y'`.

```
from typing import Annotated

from typing_extensions import TypeAliasType

from pydantic import BaseModel, Field

MyAlias = TypeAliasType('MyAlias', Annotated[int, Field(default=1)])

class Model(BaseModel):
    x: MyAlias  # This is not allowed
```

Only metadata that can be applied to the annotated type itself is allowed
(e.g. [validation constraints](/docs/validation/latest/concepts/fields#field-constraints) and JSON metadata).
Trying to support field-specific metadata would require eagerly inspecting the
type alias’s [`__value__`](https://docs.python.org/3/library/typing.html#typing.TypeAliasType.__value__), and as such Pydantic
wouldn’t be able to have the alias stored as a JSON Schema definition.

```
from typing import Annotated, TypeVar

from annotated_types import Len
from typing_extensions import TypeAliasType

T = TypeVar('T')

ShortList = TypeAliasType(
    'ShortList', Annotated[list[T], Len(max_length=4)], type_params=(T,)
)
```

#### Named recursive types

Named type aliases should be used whenever you need to define recursive type aliases .

For several reasons, Pydantic isn't able to support implicit recursive aliases. For
instance, it won't be able to resolve [forward annotations](/docs/validation/latest/concepts/forward_annotations)
across modules.

For instance, here is an example definition of a JSON type:

```
from typing import Union

from typing_extensions import TypeAliasType

from pydantic import TypeAdapter

Json = TypeAliasType(
  'Json',
  'Union[dict[str, Json], list[Json], str, int, float, bool, None]',  # (1)
)

ta = TypeAdapter(Json)
print(ta.json_schema())
"""
{
  '$defs': {
      'Json': {
          'anyOf': [
              {
                  'additionalProperties': {'$ref': '#/$defs/Json'},
                  'type': 'object',
              },
              {'items': {'$ref': '#/$defs/Json'}, 'type': 'array'},
              {'type': 'string'},
              {'type': 'integer'},
              {'type': 'number'},
              {'type': 'boolean'},
              {'type': 'null'},
          ]
      }
  },
  '$ref': '#/$defs/Json',
}
"""
```

Wrapping the annotation in quotes is necessary as it is eagerly evaluated
(and `Json` has yet to be defined).

### Customizing validation with `__get_pydantic_core_schema__`

To do more extensive customization of how Pydantic handles custom classes, and in particular when you have access to the
class or can subclass it, you can implement a special `__get_pydantic_core_schema__` to tell Pydantic how to generate the
`pydantic-core` schema.

While `pydantic` uses `pydantic-core` internally to handle validation and serialization, it is a new API for Pydantic V2,
thus it is one of the areas most likely to be tweaked in the future and you should try to stick to the built-in
constructs like those provided by `annotated-types`, `pydantic.Field`, or `BeforeValidator` and so on.

You can implement `__get_pydantic_core_schema__` both on a custom type and on metadata intended to be put in `Annotated`.
In both cases the API is middleware-like and similar to that of “wrap” validators: you get a `source_type` (which isn’t
necessarily the same as the class, in particular for generics) and a `handler` that you can call with a type to either
call the next metadata in `Annotated` or call into Pydantic’s internal schema generation.

The simplest no-op implementation calls the handler with the type you are given, then returns that as the result. You can
also choose to modify the type before calling the handler, modify the core schema returned by the handler, or not call the
handler at all.

#### As a method on a custom type

The following is an example of a type that uses `__get_pydantic_core_schema__` to customize how it gets validated.
This is equivalent to implementing `__get_validators__` in Pydantic V1.

```
from typing import Any

from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler, TypeAdapter

class Username(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))

ta = TypeAdapter(Username)
res = ta.validate_python('abc')
assert isinstance(res, Username)
assert res == 'abc'
```

See [JSON Schema](/docs/validation/latest/concepts/json_schema) for more details on how to customize JSON schemas for custom types.

#### As an annotation

Often you’ll want to parametrize your custom type by more than just generic type parameters (which you can do via the type system and will be discussed later). Or you may not actually care (or want to) make an instance of your subclass; you actually want the original type, just with some extra validation done.

For example, if you were to implement `pydantic.AfterValidator` (see [Adding validation and serialization](#adding-validation-and-serialization)) yourself, you’d do something similar to the following:

```
from dataclasses import dataclass
from typing import Annotated, Any, Callable

from pydantic_core import CoreSchema, core_schema

from pydantic import BaseModel, GetCoreSchemaHandler

@dataclass(frozen=True)  # (1)
class MyAfterValidator:
  func: Callable[[Any], Any]

  def __get_pydantic_core_schema__(
      self, source_type: Any, handler: GetCoreSchemaHandler
  ) -> CoreSchema:
      return core_schema.no_info_after_validator_function(
          self.func, handler(source_type)
      )

Username = Annotated[str, MyAfterValidator(str.lower)]

class Model(BaseModel):
  name: Username

assert Model(name='ABC').name == 'abc'  # (2)
```

The `frozen=True` specification makes `MyAfterValidator` hashable. Without this, a union such as `Username | None` will raise an error.

Notice that type checkers will not complain about assigning `'ABC'` to `Username` like they did in the previous example because they do not consider `Username` to be a distinct type from `str`.

#### Handling third-party types

Another use case for the pattern in the previous section is to handle third party types.

```
from typing import Annotated, Any

from pydantic_core import core_schema

from pydantic import (
    BaseModel,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    ValidationError,
)
from pydantic.json_schema import JsonSchemaValue

class ThirdPartyType:
    """
    This is meant to represent a type from a third-party library that wasn't designed with Pydantic
    integration in mind, and so doesn't have a `pydantic_core.CoreSchema` or anything.
    """

    x: int

    def __init__(self):
        self.x = 0

class _ThirdPartyTypePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_int(value: int) -> ThirdPartyType:
            result = ThirdPartyType()
            result.x = value
            return result

        from_int_schema = core_schema.chain_schema(
            [
                core_schema.int_schema(),
                core_schema.no_info_plain_validator_function(validate_from_int),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_int_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ThirdPartyType),
                    from_int_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.x
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.int_schema())

# We now create an `Annotated` wrapper that we'll use as the annotation for fields on `BaseModel`s, etc.
PydanticThirdPartyType = Annotated[
    ThirdPartyType, _ThirdPartyTypePydanticAnnotation
]

# Create a model class that uses this annotation as a field
class Model(BaseModel):
    third_party_type: PydanticThirdPartyType

# Demonstrate that this field is handled correctly, that ints are parsed into `ThirdPartyType`, and that
# these instances are also "dumped" directly into ints as expected.
m_int = Model(third_party_type=1)
assert isinstance(m_int.third_party_type, ThirdPartyType)
assert m_int.third_party_type.x == 1
assert m_int.model_dump() == {'third_party_type': 1}

# Do the same thing where an instance of ThirdPartyType is passed in
instance = ThirdPartyType()
assert instance.x == 0
instance.x = 10

m_instance = Model(third_party_type=instance)
assert isinstance(m_instance.third_party_type, ThirdPartyType)
assert m_instance.third_party_type.x == 10
assert m_instance.model_dump() == {'third_party_type': 10}

# Demonstrate that validation errors are raised as expected for invalid inputs
try:
    Model(third_party_type='a')
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    third_party_type.is-instance[ThirdPartyType]
      Input should be an instance of ThirdPartyType [type=is_instance_of, input_value='a', input_type=str]
    third_party_type.chain[int,function-plain[validate_from_int()]]
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
    """

assert Model.model_json_schema() == {
    'properties': {
        'third_party_type': {'title': 'Third Party Type', 'type': 'integer'}
    },
    'required': ['third_party_type'],
    'title': 'Model',
    'type': 'object',
}
```

You can use this approach to e.g. define behavior for Pandas or Numpy types.

#### Using `GetPydanticSchema` to reduce boilerplate

API Documentation

[`pydantic.types.GetPydanticSchema`](/docs/validation/latest/api/pydantic/types/#pydantic.types.GetPydanticSchema)

You may notice that the above examples where we create a marker class require a good amount of boilerplate.
For many simple cases you can greatly minimize this by using `pydantic.GetPydanticSchema`:

```
from typing import Annotated

from pydantic_core import core_schema

from pydantic import BaseModel, GetPydanticSchema

class Model(BaseModel):
    y: Annotated[
        str,
        GetPydanticSchema(
            lambda tp, handler: core_schema.no_info_after_validator_function(
                lambda x: x * 2, handler(tp)
            )
        ),
    ]

assert Model(y='ab').y == 'abab'
```

#### Summary

Let’s recap:

1. Pydantic provides high level hooks to customize types via `Annotated` like `AfterValidator` and `Field`. Use these when possible.
2. Under the hood these use `pydantic-core` to customize validation, and you can hook into that directly using `GetPydanticSchema` or a marker class with `__get_pydantic_core_schema__`.
3. If you really want a custom type you can implement `__get_pydantic_core_schema__` on the type itself.

### Handling custom generic classes

You can use
[Generic Classes](https://docs.python.org/3/library/typing.html#typing.Generic) as
field types and perform custom validation based on the “type parameters” (or sub-types)
with `__get_pydantic_core_schema__`.

If the Generic class that you are using as a sub-type has a classmethod
`__get_pydantic_core_schema__`, you don’t need to use
[`arbitrary_types_allowed`](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.arbitrary_types_allowed) for it to work.

Because the `source_type` parameter is not the same as the `cls` parameter, you can use `typing.get_args` (or `typing_extensions.get_args`) to extract the generic parameters.
Then you can use the `handler` to generate a schema for them by calling `handler.generate_schema`.
Note that we do not do something like `handler(get_args(source_type)[0])` because we want to generate an unrelated
schema for that generic parameter, not one that is influenced by the current context of `Annotated` metadata and such.
This is less important for custom types, but crucial for annotated metadata that modifies schema building.

```
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from pydantic_core import CoreSchema, core_schema
from typing_extensions import get_args, get_origin

from pydantic import (
    BaseModel,
    GetCoreSchemaHandler,
    ValidationError,
    ValidatorFunctionWrapHandler,
)

ItemType = TypeVar('ItemType')

# This is not a pydantic model, it's an arbitrary generic class
@dataclass
class Owner(Generic[ItemType]):
    name: str
    item: ItemType

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        origin = get_origin(source_type)
        if origin is None:  # used as `x: Owner` without params
            origin = source_type
            item_tp = Any
        else:
            item_tp = get_args(source_type)[0]
        # both calling handler(...) and handler.generate_schema(...)
        # would work, but prefer the latter for conceptual and consistency reasons
        item_schema = handler.generate_schema(item_tp)

        def val_item(
            v: Owner[Any], handler: ValidatorFunctionWrapHandler
        ) -> Owner[Any]:
            v.item = handler(v.item)
            return v

        python_schema = core_schema.chain_schema(
            # `chain_schema` means do the following steps in order:
            [
                # Ensure the value is an instance of Owner
                core_schema.is_instance_schema(cls),
                # Use the item_schema to validate `items`
                core_schema.no_info_wrap_validator_function(
                    val_item, item_schema
                ),
            ]
        )

        return core_schema.json_or_python_schema(
            # for JSON accept an object with name and item keys
            json_schema=core_schema.chain_schema(
                [
                    core_schema.typed_dict_schema(
                        {
                            'name': core_schema.typed_dict_field(
                                core_schema.str_schema()
                            ),
                            'item': core_schema.typed_dict_field(item_schema),
                        }
                    ),
                    # after validating the json data convert it to python
                    core_schema.no_info_before_validator_function(
                        lambda data: Owner(
                            name=data['name'], item=data['item']
                        ),
                        # note that we reuse the same schema here as below
                        python_schema,
                    ),
                ]
            ),
            python_schema=python_schema,
        )

class Car(BaseModel):
    color: str

class House(BaseModel):
    rooms: int

class Model(BaseModel):
    car_owner: Owner[Car]
    home_owner: Owner[House]

model = Model(
    car_owner=Owner(name='John', item=Car(color='black')),
    home_owner=Owner(name='James', item=House(rooms=3)),
)
print(model)
"""
car_owner=Owner(name='John', item=Car(color='black')) home_owner=Owner(name='James', item=House(rooms=3))
"""

try:
    # If the values of the sub-types are invalid, we get an error
    Model(
        car_owner=Owner(name='John', item=House(rooms=3)),
        home_owner=Owner(name='James', item=Car(color='black')),
    )
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    wine
      Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='Kinda good', input_type=str]
    cheese
      Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='yeah', input_type=str]
    """

# Similarly with JSON
model = Model.model_validate_json(
    '{"car_owner":{"name":"John","item":{"color":"black"}},"home_owner":{"name":"James","item":{"rooms":3}}}'
)
print(model)
"""
car_owner=Owner(name='John', item=Car(color='black')) home_owner=Owner(name='James', item=House(rooms=3))
"""

try:
    Model.model_validate_json(
        '{"car_owner":{"name":"John","item":{"rooms":3}},"home_owner":{"name":"James","item":{"color":"black"}}}'
    )
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    car_owner.item.color
      Field required [type=missing, input_value={'rooms': 3}, input_type=dict]
    home_owner.item.rooms
      Field required [type=missing, input_value={'color': 'black'}, input_type=dict]
    """
```

#### Generic containers

The same idea can be applied to create generic container types, like a custom `Sequence` type:

```
from collections.abc import Sequence
from typing import Any, TypeVar

from pydantic_core import ValidationError, core_schema
from typing_extensions import get_args

from pydantic import BaseModel, GetCoreSchemaHandler

T = TypeVar('T')

class MySequence(Sequence[T]):
    def __init__(self, v: Sequence[T]):
        self.v = v

    def __getitem__(self, i):
        return self.v[i]

    def __len__(self):
        return len(self.v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        instance_schema = core_schema.is_instance_schema(cls)

        args = get_args(source)
        if args:
            # replace the type and rely on Pydantic to generate the right schema
            # for `Sequence`
            sequence_t_schema = handler.generate_schema(Sequence[args[0]])
        else:
            sequence_t_schema = handler.generate_schema(Sequence)

        non_instance_schema = core_schema.no_info_after_validator_function(
            MySequence, sequence_t_schema
        )
        return core_schema.union_schema([instance_schema, non_instance_schema])

class M(BaseModel):
    model_config = dict(validate_default=True)

    s1: MySequence = [3]

m = M()
print(m)
#> s1=<__main__.MySequence object at 0x0123456789ab>
print(m.s1.v)
#> [3]

class M(BaseModel):
    s1: MySequence[int]

M(s1=[1])
try:
    M(s1=['a'])
except ValidationError as exc:
    print(exc)
    """
    2 validation errors for M
    s1.is-instance[MySequence]
      Input should be an instance of MySequence [type=is_instance_of, input_value=['a'], input_type=list]
    s1.function-after[MySequence(), json-or-python[json=list[int],python=chain[is-instance[Sequence],function-wrap[sequence_validator()]]]].0
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
    """
```

### Access to field name

As of Pydantic V2.4, you can access the field name via the `handler.field_name` within `__get_pydantic_core_schema__`
and thereby set the field name which will be available from `info.field_name`.

```
from typing import Any

from pydantic_core import core_schema

from pydantic import BaseModel, GetCoreSchemaHandler, ValidationInfo

class CustomType:
    """Custom type that stores the field it was used in."""

    def __init__(self, value: int, field_name: str):
        self.value = value
        self.field_name = field_name

    def __repr__(self):
        return f'CustomType<{self.value} {self.field_name!r}>'

    @classmethod
    def validate(cls, value: int, info: ValidationInfo):
        return cls(value, info.field_name)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate, handler(int)
        )

class MyModel(BaseModel):
    my_field: CustomType

m = MyModel(my_field=1)
print(m.my_field)
#> CustomType<1 'my_field'>
```

You can also access `field_name` from the markers used with `Annotated`, like [`AfterValidator`](/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.AfterValidator).

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ValidationInfo

def my_validators(value: int, info: ValidationInfo):
    return f'<{value} {info.field_name!r}>'

class MyModel(BaseModel):
    my_field: Annotated[int, AfterValidator(my_validators)]

m = MyModel(my_field=1)
print(m.my_field)
#> <1 'my_field'>
```

Was this page helpful?

---

## 5. JSON Schema

API Documentation

[`pydantic.json_schema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema)

Pydantic allows automatic creation and customization of JSON schemas from models.
The generated JSON schemas are compliant with the following specifications:

* [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/release-notes.html)
* [OpenAPI Specification v3.1.0](https://github.com/OAI/OpenAPI-Specification).

## Generating JSON Schema

Use the following functions to generate JSON schema:

* [`BaseModel.model_json_schema`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema) returns a jsonable dict of a model’s schema.
* [`TypeAdapter.json_schema`](/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema) returns a jsonable dict of an adapted type’s schema.

Here’s an example of generating JSON schema from a `BaseModel`:

```
import json
from enum import Enum
from typing import Annotated, Union

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

class FooBar(BaseModel):
  count: int
  size: Union[float, None] = None

class Gender(str, Enum):
  male = 'male'
  female = 'female'
  other = 'other'
  not_given = 'not_given'

class MainModel(BaseModel):
  """
  This is the description of the main model
  """

  model_config = ConfigDict(title='Main')

  foo_bar: FooBar
  gender: Annotated[Union[Gender, None], Field(alias='Gender')] = None
  snap: int = Field(
      default=42,
      title='The Snap',
      description='this is the value of snap',
      gt=30,
      lt=50,
  )

main_model_schema = MainModel.model_json_schema()  # (1)
print(json.dumps(main_model_schema, indent=2))  # (2)
"""
{
"$defs": {
  "FooBar": {
    "properties": {
      "count": {
        "title": "Count",
        "type": "integer"
      },
      "size": {
        "anyOf": [
          {
            "type": "number"
          },
          {
            "type": "null"
          }
        ],
        "default": null,
        "title": "Size"
      }
    },
    "required": [
      "count"
    ],
    "title": "FooBar",
    "type": "object"
  },
  "Gender": {
    "enum": [
      "male",
      "female",
      "other",
      "not_given"
    ],
    "title": "Gender",
    "type": "string"
  }
},
"description": "This is the description of the main model",
"properties": {
  "foo_bar": {
    "$ref": "#/$defs/FooBar"
  },
  "Gender": {
    "anyOf": [
      {
        "$ref": "#/$defs/Gender"
      },
      {
        "type": "null"
      }
    ],
    "default": null
  },
  "snap": {
    "default": 42,
    "description": "this is the value of snap",
    "exclusiveMaximum": 50,
    "exclusiveMinimum": 30,
    "title": "The Snap",
    "type": "integer"
  }
},
"required": [
  "foo_bar"
],
"title": "Main",
"type": "object"
}
"""
```

This produces a "jsonable" dict of `MainModel`'s schema.

Calling `json.dumps` on the schema dict produces a JSON string.

The [`TypeAdapter`](/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter) class lets you create an object with methods for validating, serializing,
and producing JSON schemas for arbitrary types. This serves as a complete replacement for `schema_of` in
Pydantic V1 (which is now deprecated).

Here’s an example of generating JSON schema from a [`TypeAdapter`](/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter):

```
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
print(adapter.json_schema())
#> {'items': {'type': 'integer'}, 'type': 'array'}
```

You can also generate JSON schemas for combinations of [`BaseModel`s](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel)
and [`TypeAdapter`s](/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter), as shown in this example:

```
import json
from typing import Union

from pydantic import BaseModel, TypeAdapter

class Cat(BaseModel):
    name: str
    color: str

class Dog(BaseModel):
    name: str
    breed: str

ta = TypeAdapter(Union[Cat, Dog])
ta_schema = ta.json_schema()
print(json.dumps(ta_schema, indent=2))
```

**JSON output:**

```
{
  "$defs": {
    "Cat": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "color": {
          "title": "Color",
          "type": "string"
        }
      },
      "required": [
        "name",
        "color"
      ],
      "title": "Cat",
      "type": "object"
    },
    "Dog": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "breed": {
          "title": "Breed",
          "type": "string"
        }
      },
      "required": [
        "name",
        "breed"
      ],
      "title": "Dog",
      "type": "object"
    }
  },
  "anyOf": [
    {
      "$ref": "#/$defs/Cat"
    },
    {
      "$ref": "#/$defs/Dog"
    }
  ]
}
```

### Configuring the `JsonSchemaMode`

Specify the mode of JSON schema generation via the `mode` parameter in the
[`model_json_schema`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema) and
[`TypeAdapter.json_schema`](/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema) methods. By default, the mode is set to
`'validation'`, which produces a JSON schema corresponding to the model’s validation schema.

The [`JsonSchemaMode`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.JsonSchemaMode) is a type alias that represents the available options for the `mode` parameter:

* `'validation'`
* `'serialization'`

Here’s an example of how to specify the `mode` parameter, and how it affects the generated JSON schema:

```
from decimal import Decimal

from pydantic import BaseModel

class Model(BaseModel):
    a: Decimal = Decimal('12.34')

print(Model.model_json_schema(mode='validation'))
"""
{
    'properties': {
        'a': {
            'anyOf': [
                {'type': 'number'},
                {
                    'pattern': '^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$',
                    'type': 'string',
                },
            ],
            'default': '12.34',
            'title': 'A',
        }
    },
    'title': 'Model',
    'type': 'object',
}
"""

print(Model.model_json_schema(mode='serialization'))
"""
{
    'properties': {
        'a': {
            'default': '12.34',
            'pattern': '^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$',
            'title': 'A',
            'type': 'string',
        }
    },
    'title': 'Model',
    'type': 'object',
}
"""
```

## Customizing JSON Schema

The generated JSON schema can be customized at both the [field level](#field-level-customization) and [model level](#model-level-customization).

At both the field and model levels, you can use the [`json_schema_extra` option](#using-json_schema_extra) to add extra information to the JSON schema.

For custom types, Pydantic offers other tools for customizing JSON schema generation:

1. [`WithJsonSchema` annotation](#withjsonschema-annotation)
2. [`SkipJsonSchema` annotation](#skipjsonschema-annotation)
3. [Implementing `__get_pydantic_core_schema__`](#implementing_get_pydantic_core_schema)
4. [Implementing `__get_pydantic_json_schema__`](#implementing_get_pydantic_json_schema)

### Field-Level Customization

[Fields](/docs/validation/latest/concepts/fields) can have their JSON Schema customized. This is usually done using the [`Field()`](/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field)
function.

Some field parameters are used exclusively to customize the generated JSON Schema:

* `title`: The title of the field.
* `description`: The description of the field.
* `examples`: The examples of the field.
* `json_schema_extra`: Extra JSON Schema properties to be added to the field (see the [dedicated documentation](#using-json_schema_extra)).
* `field_title_generator`: A function that programmatically sets the field’s title, based on its name and info.

Here’s an example:

```
import json
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, SecretStr

class User(BaseModel):
  age: int = Field(description='Age of the user')
  email: Annotated[EmailStr, Field(examples=['[email protected]'])]  # (1)
  name: str = Field(title='Username')
  password: SecretStr = Field(
      json_schema_extra={
          'title': 'Password',
          'description': 'Password of the user',
          'examples': ['123456'],
      }
  )

print(json.dumps(User.model_json_schema(), indent=2))
"""
{
"properties": {
  "age": {
    "description": "Age of the user",
    "title": "Age",
    "type": "integer"
  },
  "email": {
    "examples": [
      "[email protected]"
    ],
    "format": "email",
    "title": "Email",
    "type": "string"
  },
  "name": {
    "title": "Username",
    "type": "string"
  },
  "password": {
    "description": "Password of the user",
    "examples": [
      "123456"
    ],
    "format": "password",
    "title": "Password",
    "type": "string",
    "writeOnly": true
  }
},
"required": [
  "age",
  "email",
  "name",
  "password"
],
"title": "User",
"type": "object"
}
"""
```

The [annotated pattern](/docs/validation/latest/concepts/fields#the-annotated-pattern) can also be used.

### Programmatic field title generation

The `field_title_generator` parameter can be used to programmatically generate the title for a field based on its name and info.

See the following example:

```
import json

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

def make_title(field_name: str, field_info: FieldInfo) -> str:
    return field_name.upper()

class Person(BaseModel):
    name: str = Field(field_title_generator=make_title)
    age: int = Field(field_title_generator=make_title)

print(json.dumps(Person.model_json_schema(), indent=2))
```

**JSON output:**

```
{
  "properties": {
    "name": {
      "title": "NAME",
      "type": "string"
    },
    "age": {
      "title": "AGE",
      "type": "integer"
    }
  },
  "required": [
    "name",
    "age"
  ],
  "title": "Person",
  "type": "object"
}
```

### Model-Level Customization

You can also use [model config](/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict) to customize JSON schema generation on a model.
Specifically, the following config options are relevant:

### Using `json_schema_extra`

The `json_schema_extra` option can be used to add extra information to the JSON schema, either at the
[Field level](#field-level-customization) or at the [Model level](#model-level-customization).
You can pass a `dict` or a `Callable` to `json_schema_extra`.

#### Using `json_schema_extra` with a `dict`

You can pass a `dict` to `json_schema_extra` to add extra information to the JSON schema:

```
import json

from pydantic import BaseModel, ConfigDict

class Model(BaseModel):
    a: str

    model_config = ConfigDict(json_schema_extra={'examples': [{'a': 'Foo'}]})

print(json.dumps(Model.model_json_schema(), indent=2))
```

**JSON output:**

```
{
  "examples": [
    {
      "a": "Foo"
    }
  ],
  "properties": {
    "a": {
      "title": "A",
      "type": "string"
    }
  },
  "required": [
    "a"
  ],
  "title": "Model",
  "type": "object"
}
```

#### Using `json_schema_extra` with a `Callable`

You can pass a `Callable` to `json_schema_extra` to modify the JSON schema with a function:

```
import json

from pydantic import BaseModel, Field

def pop_default(s):
    s.pop('default')

class Model(BaseModel):
    a: int = Field(default=1, json_schema_extra=pop_default)

print(json.dumps(Model.model_json_schema(), indent=2))
```

**JSON output:**

```
{
  "properties": {
    "a": {
      "title": "A",
      "type": "integer"
    }
  },
  "title": "Model",
  "type": "object"
}
```

#### Merging `json_schema_extra`

Starting in v2.9, Pydantic merges `json_schema_extra` dictionaries from annotated types.
This pattern offers a more additive approach to merging rather than the previous override behavior.
This can be quite helpful for cases of reusing json schema extra information across multiple types.

We viewed this change largely as a bug fix, as it resolves unintentional differences in the `json_schema_extra` merging behavior
between `BaseModel` and `TypeAdapter` instances - see [this issue](https://github.com/pydantic/pydantic/issues/9210)
for more details.

```
import json
from typing import Annotated

from typing_extensions import TypeAlias

from pydantic import Field, TypeAdapter

ExternalType: TypeAlias = Annotated[
    int, Field(json_schema_extra={'key1': 'value1'})
]

ta = TypeAdapter(
    Annotated[ExternalType, Field(json_schema_extra={'key2': 'value2'})]
)
print(json.dumps(ta.json_schema(), indent=2))
```

**JSON output:**

```
{
  "key1": "value1",
  "key2": "value2",
  "type": "integer"
}
```

### `WithJsonSchema` annotation

API Documentation

[`pydantic.json_schema.WithJsonSchema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.WithJsonSchema)

The [`WithJsonSchema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.WithJsonSchema) annotation can be used to override the generated (base)
JSON schema for a given type without the need to implement `__get_pydantic_core_schema__`
or `__get_pydantic_json_schema__` on the type itself. Note that this overrides the whole JSON Schema generation process
for the field (in the following example, the `'type'` also needs to be provided).

```
import json
from typing import Annotated

from pydantic import BaseModel, WithJsonSchema

MyInt = Annotated[
    int,
    WithJsonSchema({'type': 'integer', 'examples': [1, 0, -1]}),
]

class Model(BaseModel):
    a: MyInt

print(json.dumps(Model.model_json_schema(), indent=2))
```

**JSON output:**

```
{
  "properties": {
    "a": {
      "examples": [
        1,
        0,
        -1
      ],
      "title": "A",
      "type": "integer"
    }
  },
  "required": [
    "a"
  ],
  "title": "Model",
  "type": "object"
}
```

### `SkipJsonSchema` annotation

API Documentation

[`pydantic.json_schema.SkipJsonSchema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.SkipJsonSchema)

The [`SkipJsonSchema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.SkipJsonSchema) annotation can be used to skip an included field (or part of a field’s specifications)
from the generated JSON schema. See the API docs for more details.

### Implementing `__get_pydantic_core_schema__`

Custom types (used as `field_name: TheType` or `field_name: Annotated[TheType, ...]`) as well as `Annotated` metadata
(used as `field_name: Annotated[int, SomeMetadata]`)
can modify or override the generated schema by implementing `__get_pydantic_core_schema__`.
This method receives two positional arguments:

1. The type annotation that corresponds to this type (so in the case of `TheType[T](https://docs.python.org/3/library/functions.html#int)` it would be `TheType[int]`).
2. A handler/callback to call the next implementer of `__get_pydantic_core_schema__`.

The handler system works just like [*wrap* field validators](/docs/validation/latest/concepts/validators#field-wrap-validator).
In this case the input is the type and the output is a `core_schema`.

Here is an example of a custom type that *overrides* the generated `core_schema`:

```
from dataclasses import dataclass
from typing import Any

from pydantic_core import core_schema

from pydantic import BaseModel, GetCoreSchemaHandler

@dataclass
class CompressedString:
    dictionary: dict[int, str]
    text: list[int]

    def build(self) -> str:
        return ' '.join([self.dictionary[key] for key in self.text])

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        assert source is CompressedString
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )

    @staticmethod
    def _validate(value: str) -> 'CompressedString':
        inverse_dictionary: dict[str, int] = {}
        text: list[int] = []
        for word in value.split(' '):
            if word not in inverse_dictionary:
                inverse_dictionary[word] = len(inverse_dictionary)
            text.append(inverse_dictionary[word])
        return CompressedString(
            {v: k for k, v in inverse_dictionary.items()}, text
        )

    @staticmethod
    def _serialize(value: 'CompressedString') -> str:
        return value.build()

class MyModel(BaseModel):
    value: CompressedString

print(MyModel.model_json_schema())
"""
{
    'properties': {'value': {'title': 'Value', 'type': 'string'}},
    'required': ['value'],
    'title': 'MyModel',
    'type': 'object',
}
"""
print(MyModel(value='fox fox fox dog fox'))
"""
value = CompressedString(dictionary={0: 'fox', 1: 'dog'}, text=[0, 0, 0, 1, 0])
"""

print(MyModel(value='fox fox fox dog fox').model_dump(mode='json'))
#> {'value': 'fox fox fox dog fox'}
```

Since Pydantic would not know how to generate a schema for `CompressedString`, if you call `handler(source)` in its
`__get_pydantic_core_schema__` method you would get a `pydantic.errors.PydanticSchemaGenerationError` error.
This will be the case for most custom types, so you almost never want to call into `handler` for custom types.

The process for `Annotated` metadata is much the same except that you can generally call into `handler` to have
Pydantic handle generating the schema.

```
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Any

from pydantic_core import core_schema

from pydantic import BaseModel, GetCoreSchemaHandler, ValidationError

@dataclass
class RestrictCharacters:
    alphabet: Sequence[str]

    def __get_pydantic_core_schema__(
        self, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        if not self.alphabet:
            raise ValueError('Alphabet may not be empty')
        schema = handler(
            source
        )  # get the CoreSchema from the type / inner constraints
        if schema['type'] != 'str':
            raise TypeError('RestrictCharacters can only be applied to strings')
        return core_schema.no_info_after_validator_function(
            self.validate,
            schema,
        )

    def validate(self, value: str) -> str:
        if any(c not in self.alphabet for c in value):
            raise ValueError(
                f'{value!r} is not restricted to {self.alphabet!r}'
            )
        return value

class MyModel(BaseModel):
    value: Annotated[str, RestrictCharacters('ABC')]

print(MyModel.model_json_schema())
"""
{
    'properties': {'value': {'title': 'Value', 'type': 'string'}},
    'required': ['value'],
    'title': 'MyModel',
    'type': 'object',
}
"""
print(MyModel(value='CBA'))
#> value='CBA'

try:
    MyModel(value='XYZ')
except ValidationError as e:
    print(e)
    """
    1 validation error for MyModel
    value
      Value error, 'XYZ' is not restricted to 'ABC' [type=value_error, input_value='XYZ', input_type=str]
    """
```

So far we have been wrapping the schema, but if you just want to *modify* it or *ignore* it you can as well.

To modify the schema, first call the handler, then mutate the result:

```
from typing import Annotated, Any

from pydantic_core import ValidationError, core_schema

from pydantic import BaseModel, GetCoreSchemaHandler

class SmallString:
    def __get_pydantic_core_schema__(
        self,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        schema = handler(source)
        assert schema['type'] == 'str'
        schema['max_length'] = 10  # modify in place
        return schema

class MyModel(BaseModel):
    value: Annotated[str, SmallString()]

try:
    MyModel(value='too long!!!!!')
except ValidationError as e:
    print(e)
    """
    1 validation error for MyModel
    value
      String should have at most 10 characters [type=string_too_long, input_value='too long!!!!!', input_type=str]
    """
```

To override the schema completely, do not call the handler and return your own
`CoreSchema`:

```
from typing import Annotated, Any

from pydantic_core import ValidationError, core_schema

from pydantic import BaseModel, GetCoreSchemaHandler

class AllowAnySubclass:
    def __get_pydantic_core_schema__(
        self, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        # we can't call handler since it will fail for arbitrary types
        def validate(value: Any) -> Any:
            if not isinstance(value, source):
                raise ValueError(
                    f'Expected an instance of {source}, got an instance of {type(value)}'
                )

        return core_schema.no_info_plain_validator_function(validate)

class Foo:
    pass

class Model(BaseModel):
    f: Annotated[Foo, AllowAnySubclass()]

print(Model(f=Foo()))
#> f=None

class NotFoo:
    pass

try:
    Model(f=NotFoo())
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    f
      Value error, Expected an instance of <class '__main__.Foo'>, got an instance of <class '__main__.NotFoo'> [type=value_error, input_value=<__main__.NotFoo object at 0x0123456789ab>, input_type=NotFoo]
    """
```

### Implementing `__get_pydantic_json_schema__`

You can also implement `__get_pydantic_json_schema__` to modify or override the generated json schema.
Modifying this method only affects the JSON schema - it doesn’t affect the core schema, which is used for validation and serialization.

Here’s an example of modifying the generated JSON schema:

```
import json
from typing import Any

from pydantic_core import core_schema as cs

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, TypeAdapter
from pydantic.json_schema import JsonSchemaValue

class Person:
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> cs.CoreSchema:
        return cs.typed_dict_schema(
            {
                'name': cs.typed_dict_field(cs.str_schema()),
                'age': cs.typed_dict_field(cs.int_schema()),
            },
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema['examples'] = [
            {
                'name': 'John Doe',
                'age': 25,
            }
        ]
        json_schema['title'] = 'Person'
        return json_schema

print(json.dumps(TypeAdapter(Person).json_schema(), indent=2))
"""
{
  "examples": [
    {
      "age": 25,
      "name": "John Doe"
    }
  ],
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "age": {
      "title": "Age",
      "type": "integer"
    }
  },
  "required": [
    "name",
    "age"
  ],
  "title": "Person",
  "type": "object"
}
"""
```

### Using `field_title_generator`

The `field_title_generator` parameter can be used to programmatically generate the title for a field based on its name and info.
This is similar to the field level `field_title_generator`, but the `ConfigDict` option will be applied to all fields of the class.

See the following example:

```
import json

from pydantic import BaseModel, ConfigDict

class Person(BaseModel):
    model_config = ConfigDict(
        field_title_generator=lambda field_name, field_info: field_name.upper()
    )
    name: str
    age: int

print(json.dumps(Person.model_json_schema(), indent=2))
```

**JSON output:**

```
{
  "properties": {
    "name": {
      "title": "NAME",
      "type": "string"
    },
    "age": {
      "title": "AGE",
      "type": "integer"
    }
  },
  "required": [
    "name",
    "age"
  ],
  "title": "Person",
  "type": "object"
}
```

### Using `model_title_generator`

The `model_title_generator` config option is similar to the `field_title_generator` option, but it applies to the title of the model itself,
and accepts the model class as input.

See the following example:

```
import json

from pydantic import BaseModel, ConfigDict

def make_title(model: type) -> str:
    return f'Title-{model.__name__}'

class Person(BaseModel):
    model_config = ConfigDict(model_title_generator=make_title)
    name: str
    age: int

print(json.dumps(Person.model_json_schema(), indent=2))
```

**JSON output:**

```
{
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "age": {
      "title": "Age",
      "type": "integer"
    }
  },
  "required": [
    "name",
    "age"
  ],
  "title": "Title-Person",
  "type": "object"
}
```

## JSON schema types

Types, custom field types, and constraints (like `max_length`) are mapped to the corresponding spec formats in the
following priority order (when there is an equivalent available):

1. [JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core)
2. [JSON Schema Validation](https://json-schema.org/draft/2020-12/json-schema-validation)
3. [OpenAPI Data Types](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#data-types)
4. The standard `format` JSON field is used to define Pydantic extensions for more complex `string` sub-types.

The field schema mapping from Python or Pydantic to JSON schema is done as follows:

| Python type | JSON Schema Type | Additional JSON Schema | Defined in | Notes |
| --- | --- | --- | --- | --- |
| `None` | `null` |  | JSON Schema Core | Same for `type(None)` or `Literal[None]` |
| `bool` | `boolean` |  | JSON Schema Core |  |
| `str` | `string` |  | JSON Schema Core |  |
| `float` | `number` |  | JSON Schema Core |  |
| `int` | `integer` |  | JSON Schema Validation |  |
| `dict` | `object` |  | JSON Schema Core |  |
| `list` | `array` | `\{"items": \{\}\}` | JSON Schema Core |  |
| `tuple-positional` | `array` | `\{"items": \{\}\}` | JSON Schema Core |  |
| `tuple-variable` | `array` | `\{"items": \{\}\}` | JSON Schema Core |  |
| `set` | `array` | `\{"uniqueItems": true, "items": \{\}\}` | JSON Schema Validation |  |
| `frozenset` | `array` | `\{"uniqueItems": true, "items": \{\}\}` | JSON Schema Validation |  |
| `List[str]` | `array` | `\{"items": \{"type": "string"\}\}` | JSON Schema Validation | And equivalently for any other sub type, e.g. `List[int]`. |
| `Tuple[str, ...]` | `array` | `\{"items": \{"type": "string"\}\}` | JSON Schema Validation | And equivalently for any other sub type, e.g. `Tuple[int, ...]`. |
| `Tuple[str, int]` | `array` | `\{"minItems": 2, "maxItems": 2, "items": [\{"type": "string"\}, \{"type": "integer"\}]\}` | JSON Schema Validation | And equivalently for any other set of subtypes. Note: If using schemas for OpenAPI, you shouldn’t use this declaration, as it would not be valid in OpenAPI (although it is valid in JSON Schema). |
| `Dict[str, int]` | `object` | `\{"additionalProperties": \{"type": "integer"\}\}` | JSON Schema Validation | And equivalently for any other subfields for dicts. Have in mind that although you can use other types as keys for dicts with Pydantic, only strings are valid keys for JSON, and so, only str is valid as JSON Schema key types. |
| `Union[str, int]` | `anyOf` | `\{"anyOf": [\{"type": "string"\}, \{"type": "integer"\}]\}` | JSON Schema Validation | And equivalently for any other subfields for unions. |
| `Enum` | `enum` | `\{"enum": [...]\}` | JSON Schema Validation | All the literal values in the enum are included in the definition. |
| `SecretStr` | `string` | `\{"writeOnly": true\}` | JSON Schema Validation |  |
| `SecretBytes` | `string` | `\{"writeOnly": true\}` | JSON Schema Validation |  |
| `EmailStr` | `string` | `\{"format": "email"\}` | JSON Schema Validation |  |
| `NameEmail` | `string` | `\{"format": "name-email"\}` | Pydantic standard “format” extension |  |
| `AnyUrl` | `string` | `\{"format": "uri"\}` | JSON Schema Validation |  |
| `Pattern` | `string` | `\{"format": "regex"\}` | JSON Schema Validation |  |
| `bytes` | `string` | `\{"format": "binary"\}` | OpenAPI |  |
| `Decimal` | `number` |  | JSON Schema Core |  |
| `UUID1` | `string` | `\{"format": "uuid1"\}` | Pydantic standard “format” extension |  |
| `UUID3` | `string` | `\{"format": "uuid3"\}` | Pydantic standard “format” extension |  |
| `UUID4` | `string` | `\{"format": "uuid4"\}` | Pydantic standard “format” extension |  |
| `UUID5` | `string` | `\{"format": "uuid5"\}` | Pydantic standard “format” extension |  |
| `UUID` | `string` | `\{"format": "uuid"\}` | Pydantic standard “format” extension | Suggested in OpenAPI. |
| `FilePath` | `string` | `\{"format": "file-path"\}` | Pydantic standard “format” extension |  |
| `DirectoryPath` | `string` | `\{"format": "directory-path"\}` | Pydantic standard “format” extension |  |
| `Path` | `string` | `\{"format": "path"\}` | Pydantic standard “format” extension |  |
| `datetime` | `string` | `\{"format": "date-time"\}` | JSON Schema Validation |  |
| `date` | `string` | `\{"format": "date"\}` | JSON Schema Validation |  |
| `time` | `string` | `\{"format": "time"\}` | JSON Schema Validation |  |
| `timedelta` | `number` | `\{"format": "time-delta"\}` | Difference in seconds (a `float`), with Pydantic standard “format” extension | Suggested in JSON Schema repository’s issues by maintainer. |
| `Json` | `string` | `\{"format": "json-string"\}` | Pydantic standard “format” extension |  |
| `IPv4Address` | `string` | `\{"format": "ipv4"\}` | JSON Schema Validation |  |
| `IPv6Address` | `string` | `\{"format": "ipv6"\}` | JSON Schema Validation |  |
| `IPvAnyAddress` | `string` | `\{"format": "ipvanyaddress"\}` | Pydantic standard “format” extension | IPv4 or IPv6 address as used in `ipaddress` module |
| `IPv4Interface` | `string` | `\{"format": "ipv4interface"\}` | Pydantic standard “format” extension | IPv4 interface as used in `ipaddress` module |
| `IPv6Interface` | `string` | `\{"format": "ipv6interface"\}` | Pydantic standard “format” extension | IPv6 interface as used in `ipaddress` module |
| `IPvAnyInterface` | `string` | `\{"format": "ipvanyinterface"\}` | Pydantic standard “format” extension | IPv4 or IPv6 interface as used in `ipaddress` module |
| `IPv4Network` | `string` | `\{"format": "ipv4network"\}` | Pydantic standard “format” extension | IPv4 network as used in `ipaddress` module |
| `IPv6Network` | `string` | `\{"format": "ipv6network"\}` | Pydantic standard “format” extension | IPv6 network as used in `ipaddress` module |
| `IPvAnyNetwork` | `string` | `\{"format": "ipvanynetwork"\}` | Pydantic standard “format” extension | IPv4 or IPv6 network as used in `ipaddress` module |
| `StrictBool` | `boolean` |  | JSON Schema Core |  |
| `StrictStr` | `string` |  | JSON Schema Core |  |
| `ConstrainedStr` | `string` |  | JSON Schema Core | If the type has values declared for the constraints, they are included as validations. See the mapping for `constr` below. |
| `constr(pattern=‘^text |  |  |  |  |

## Top-level schema generation

You can also generate a top-level JSON schema that only includes a list of models and related
sub-models in its `$defs`:

```
import json

from pydantic import BaseModel
from pydantic.json_schema import models_json_schema

class Foo(BaseModel):
    a: str = None

class Model(BaseModel):
    b: Foo

class Bar(BaseModel):
    c: int

_, top_level_schema = models_json_schema(
    [(Model, 'validation'), (Bar, 'validation')], title='My Schema'
)
print(json.dumps(top_level_schema, indent=2))
```

**JSON output:**

```
{
  "$defs": {
    "Bar": {
      "properties": {
        "c": {
          "title": "C",
          "type": "integer"
        }
      },
      "required": [
        "c"
      ],
      "title": "Bar",
      "type": "object"
    },
    "Foo": {
      "properties": {
        "a": {
          "default": null,
          "title": "A",
          "type": "string"
        }
      },
      "title": "Foo",
      "type": "object"
    },
    "Model": {
      "properties": {
        "b": {
          "$ref": "#/$defs/Foo"
        }
      },
      "required": [
        "b"
      ],
      "title": "Model",
      "type": "object"
    }
  },
  "title": "My Schema"
}
```

## Customizing the JSON Schema Generation Process

API Documentation

[`pydantic.json_schema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema)

If you need custom schema generation, you can use a `schema_generator`, modifying the
[`GenerateJsonSchema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema) class as necessary for your application.

The various methods that can be used to produce JSON schema accept a keyword argument `schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema`, and you can pass your custom subclass to these methods in order to use your own approach to generating JSON schema.

`GenerateJsonSchema` implements the translation of a type’s `pydantic-core` schema into a JSON schema.
By design, this class breaks the JSON schema generation process into smaller methods that can be easily overridden in
subclasses to modify the “global” approach to generating JSON schema.

```
from pydantic import BaseModel
from pydantic.json_schema import GenerateJsonSchema

class MyGenerateJsonSchema(GenerateJsonSchema):
    def generate(self, schema, mode='validation'):
        json_schema = super().generate(schema, mode=mode)
        json_schema['title'] = 'Customize title'
        json_schema['$schema'] = self.schema_dialect
        return json_schema

class MyModel(BaseModel):
    x: int

print(MyModel.model_json_schema(schema_generator=MyGenerateJsonSchema))
"""
{
    'properties': {'x': {'title': 'X', 'type': 'integer'}},
    'required': ['x'],
    'title': 'Customize title',
    'type': 'object',
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
}
"""
```

Below is an approach you can use to exclude any fields from the schema that don’t have valid json schemas:

```
from typing import Callable

from pydantic_core import PydanticOmit, core_schema

from pydantic import BaseModel
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue

class MyGenerateJsonSchema(GenerateJsonSchema):
    def handle_invalid_for_json_schema(
        self, schema: core_schema.CoreSchema, error_info: str
    ) -> JsonSchemaValue:
        raise PydanticOmit

def example_callable():
    return 1

class Example(BaseModel):
    name: str = 'example'
    function: Callable = example_callable

instance_example = Example()

validation_schema = instance_example.model_json_schema(
    schema_generator=MyGenerateJsonSchema, mode='validation'
)
print(validation_schema)
"""
{
    'properties': {
        'name': {'default': 'example', 'title': 'Name', 'type': 'string'}
    },
    'title': 'Example',
    'type': 'object',
}
"""
```

### JSON schema sorting

By default, Pydantic recursively sorts JSON schemas by alphabetically sorting keys. Notably, Pydantic skips sorting the values of the `properties` key,
to preserve the order of the fields as they were defined in the model.

If you would like to customize this behavior, you can override the `sort` method in your custom `GenerateJsonSchema` subclass. The below example
uses a no-op `sort` method to disable sorting entirely, which is reflected in the preserved order of the model fields and `json_schema_extra` keys:

```
import json
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue

class MyGenerateJsonSchema(GenerateJsonSchema):
    def sort(
        self, value: JsonSchemaValue, parent_key: Optional[str] = None
    ) -> JsonSchemaValue:
        """No-op, we don't want to sort schema values at all."""
        return value

class Bar(BaseModel):
    c: str
    b: str
    a: str = Field(json_schema_extra={'c': 'hi', 'b': 'hello', 'a': 'world'})

json_schema = Bar.model_json_schema(schema_generator=MyGenerateJsonSchema)
print(json.dumps(json_schema, indent=2))
```

**JSON output:**

```
{
  "type": "object",
  "properties": {
    "c": {
      "type": "string",
      "title": "C"
    },
    "b": {
      "type": "string",
      "title": "B"
    },
    "a": {
      "type": "string",
      "c": "hi",
      "b": "hello",
      "a": "world",
      "title": "A"
    }
  },
  "required": [
    "c",
    "b",
    "a"
  ],
  "title": "Bar"
}
```

## Customizing the `$ref`s in JSON Schema

The format of `$ref`s can be altered by calling [`model_json_schema()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema)
or [`model_dump_json()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json) with the `ref_template` keyword argument.
The definitions are always stored under the key `$defs`, but a specified prefix can be used for the references.

This is useful if you need to extend or modify the JSON schema default definitions location. For example, with OpenAPI:

```
import json

from pydantic import BaseModel
from pydantic.type_adapter import TypeAdapter

class Foo(BaseModel):
    a: int

class Model(BaseModel):
    a: Foo

adapter = TypeAdapter(Model)

print(
    json.dumps(
        adapter.json_schema(ref_template='#/components/schemas/{model}'),
        indent=2,
    )
)
```

**JSON output:**

```
{
  "$defs": {
    "Foo": {
      "properties": {
        "a": {
          "title": "A",
          "type": "integer"
        }
      },
      "required": [
        "a"
      ],
      "title": "Foo",
      "type": "object"
    }
  },
  "properties": {
    "a": {
      "$ref": "#/components/schemas/Foo"
    }
  },
  "required": [
    "a"
  ],
  "title": "Model",
  "type": "object"
}
```

## Miscellaneous Notes on JSON Schema Generation

* The JSON schema for `Optional` fields indicates that the value `null` is allowed.
* The `Decimal` type is exposed in JSON schema (and serialized) as a string.
* Since the `namedtuple` type doesn’t exist in JSON, a model’s JSON schema does not preserve `namedtuple`s as `namedtuple`s.
* Sub-models used are added to the `$defs` JSON attribute and referenced, as per the spec.
* Sub-models with modifications (via the `Field` class) like a custom title, description, or default value,
  are recursively included instead of referenced.
* The `description` for models is taken from either the docstring of the class or the argument `description` to
  the `Field` class.
* The schema is generated by default using aliases as keys, but it can be generated using model
  property names instead by calling [`model_json_schema()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema) or
  [`model_dump_json()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json) with the `by_alias=False` keyword argument.
  , min\_length=2, max\_length=10)`|`string`| | JSON Schema Validation | Any argument not passed to the function (not defined) will not be included in the schema. | |`ConstrainedInt`|`integer`| | JSON Schema Core | If the type has values declared for the constraints, they are included as validations. See the mapping for`conint`below. | |`conint(gt=1, ge=2, lt=6, le=5, multiple\_of=2)`|`integer`|`{“maximum”: 5, “exclusiveMaximum”: 6, “minimum”: 2, “exclusiveMinimum”: 1, “multipleOf”: 2}`| | Any argument not passed to the function (not defined) will not be included in the schema. | |`PositiveInt`|`integer`|`{“exclusiveMinimum”: 0}`| JSON Schema Validation | | |`NegativeInt`|`integer`|`{“exclusiveMaximum”: 0}`| JSON Schema Validation | | |`NonNegativeInt`|`integer`|`{“minimum”: 0}`| JSON Schema Validation | | |`NonPositiveInt`|`integer`|`{“maximum”: 0}`| JSON Schema Validation | | |`ConstrainedFloat`|`number`| | JSON Schema Core | If the type has values declared for the constraints, they are included as validations. See the mapping for`confloat`below. | |`confloat(gt=1, ge=2, lt=6, le=5, multiple\_of=2)`|`number`|`{“maximum”: 5, “exclusiveMaximum”: 6, “minimum”: 2, “exclusiveMinimum”: 1, “multipleOf”: 2}`| JSON Schema Validation | Any argument not passed to the function (not defined) will not be included in the schema. | |`PositiveFloat`|`number`|`{“exclusiveMinimum”: 0}`| JSON Schema Validation | | |`NegativeFloat`|`number`|`{“exclusiveMaximum”: 0}`| JSON Schema Validation | | |`NonNegativeFloat`|`number`|`{“minimum”: 0}`| JSON Schema Validation | | |`NonPositiveFloat`|`number`|`{“maximum”: 0}`| JSON Schema Validation | | |`ConstrainedDecimal`|`number`| | JSON Schema Core | If the type has values declared for the constraints, they are included as validations. See the mapping for`condecimal`below. | |`condecimal(gt=1, ge=2, lt=6, le=5, multiple\_of=2)`|`number`|`{“maximum”: 5, “exclusiveMaximum”: 6, “minimum”: 2, “exclusiveMinimum”: 1, “multipleOf”: 2}`| JSON Schema Validation | Any argument not passed to the function (not defined) will not be included in the schema. | |`BaseModel`|`object`| | JSON Schema Core | All the properties defined will be defined with standard JSON Schema, including submodels. | |`Color`|`string`|`{“format”: “color”}` | Pydantic standard “format” extension | |

## Top-level schema generation

You can also generate a top-level JSON schema that only includes a list of models and related
sub-models in its `$defs`:

```
import json

from pydantic import BaseModel
from pydantic.json_schema import models_json_schema

class Foo(BaseModel):
    a: str = None

class Model(BaseModel):
    b: Foo

class Bar(BaseModel):
    c: int

_, top_level_schema = models_json_schema(
    [(Model, 'validation'), (Bar, 'validation')], title='My Schema'
)
print(json.dumps(top_level_schema, indent=2))
```

**JSON output:**

```
{
  "$defs": {
    "Bar": {
      "properties": {
        "c": {
          "title": "C",
          "type": "integer"
        }
      },
      "required": [
        "c"
      ],
      "title": "Bar",
      "type": "object"
    },
    "Foo": {
      "properties": {
        "a": {
          "default": null,
          "title": "A",
          "type": "string"
        }
      },
      "title": "Foo",
      "type": "object"
    },
    "Model": {
      "properties": {
        "b": {
          "$ref": "#/$defs/Foo"
        }
      },
      "required": [
        "b"
      ],
      "title": "Model",
      "type": "object"
    }
  },
  "title": "My Schema"
}
```

## Customizing the JSON Schema Generation Process

API Documentation

[`pydantic.json_schema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema)

If you need custom schema generation, you can use a `schema_generator`, modifying the
[`GenerateJsonSchema`](/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema) class as necessary for your application.

The various methods that can be used to produce JSON schema accept a keyword argument `schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema`, and you can pass your custom subclass to these methods in order to use your own approach to generating JSON schema.

`GenerateJsonSchema` implements the translation of a type’s `pydantic-core` schema into a JSON schema.
By design, this class breaks the JSON schema generation process into smaller methods that can be easily overridden in
subclasses to modify the “global” approach to generating JSON schema.

```
from pydantic import BaseModel
from pydantic.json_schema import GenerateJsonSchema

class MyGenerateJsonSchema(GenerateJsonSchema):
    def generate(self, schema, mode='validation'):
        json_schema = super().generate(schema, mode=mode)
        json_schema['title'] = 'Customize title'
        json_schema['$schema'] = self.schema_dialect
        return json_schema

class MyModel(BaseModel):
    x: int

print(MyModel.model_json_schema(schema_generator=MyGenerateJsonSchema))
"""
{
    'properties': {'x': {'title': 'X', 'type': 'integer'}},
    'required': ['x'],
    'title': 'Customize title',
    'type': 'object',
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
}
"""
```

Below is an approach you can use to exclude any fields from the schema that don’t have valid json schemas:

```
from typing import Callable

from pydantic_core import PydanticOmit, core_schema

from pydantic import BaseModel
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue

class MyGenerateJsonSchema(GenerateJsonSchema):
    def handle_invalid_for_json_schema(
        self, schema: core_schema.CoreSchema, error_info: str
    ) -> JsonSchemaValue:
        raise PydanticOmit

def example_callable():
    return 1

class Example(BaseModel):
    name: str = 'example'
    function: Callable = example_callable

instance_example = Example()

validation_schema = instance_example.model_json_schema(
    schema_generator=MyGenerateJsonSchema, mode='validation'
)
print(validation_schema)
"""
{
    'properties': {
        'name': {'default': 'example', 'title': 'Name', 'type': 'string'}
    },
    'title': 'Example',
    'type': 'object',
}
"""
```

### JSON schema sorting

By default, Pydantic recursively sorts JSON schemas by alphabetically sorting keys. Notably, Pydantic skips sorting the values of the `properties` key,
to preserve the order of the fields as they were defined in the model.

If you would like to customize this behavior, you can override the `sort` method in your custom `GenerateJsonSchema` subclass. The below example
uses a no-op `sort` method to disable sorting entirely, which is reflected in the preserved order of the model fields and `json_schema_extra` keys:

```
import json
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue

class MyGenerateJsonSchema(GenerateJsonSchema):
    def sort(
        self, value: JsonSchemaValue, parent_key: Optional[str] = None
    ) -> JsonSchemaValue:
        """No-op, we don't want to sort schema values at all."""
        return value

class Bar(BaseModel):
    c: str
    b: str
    a: str = Field(json_schema_extra={'c': 'hi', 'b': 'hello', 'a': 'world'})

json_schema = Bar.model_json_schema(schema_generator=MyGenerateJsonSchema)
print(json.dumps(json_schema, indent=2))
```

**JSON output:**

```
{
  "type": "object",
  "properties": {
    "c": {
      "type": "string",
      "title": "C"
    },
    "b": {
      "type": "string",
      "title": "B"
    },
    "a": {
      "type": "string",
      "c": "hi",
      "b": "hello",
      "a": "world",
      "title": "A"
    }
  },
  "required": [
    "c",
    "b",
    "a"
  ],
  "title": "Bar"
}
```

## Customizing the `$ref`s in JSON Schema

The format of `$ref`s can be altered by calling [`model_json_schema()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema)
or [`model_dump_json()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json) with the `ref_template` keyword argument.
The definitions are always stored under the key `$defs`, but a specified prefix can be used for the references.

This is useful if you need to extend or modify the JSON schema default definitions location. For example, with OpenAPI:

```
import json

from pydantic import BaseModel
from pydantic.type_adapter import TypeAdapter

class Foo(BaseModel):
    a: int

class Model(BaseModel):
    a: Foo

adapter = TypeAdapter(Model)

print(
    json.dumps(
        adapter.json_schema(ref_template='#/components/schemas/{model}'),
        indent=2,
    )
)
```

**JSON output:**

```
{
  "$defs": {
    "Foo": {
      "properties": {
        "a": {
          "title": "A",
          "type": "integer"
        }
      },
      "required": [
        "a"
      ],
      "title": "Foo",
      "type": "object"
    }
  },
  "properties": {
    "a": {
      "$ref": "#/components/schemas/Foo"
    }
  },
  "required": [
    "a"
  ],
  "title": "Model",
  "type": "object"
}
```

## Miscellaneous Notes on JSON Schema Generation

* The JSON schema for `Optional` fields indicates that the value `null` is allowed.
* The `Decimal` type is exposed in JSON schema (and serialized) as a string.
* Since the `namedtuple` type doesn’t exist in JSON, a model’s JSON schema does not preserve `namedtuple`s as `namedtuple`s.
* Sub-models used are added to the `$defs` JSON attribute and referenced, as per the spec.
* Sub-models with modifications (via the `Field` class) like a custom title, description, or default value,
  are recursively included instead of referenced.
* The `description` for models is taken from either the docstring of the class or the argument `description` to
  the `Field` class.
* The schema is generated by default using aliases as keys, but it can be generated using model
  property names instead by calling [`model_json_schema()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema) or
  [`model_dump_json()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json) with the `by_alias=False` keyword argument.

Was this page helpful?

---

## Bibliography

1. [Models](https://docs.pydantic.dev/latest/concepts/models/)
2. [Fields](https://docs.pydantic.dev/latest/concepts/fields/)
3. [Validators](https://docs.pydantic.dev/latest/concepts/validators/)
4. [Types](https://docs.pydantic.dev/latest/concepts/types/)
5. [JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)