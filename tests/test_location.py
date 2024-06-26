import dataclasses

import pytest
from pydantic import ValidationError

from core.domain.shared_kernel import Location


@pytest.fixture
def location_random():
    yield Location.random()


def test_mutable_location(location_random):
    with pytest.raises(dataclasses.FrozenInstanceError):
        location_random.x = 4
        location_random.y = 5


@pytest.mark.parametrize("x,y", [
    (Location.min_coord - 1, Location.max_coord),
    (Location.min_coord, Location.max_coord + 1),
    (Location.min_coord - 1, Location.max_coord + 1)
])
def test_not_valid_location_range(x, y):
    with pytest.raises(ValidationError):
        Location(x, y)


@pytest.mark.parametrize("x,y", [
    (1, 2.4),
    (2, "10.04"),
    (5.02, 5.01)
])
def test_not_valid_coordinate_types(x, y):
    with pytest.raises(ValidationError):
        Location(x, y)


@pytest.mark.parametrize("coord_a,coord_b,expected", [
    (Location(2, 6), Location(4, 9), 7),
    (Location(4, 9), Location(4, 9), 0),
    (Location(10, 10), Location(1, 1), 20),
    (Location(10, 10), Location(6, 6), 10),
    (Location(6, 6), Location(1, 1), 12)
])
def test_not_valid_range_computation(coord_a, coord_b, expected):
    assert coord_a.distance(coord_b) == expected
