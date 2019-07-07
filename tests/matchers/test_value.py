import pytest

from mimid import ValueNotCapturedException
from mimid.matchers.value import gt, eq, any, gte, lte, CaptureSlot, capture


def test_any():
    assert any()(1)


def test_eq():
    assert eq(0)(0)
    assert not eq(0)(1)


def test_gt():
    assert gt(0)(1)
    assert not gt(0)(-1)


def test_gte():
    assert gte(0)(0)
    assert gte(0)(1)
    assert not gte(0)(-1)


def test_ltt():
    assert lte(0)(0)
    assert lte(0)(-1)
    assert not lte(0)(1)


def test_capture():
    slot = CaptureSlot()
    value_capture = capture(slot)

    result = value_capture(1)

    assert result
    assert slot.value == 1


def test_capture_slot_raises_exception_when_not_captured():
    slot = CaptureSlot()

    with pytest.raises(ValueNotCapturedException):
        slot.value
