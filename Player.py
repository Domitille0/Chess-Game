from Pieces import *
from show import *


class Player:
    def __init__(self):
        self.eat = []
        self.king_move = False
        self.rook_little_castling = False
        self.rook_large_castling = False

    def choose_new_piece(self, x, y, board, surf):
        font.init()
        myfont = font.SysFont('Comic Sans MS', 25)
        text = myfont.render('Choose your new piece', True, (0, 255, 0))
        surf.blit(text, (175, H + 120))
        for i in range(4):
            pion = self.list_of_pieces[i]
            img = pion.image
            transform.scale(img, (c / 2, c / 2))
            surf.blit(img, (c*(i + 4), H+100+c))
        display.flip()
        piece_chosen = self.select_new_piece()
        piece = self.list_of_pieces[piece_chosen]
        board.set(x, y, piece)
        erase = Rect(0, H+100, H+200, H+200)
        draw.rect(surf, (255, 255, 255), erase)
        display.flip()

    def select_new_piece(self):
        while True:
            ev = event.get()
            for e in ev:
                if e.type == MOUSEBUTTONUP:
                    pos = mouse.get_pos()
                    x = int(pos[0])
                    for i in range(4):
                        if c * (i + 5) > x > c * (i + 4):
                            return i


class Player_White(Player):
    def __init__(self):
        super().__init__()
        self.list_of_pieces = [Rook(Color.WHITE), Knight(Color.WHITE), Bishop(Color.WHITE), Queen(Color.WHITE)]

    def new_piece(self, board, surf):
        #if there is a promotion for the white player
        if type(board.get(board.old_move[1][0], board.old_move[1][1])) == Pawn and board.old_move[1][1] == 0 and board.get(board.old_move[1][0], board.old_move[1][1]).color == Color.WHITE:
            self.choose_new_piece(board.old_move[1][0], board.old_move[1][1], board, surf)


class Player_Black(Player):
    def __init__(self):
        super().__init__()
        self.list_of_pieces = [Rook(Color.BLACK), Knight(Color.BLACK), Bishop(Color.BLACK), Queen(Color.BLACK)]

    def new_piece(self, board, surf):
        #if there is a promotion for the black player
        if type(board.get(board.old_move[1][0], board.old_move[1][1])) == Pawn and board.old_move[1][1] == 7 and board.get(board.old_move[1][0], board.old_move[1][1]).color == Color.BLACK:
            self.choose_new_piece(board.old_move[1][0], board.old_move[1][1], board, surf)