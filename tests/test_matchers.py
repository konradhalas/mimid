from mimid import gt, lt


def test_gt():
    assert gt(0)(1)
    assert not gt(0)(-1)


def test_lt():
    assert lt(0)(-1)
    assert not lt(0)(1)
