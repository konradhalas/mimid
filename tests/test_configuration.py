import pytest

from mimid import mock, every, CallNotConfiguredException
from tests.targets import A, Error, function


def test_mock_method_call_returns_configured_value():
    obj = mock(A)
    every(obj.method).returns(2)

    result = obj.method(1)

    assert result == 2


def test_mock_method_call_raises_exception_when_call_is_not_configured():
    obj = mock(A)

    with pytest.raises(CallNotConfiguredException):
        obj.method(1)


def test_mock_method_call_raises_exception_when_called_with_non_matching_arguments():
    obj = mock(A)
    every(obj.method).with_args(1).returns(2)

    with pytest.raises(CallNotConfiguredException):
        obj.method(2)


def test_mock_method_call_returns_configured_value_when_called_with_matching_arguments():
    obj = mock(A)
    every(obj.method).with_args(1).returns(2)

    result = obj.method(1)

    assert result == 2


def test_mock_method_call_returns_configured_value_when_called_with_matching_arguments_and_multiple_configurations():
    obj = mock(A)
    every(obj.method).with_args(1).returns(2)
    every(obj.method).with_args(3).returns(4)

    result_1 = obj.method(1)
    result_2 = obj.method(3)

    assert result_1 == 2
    assert result_2 == 4


def test_mock_method_call_raises_configured_exception():
    obj = mock(A)
    every(obj.method).raises(Error())

    with pytest.raises(Error):
        obj.method(1)


def test_mock_function_call_returns_configured_value():
    func = mock(function)
    every(func).returns(2)

    result = func(1)

    assert result == 2


def test_mock_function_call_raises_exception_when_call_is_not_configured():
    func = mock(function)

    with pytest.raises(CallNotConfiguredException):
        func(1)


def test_mock_function_call_raises_exception_when_called_with_non_matching_arguments():
    func = mock(function)
    every(func).with_args(1).returns(2)

    with pytest.raises(CallNotConfiguredException):
        func(2)


def test_mock_function_call_returns_configured_value_when_called_with_matching_arguments():
    func = mock(function)
    every(func).with_args(1).returns(2)

    result = func(1)

    assert result == 2


def test_mock_function_call_returns_configured_value_when_called_with_matching_arguments_and_multiple_configurations():
    func = mock(function)
    every(func).with_args(1).returns(2)
    every(func).with_args(3).returns(4)

    result_1 = func(1)
    result_2 = func(3)

    assert result_1 == 2
    assert result_2 == 4


def test_every_should_raises_exception_when_called_with_non_mock_object():
    with pytest.raises(TypeError):
        every(1)


def test_mock_function_call_returns_multiple_values():
    func = mock(function)
    every(func).returns_many([1, 2])

    result_1 = func(1)
    result_2 = func(1)

    assert result_1 == 1
    assert result_2 == 2


def test_mock_function_call_returns_last_value_when_called_more_times():
    func = mock(function)
    every(func).returns_many([1, 2])
    func(1)
    func(1)

    result = func()

    assert result == 2
