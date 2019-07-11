from mimid.common import CallArguments
from mimid.matchers.call import SpecificCallArgumentsMatcher
from mimid.matchers.value import eq


def func_without_params():
    pass


def func_with_one_param(param):
    pass


def test_match_with_empty_args_kwargs_and_matching_matcher():
    call_args = CallArguments(args=(), kwargs={})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_without_params, args=(), kwargs={})

    assert call_args_matcher.match(call_args)


def test_match_with_args_and_matching_matcher():
    call_args = CallArguments(args=(1,), kwargs={})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(eq(1),), kwargs={})

    assert call_args_matcher.match(call_args)


def test_match_with_args_and_not_matching_matcher():
    call_args = CallArguments(args=(1,), kwargs={})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(eq(2),), kwargs={})

    assert not call_args_matcher.match(call_args)


def test_match_with_args_and_extra_matcher():
    call_args = CallArguments(args=(), kwargs={})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(eq(1),), kwargs={})

    assert not call_args_matcher.match(call_args)


def test_match_with_kwargs_and_matching_matcher():
    call_args = CallArguments(args=(), kwargs={"param": 1})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(), kwargs={"param": eq(1)})

    assert call_args_matcher.match(call_args)


def test_match_with_kwargs_and_not_matching_matcher():
    call_args = CallArguments(args=(), kwargs={"param": 1})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(), kwargs={"param": eq(2)})

    assert not call_args_matcher.match(call_args)


def test_match_with_kwargs_and_extra_matcher():
    call_args = CallArguments(args=(), kwargs={})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(), kwargs={"param": eq(1)})

    assert not call_args_matcher.match(call_args)


def test_match_with_matching_args_call_and_kwargs_configuration():
    call_args = CallArguments(args=(1,), kwargs={})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(), kwargs={"param": eq(1)})

    assert call_args_matcher.match(call_args)


def test_match_with_matching_kwargs_call_and_args_configuration():
    call_args = CallArguments(args=(), kwargs={"param": 1})
    call_args_matcher = SpecificCallArgumentsMatcher(target=func_with_one_param, args=(eq(1),), kwargs={})

    assert call_args_matcher.match(call_args)
