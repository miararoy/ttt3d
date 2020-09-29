from enum import IntEnum


class Symbol(IntEnum):
    E = 0
    O = 1
    X = 2

    def __repr__(self):
        return self.name


class GameResult(IntEnum):
    NA = 0
    O = 1
    X = 2
    TIE = 3

    def __repr__(self):
        return self.name
