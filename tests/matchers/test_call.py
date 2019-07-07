from mimid.common import CallArguments
from mimid.matchers.call import CallArgumentsMatcher
from mimid.matchers.value import eq


def test_match_with_empty_args_kwargs_and_matching_matcher():
    call_args = CallArguments(args=(), kwargs={})
    call_args_matcher = CallArgumentsMatcher(args=(), kwargs={})

    assert call_args_matcher.match(call_args)


def test_match_with_args_and_matching_matcher():
    call_args = CallArguments(args=(1,), kwargs={})
    call_args_matcher = CallArgumentsMatcher(args=(eq(1),), kwargs={})

    assert call_args_matcher.match(call_args)


def test_match_with_args_and_not_matching_matcher():
    call_args = CallArguments(args=(1,), kwargs={})
    call_args_matcher = CallArgumentsMatcher(args=(eq(2),), kwargs={})

    assert not call_args_matcher.match(call_args)


def test_match_with_args_and_missing_matcher():
    call_args = CallArguments(args=(1,), kwargs={})
    call_args_matcher = CallArgumentsMatcher(args=(), kwargs={})

    assert not call_args_matcher.match(call_args)


def test_match_with_args_and_extra_matcher():
    call_args = CallArguments(args=(), kwargs={})
    call_args_matcher = CallArgumentsMatcher(args=(eq(1),), kwargs={})

    assert not call_args_matcher.match(call_args)


def test_match_with_kwargs_and_matching_matcher():
    call_args = CallArguments(args=(), kwargs={"a": 1})
    call_args_matcher = CallArgumentsMatcher(args=(), kwargs={"a": eq(1)})

    assert call_args_matcher.match(call_args)


def test_match_with_kwargs_and_not_matching_matcher():
    call_args = CallArguments(args=(), kwargs={"a": 1})
    call_args_matcher = CallArgumentsMatcher(args=(), kwargs={"a": eq(2)})

    assert not call_args_matcher.match(call_args)


def test_match_with_kwargs_and_missing_matcher():
    call_args = CallArguments(args=(), kwargs={"a": 1})
    call_args_matcher = CallArgumentsMatcher(args=(), kwargs={})

    assert not call_args_matcher.match(call_args)


def test_match_with_kwargs_and_extra_matcher():
    call_args = CallArguments(args=(), kwargs={})
    call_args_matcher = CallArgumentsMatcher(args=(), kwargs={"a": eq(1)})

    assert not call_args_matcher.match(call_args)
