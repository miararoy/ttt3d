from typing import Iterable, Tuple

from ttt3d import np

from ttt3d.player_base import PlayerBase


class PlayerHuman(PlayerBase):

    def play_turn(self, game_state: Iterable[int]) -> Tuple[int, int]:
        in_str = f'its {self.symbol.name} turn, play: <x y>'
        print(np.array(game_state).reshape((3, 3, 3)))
        xy = tuple(int(x) for x in input(in_str).split()[:2])
        if len(xy) < 2:
            raise ValueError('Bad input. expected: <x> <y>')
        return xy