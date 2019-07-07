from mimid.matchers.value import gt, lt, eq, any


def test_any():
    assert any()(1)


def test_gt():
    assert gt(0)(1)
    assert not gt(0)(-1)


def test_lt():
    assert lt(0)(-1)
    assert not lt(0)(1)


def test_eq():
    assert eq(0)(0)
    assert not eq(0)(1)
