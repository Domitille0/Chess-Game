
from Board import *
from Game import *
if __name__ == "__main__":
    # initialisation: no check
    check = False
    plateau = display.set_mode((H+200, H+200),)
    plateau.fill((255, 255, 255))
    B = Board()
    player_white = Player_White()
    player_black = Player_Black()
    game = True
    init()
    keep = True
    while keep:
        while game:
            playwhite(B, plateau, player_white, player_black, plateau)
            player_white.new_piece(B, plateau)
            B.check(Color.BLACK, player_white, player_black, plateau)
            end = endgame(B, plateau, Color.BLACK, player_white, player_black)
            if not end:
                playblack(B, plateau, player_white, player_black, plateau)
                player_black.new_piece(B, plateau)
                B.check(Color.WHITE, player_white, player_black, plateau)
                if endgame(B, plateau, Color.WHITE, player_white, player_black):
                    game = False
            else:
                game = False
    quit()
