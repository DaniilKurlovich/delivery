import random
from typing import ClassVar

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    # координаты начинаются не с нуля нужно учитывать при расчете расстояния
    swift_pos: ClassVar[int] = 1
    min_coord: ClassVar[int] = 1
    max_coord: ClassVar[int] = 10

    x: int = Field(title='coord of X axis', ge=min_coord, le=max_coord)
    y: int = Field(title='coord of Y axis', ge=min_coord, le=max_coord)

    @classmethod
    def random(cls):
        return Location(random.randint(cls.min_coord, cls.max_coord),
                        random.randint(cls.min_coord, cls.max_coord))

    def _get_distance_axis(self, x_1, x_2):
        diff_ = abs(x_1 - x_2)
        if diff_ != 0:
            return diff_ + self.swift_pos
        return diff_

    def distance(self, other: "Location") -> int:
        return self._get_distance_axis(self.x, other.x) + self._get_distance_axis(self.y, other.y)
