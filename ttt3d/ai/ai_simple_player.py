import pickle
from copy import deepcopy
from typing import Optional, List, Tuple, Iterable
import random

from ttt3d.tiktactoe3d import TikTacToe3d, GameResult, PlayerBase, PlayerHuman

cache = {}
"""
unimplemented optimizations:
# check immediate win
# consider symmetry (mirroring+rotations) enough to check 1st move for (0,0),(1,0),(1,1)
"""

Prob = Tuple[int, int, int]  # Prob = namedtuple('Probe', ['win', 'tie', 'loose'])


def flip_prob(opponent_prob: Prob) -> Prob:
    if opponent_prob is None:
        return None
    try:
        return (opponent_prob[2], opponent_prob[1], opponent_prob[0])
    except AttributeError:
        pass


def choose_move(prob_map_yx: List[Optional[Prob]]) -> int:
    best = -10
    best_idx = None
    for idx, prob in enumerate(prob_map_yx):
        if prob is not None:
            prob_diff = prob[0] - prob[2]
            if prob_diff > best:
                best = prob_diff
                best_idx = idx
    return best_idx


def player_recursion(game: TikTacToe3d, depth=0) -> Optional[Prob]:
    state_hash = game.get_board_tuple()
    cached_result = cache.get(state_hash, None)
    # if depth > 6:
    #     return None
    if cached_result is not None:
        return cached_result[1]

    prob_map_yx = [None] * 9
    for yi in range(3):
        for xi in range(3):
            if depth < 3:
                print('>' * depth, f'(y{yi},x{xi})')
            temp_game = deepcopy(game)
            result = temp_game.place(xy=(xi, yi))
            if result == GameResult.NA:
                try:
                    prob_map_yx[3 * yi + xi] = flip_prob(player_recursion(temp_game, depth + 1))
                except ValueError:
                    continue
            elif result == GameResult.TIE:
                prob_map_yx[3 * yi + xi] = (0, 1, 0)  # Prob(tie=1, win=0, loose=0)
            elif result.name == game.turn.name:
                # win now
                win_prob = (1, 0, 0)  # Prob(tie=0, win=1, loose=0)
                cache[state_hash] = (3 * yi + xi, win_prob)
                return win_prob
            else:
                raise EnvironmentError('loose on my turn should not happen')
        best_idx = choose_move(prob_map_yx=prob_map_yx)
        if best_idx is not None:
            cache[state_hash] = (best_idx, prob_map_yx[best_idx])
        else:
            cache[state_hash] = None


def save_obj(obj, name):
    path = 'obj/' + name + '.pkl'
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    print('Stored cache')



def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
    print('Loaded cache')


class PlayerAI(PlayerBase):
    def __init__(self):
        self.cache = load_obj('deterministic_cache')

    def _random_move(self) -> Tuple[int,int]:
        return random.choice([0,1,2]), random.choice([0,1,2])

    def play_turn(self, game_state: Iterable[int]) -> Tuple[int, int]:
        try:
            xy, prob = self.cache.get(game_state)
        except KeyError:
            print('AI player encountered unknown state, improvising')
            return self._random_move()
        except TypeError:
            print('AI player encountered unsolved state, improvising')
            return self._random_move()
        (x,y) = xy//3,xy%3
        print(f'AI player ({self.symbol}) played (x{x},y{y}), w/t/l = {prob}')
        return xy%3,xy//3

def test_ai_vs_human():
    player_o = PlayerHuman()
    player_x = PlayerAI()
    game = TikTacToe3d()
    result = game.start_game(player_x=player_x, player_o=player_o)
    print(f'Game finished: {result}')


def solve_game_to_cache():
    game = TikTacToe3d()
    player_recursion(game)
    save_obj(cache, 'deterministic_cache')


if __name__ == "__main__":
    """To learn game:"""
    solve_game_to_cache()
    """To play game:"""
    # test_ai_vs_human()