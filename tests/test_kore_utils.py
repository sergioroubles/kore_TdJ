import pytest
from core.kore_utils import *

@pytest.mark.parametrize(
    "path_in, path_expected",
    [
        ("NSWE", "SNEW"),
        ("N6S2W6E8", "S6N2E6W8"),
        ("N", "S"),
        ("S", "N"),
        ("W", "E"),
        ("E", "W"),
        ("S1", "N1"),
     ],
)
def test_get_opposite_way(path_in, path_expected):
    assert get_opposite_way(path_in) == path_expected

