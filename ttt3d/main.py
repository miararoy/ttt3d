from ttt3d.player_human import PlayerHuman
from ttt3d.tiktactoe3d import TikTacToe3d

if __name__ == '__main__':
    player_x = PlayerHuman()
    player_o = PlayerHuman()
    game = TikTacToe3d()
    game.start_game(player_x=player_x, player_o=player_o)