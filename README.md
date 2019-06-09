# mimid

[![Build Status](https://travis-ci.org/konradhalas/mimid.svg?branch=master)](https://travis-ci.org/konradhalas/mimid)
[![Coverage Status](https://coveralls.io/repos/github/konradhalas/mimid/badge.svg?branch=master)](https://coveralls.io/github/konradhalas/mimid?branch=master)

Mocking library for Python.

## Installation

To install `mimid`, simply use `pip`:

```
$ pip install mimid
```

## Quick start


```python
from mimid import mock, every, verify

class Calc:
    def add(self, a, b):
        return a + b

def test_add():
    calc_mock = mock(Calc)
    every(calc_mock.add).returns(5)    
    
    result = calc_mock.add(2, 2)
    
    assert result == 5
    verify(calc_mock.add).with_args(2, 2).called_once()
```

## Why not `unittest.mock`?

Python built-in `mock` module is an awesome tool. It's a first choice if you want to mock something in you tests.

However it has a few disadvantages:

- it doesn't work well with modern IDEs (e.g. auto completion)
- it doesn't work well with type hinted code
- it's difficult to define different behaviours for different call arguments
- it allows too much freedom