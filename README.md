# mimid

[![Build Status](https://travis-ci.org/konradhalas/mimid.svg?branch=master)](https://travis-ci.org/konradhalas/mimid)
[![Coverage Status](https://coveralls.io/repos/github/konradhalas/mimid/badge.svg?branch=master)](https://coveralls.io/github/konradhalas/mimid?branch=master)
[![License](https://img.shields.io/pypi/l/mimid.svg)](https://pypi.python.org/pypi/mimid/)
[![Version](https://img.shields.io/pypi/v/mimid.svg)](https://pypi.python.org/pypi/mimid/)
[![Python versions](https://img.shields.io/pypi/pyversions/mimid.svg)](https://pypi.python.org/pypi/mimid/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Modern mocking library for Python.

**⚠️ This project is under heavy development, API could be unstable.**

## Installation

To install `mimid`, simply use `pip`:

```
$ pip install mimid
```

## Quick start


```python
from mimid import mock, every, verify, any, gt

def add(a: int, b: int) -> int:
    return a + b

def test_add():
    add_mock = mock(add)
    every(add_mock).returns(5)    
    
    result = add_mock(2, 2)
    
    assert result == 5
    verify(add_mock).with_args(any(), gt(0)).called(times=1)
```

## Features

Mimid supports following features:

- easy mock behaviour configuration and verification
- works with classes and plain functions
- fully type hinted - it works with IDE's and type checkers
- clean API - not too much magic

## Why not `mock`?

Python built-in `mock` module is an awesome tool. It's a first choice if you want to mock something in your tests.

However it has a few disadvantages:

- it doesn't work well with modern IDEs (e.g. auto completion) and type checkers
- it's difficult to define different behaviours for different cases
- it allows too much freedom, you can do anything with your mock object, even if you didn't define any behaviour

## Inspiration

Mimid is highly inspired by mocking frameworks from a JVM world, like [mockito] or [mockk].

## Usage

There are 3 simple steps in the `mimid` mocking workflow:

1. [Creation](#creation)
2. [Configuration](#configuration)
3. [Verification](#verification)

Additionally you can use [matchers](#matchers) in both configuration and verification steps. 

### Creation

You have to use `mock` function to create your mock object. It works both with classes and functions.

Class example:

```python
from mimid import mock

class A:

    def foo(self, param):
        pass
        
class_mock = mock(A) 
```

Function example:

```python
from mimid import mock

def foo(param):
    pass

function_mock = mock(foo)
```

### Configuration

Before you call your mock (function or method) you have to configure its behaviour. Use `every` with additional
methods (`returns`, `raises`, ...) to define how it should works during your test.

```python
from mimid import mock, every

def foo(param):
    pass

function_mock = mock(foo)
every(function_mock).returns(1)
``` 

You can also specify arguments which should trigger defined behaviour.

```python
from mimid import mock, every

def foo(param):
    pass

function_mock = mock(foo)
every(function_mock).with_args(param=2).returns(1)
every(function_mock).with_args(param=3).raises(Exception())
```

If you want to define property behaviour you have to use `prop` function:

```python
from mimid import mock, every, prop

class A:
    
    @property
    def x(self) -> int:
        pass
        
class_mock = mock(A) 
every(prop(class_mock).x).returns(1)
```

Available configurations:

| Configuration    | Description                           |
| ---------------- | ------------------------------------- |
| `returns`        | return given value                    |
| `returns_many`   | return each value from provided list  |
| `raises`         | raise given exception                 | 
| `execute`        | call given callable                   | 

### Verification

At the end of your test you can check if mock was called as expected with `verify`.

```python
from mimid import mock, verify

def foo(param):
    pass

function_mock = mock(foo)

... # mock calls

verify(function_mock).called(times=2)
```

You can use the same `with_args` also during verification step:

```python
from mimid import mock, verify

def foo(param):
    pass

function_mock = mock(foo)

... # mock calls

verify(function_mock).with_args(param=1).called(times=2)
```

### Matchers

You can use matchers during configuration (`with_args`) and verification (`with_args`, `called`) steps. You can also combine matchers with `|` or `&` and negate it with `~`.

Example:

```python
from mimid import mock, every, verify, gt, lt, gte

def foo(param):
    pass

function_mock = mock(foo)
every(function_mock).with_args(gt(0)).returns(1)

result = function_mock(10)

assert result == 1
verify(function_mock).with_args(gt(5) | lt(15)).called(times=gte(1))

```

`capture` is a special matcher - it behaves like `any()` but additionally it 
stores given argument in provided slot.

Example:

```python
from mimid import mock, every, slot, capture

def foo(param):
    pass

function_mock = mock(foo)
param_slot = slot()
every(function_mock).with_args(capture(param_slot)).execute(lambda: param_slot.value + 1)

result = function_mock(1)

assert result == 2
assert param_slot.value == 1

```

Available matchers:

| Matcher          | Description                           |
| ---------------- | ------------------------------------- |
| `any`            | match any value                       |
| `eq`             | match equal value                     |
| `lt`             | match lower value                     | 
| `lte`            | match lower or equal value            | 
| `gt`             | match greater value                   | 
| `gte`            | match greater or equal value          | 
| `capture`        | capture provided argument             | 

## Authors

Created by [Konrad Hałas][halas-homepage].

[halas-homepage]: https://konradhalas.pl
[mockito]: https://site.mockito.org
[mockk]: https://github.com/mockk/mockk
