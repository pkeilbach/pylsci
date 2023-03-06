"""tests for pylsci module
"""

import pytest

from pylsci import Lsci  # type: ignore


@pytest.mark.parametrize(
    "std, mean, contrast", [(1, 1, 1), (0.0, 1.0, 0), (0.5, 0.25, 2)]
)
def test_lsci_contrast(std, mean, contrast):
    """
    test contrast calculation
    """
    assert Lsci.contrast(std, mean) == contrast
