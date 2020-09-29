from enum import IntEnum
from typing import Tuple, Iterable

from ttt3d import np
from ttt3d.enums import Symbol, GameResult
from ttt3d.player_base import PlayerBase


class TikTacToe3d:
    def __init__(self):
        self.board = np.full((3, 3, 3), fill_value=Symbol.E, dtype=Symbol)
        # self.board[:,:,:] = Symbol.E
        self.turn = Symbol.X
        self.result = GameResult.NA

    def plot(self):
        print(self.board)
        pass

    def check_win(self, x: int, y: int, z: int) -> GameResult:
        check_board = self.board == self.turn
        # lines
        if all(check_board[z, y, :]) or \
                all(check_board[:, y, x]) or \
                all(check_board[z, :, x]):
            return GameResult(self.turn)

        # diagonals
        if (x == y and check_board[z, 0, 0] and check_board[z, 1, 1] and check_board[z, 2, 2]) or \
                (x == z and check_board[0, y, 0] and check_board[1, y, 1] and check_board[2, y, 2]) or \
                (y == z and check_board[0, 0, x] and check_board[1, 1, x] and check_board[2, 2, x]):
            return GameResult(self.turn)

        # reversed diagonals:
        if (x + y == 2 and check_board[z, 2, 0] and check_board[z, 1, 1] and check_board[z, 0, 2]) or \
                (x + z == 2 and check_board[2, y, 0] and check_board[1, y, 1] and check_board[0, y, 2]) or \
                (z + y == 2 and check_board[2, 0, x] and check_board[1, 1, x] and check_board[0, 2, x]):
            return GameResult(self.turn)

        # 3D diagonals
        if check_board[1, 1, 1]:
            if (check_board[0, 0, 0] and check_board[2, 2, 2]) or \
                    (check_board[2, 0, 0] and check_board[0, 2, 2]) or \
                    (check_board[0, 2, 0] and check_board[2, 0, 2]) or \
                    (check_board[0, 0, 2] and check_board[0, 2, 2]):
                return GameResult(self.turn)

        if not (self.board == Symbol.E).any():
            return GameResult.TIE
        else:
            return GameResult.NA

    def get_board_tuple(self) -> Iterable[int]:
        board_tuple = tuple(self.board.flatten().astype('uint8'))
        return board_tuple

    def place(self, xy: Tuple[int, int]) -> GameResult:
        x, y = xy
        assert (3 > x >= 0 and 3 > y >= 0)
        placed = False
        z = None
        for zi in range(3):
            if self.board[zi, y, x] == Symbol.E:
                z = zi
                self.board[z, y, x] = self.turn
                placed = True
                break
        if not placed:
            raise ValueError(f'could not place in ({x},{y})')
        result = self.check_win(x=x, y=y, z=z)
        self.result = result

        self.turn = Symbol.O if self.turn == Symbol.X else Symbol.X
        return result

    def publish_results(self):
        if self.result == GameResult.TIE:
            print("TIE")
        if self.result == GameResult.NA:
            print("NO RESULT")
        else:
            print(f"{self.result.name} IS THE WINNER")

    def start_game(self, player_x, player_o) -> GameResult:
        assert (isinstance(player_x, PlayerBase))
        assert (isinstance(player_o, PlayerBase))

        player_o.symbol = Symbol.O
        player_x.symbol = Symbol.X
        while self.result == GameResult.NA:
            player = player_x if self.turn == Symbol.X else player_o
            xy = player.play_turn(self.get_board_tuple())
            try:
                self.place(xy)
            except ValueError:
                continue
            except KeyboardInterrupt:
                self.publish_results()
        self.publish_results()
        return self.result.value
