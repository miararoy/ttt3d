from typing import Iterable, Tuple

from ttt3d.enums import Symbol


class PlayerBase:
    def __init__(self):
        self._symbol = None

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: Symbol):
        assert symbol.name in ['X', 'O']
        self._symbol = symbol

    def play_turn(self, game_state: Iterable[int]) -> Tuple[int, int]:
        raise NotImplementedError