"""Tests the general utilities contained in the `pymerkle.utils` module
"""
import pytest
import itertools
from pymerkle import utils


# ------------------------------------ setup -----------------------------

logarithms = []
nums = []
mixed_powers = []
for p in tuple(range(0, 11)):                                # 0 <= p <= 10
    _set = list(range(p))                                    # [0, 1, ... p-1]
    for k in range(p + 1):                                   # 0 <= k <= p
        for combination in itertools.combinations(_set, k):
            combination = list(combination)

            # [i_1, ..., i_k, p], i_1 < ... < i_k < p
            combination.append(p)
            mixed_powers.append(combination)

            # 2 ^ i_1 + ... + 2 ^ i_k + 2 ^ p, i_1 < ... < i_k < p,   0 <= p <= 10
            nums.append(sum((map(lambda x: 2**x, combination))))

            logarithms.append(p)


# ------------------------------------ log_2 -----------------------------

def test_log_2_exception():
    """Tests that log_2 raises ValueError for negative arguments
    """
    with pytest.raises(ValueError):
        utils.log_2(-1)


def test_log_2_zero_convention():
    """Tests that log_2 evaluates to 0 for the zero argument
    """
    assert utils.log_2(0) == 0


@pytest.mark.parametrize(
    "num, expected", [
        (nums[i], logarithms[i]) for i in range(
            len(logarithms))])
def test_log_2(num, expected):
    """Tests log_2 evaluations for all possible combination of powers from 0 to 10
    """
    assert utils.log_2(num) == expected


# ---------------------------------- decompose ---------------------------

def test_decompose_zero_convention():
    """Tests that decompose returns the nonsensical empty tuple for arguments
    equal to zero
    """
    assert utils.decompose(0) == ()


def test_decompose_negative_convention():
    """Tests that decompose returns the nonsensical empty tuple for arguments
    smaller than zero
    """
    assert utils.decompose(-1) == ()


def reverseTupleFromList(_list):
    """Helper function for the next test session.
    Returns tuple from list in reverse order
    """
    _tuple = ()
    for elem in reversed(_list):
        _tuple += (elem, )
    return _tuple


@pytest.mark.parametrize(
    "num, powers", [
        (nums[i], mixed_powers[i]) for i in range(
            len(nums))])
def test_decompose(num, powers):
    """Tests decompose for all possible combination of powers from 0 to 10
    """
    assert utils.decompose(num) == reverseTupleFromList(powers)