from show import *
from Pieces import *


class Board:
    def __init__(self):
        self.board = [[Rook(Color.BLACK), Knight(Color.BLACK), Bishop(Color.BLACK), Queen(Color.BLACK), King(Color.BLACK), Bishop(Color.BLACK), Knight(Color.BLACK), Rook(Color.BLACK)],
                     [Pawn(Color.BLACK), Pawn(Color.BLACK), Pawn(Color.BLACK), Pawn(Color.BLACK), Pawn(Color.BLACK), Pawn(Color.BLACK), Pawn(Color.BLACK), Pawn(Color.BLACK)],
                     [Vide, Vide, Vide, Vide, Vide, Vide, Vide, Vide],
                     [Vide, Vide, Vide, Vide, Vide, Vide, Vide, Vide],
                     [Vide, Vide, Vide, Vide, Vide, Vide, Vide, Vide],
                     [Vide, Vide, Vide, Vide, Vide, Vide, Vide, Vide],
                     [Pawn(Color.WHITE), Pawn(Color.WHITE), Pawn(Color.WHITE), Pawn(Color.WHITE), Pawn(Color.WHITE), Pawn(Color.WHITE), Pawn(Color.WHITE), Pawn(Color.WHITE)],
                     [Rook(Color.WHITE), Knight(Color.WHITE), Bishop(Color.WHITE), Queen(Color.WHITE), King(Color.WHITE), Bishop(Color.WHITE), Knight(Color.WHITE), Rook(Color.WHITE)]
                     ]
        self.old_move = []

    def is_empty(self, x, y):
        if self.get(x, y) == Vide:
            return True
        else:
            return False

    def get(self, x, y):
        return self.board[y][x]

    def get_color(self, x, y):
        if self.board[y][x] == Vide:
            return None
        else:
            return self.board[y][x].color

    def set(self, x, y, piece):
        self.board[y][x] = piece

    def out_of_range(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return True
        else:
            return False

    def move_piece_possible(self, x, y, player_white, player_black):
        piece = self.get(x, y)
        position_possible = piece.move_possible(x, y, self, player_white, player_black)
        return position_possible

    def choice_case(self, piece, new_piece, position_possible,  player_white, player_black):
        x = piece[0]
        y = piece[1]
        x_new = new_piece[0]
        y_new = new_piece[1]

        if [x_new, y_new] not in position_possible:
            print("Move not possible with this piece")
            return [x, y]
        elif [x, y] != [x_new, y_new]:
            piece = self.get(x, y)
            if self.get(new_piece[0], new_piece[1]) != Vide:
                if self.get(new_piece[0], new_piece[1]).color == Color.BLACK:
                    player_black.eat.append(self.get(new_piece[0], new_piece[1]))
                else:
                    player_white.eat.append(self.get(new_piece[0], new_piece[1]))
            self.board[y][x] = Vide
            self.board[y_new][x_new] = piece
        return [x_new, y_new]

    def move_possible_echec(self, x, y, player_white, player_black):
        # move possible when we take in account the check possibilities
        move_piece_possible = self.move_piece_possible(x, y, player_white, player_black)
        move_possible_echec = []
        piece = self.board[y][x]
        for elem in move_piece_possible:
            # for all the potential move, we simulate the move and make sure that the move doesn't put the king in danger
            piece_eat = self.board[elem[1]][elem[0]]
            self.board[y][x] = Vide
            self.board[elem[1]][elem[0]] = piece
            if not self.move_possible_eat_king(piece.color, player_white, player_black):
                # if there is no danger, we add the move in the final list
                move_possible_echec.append(elem)
            self.board[y][x] = piece
            self.board[elem[1]][elem[0]] = piece_eat
        return move_possible_echec

    def move_possible(self):
        raise NotImplementedError

    def little_castling(self, color):
        # move the piece in case of castling
        if color == Color.WHITE:
            king = self.board[7][4]
            rook = self.board[7][7]
            self.board[7][6] = king
            self.board[7][5] = rook
            self.board[7][7] = Vide
            self.board[7][4] = Vide
        if color == Color.BLACK:
            king = self.board[0][4]
            rook = self.board[0][7]
            self.board[0][6] = king
            self.board[0][5] = rook
            self.board[0][7] = Vide
            self.board[0][4] = Vide

    def large_castling(self, color):
        if color == Color.WHITE:
            king = self.board[7][4]
            rook = self.board[7][0]
            self.board[7][2] = king
            self.board[7][3] = rook
            self.board[7][0] = Vide
            self.board[7][4] = Vide
        if color == Color.BLACK:
            king = self.board[0][4]
            rook = self.board[0][0]
            self.board[0][2] = king
            self.board[0][3] = rook
            self.board[0][0] = Vide
            self.board[0][4] = Vide

    # Selection of all the possible move of the color_other player
    def all_move_possible(self, color, player_white, player_black):
        move_possible = []
        for i in range(8):
            for j in range(8):
                piece = self.get(i, j)
                if piece != Vide and piece.color != color:  # if the piece has not the same color
                    for elem in (self.move_piece_possible(i, j, player_white, player_black)):
                        move_possible.append([[i, j], elem])  # we add all its move possible
        return move_possible

# Selection of all the move about to eat the king in color
    def move_possible_eat_king(self, color, player_white, player_black):
        all_move_possible_against_king = []
        all_move_possible = self.all_move_possible(color, player_white, player_black)
        # we take all the move possible for the other_color player
        for elem in all_move_possible:
            if not self.is_empty(elem[1][0], elem[1][1]):
                if type(self.get(elem[1][0], elem[1][1])) == King and self.get(elem[1][0], elem[1][1]).color == color:
                    # if one eats the king of color
                    all_move_possible_against_king.append([elem[0], elem[1]])  # we add the move
        return all_move_possible_against_king

    def check(self, color, player_white, player_black, surf):
        # we check there is no check
        king_in_danger = self.move_possible_eat_king(color, player_white, player_black)
        if king_in_danger: # if there is a move that can eat the king
            message_haut(surf, 'Check!')
            return self.check_mate(color, player_white, player_black)
        else:
            erase_haut(surf)
        return False

    def check_mate(self, color, player_white, player_black):
        # we check there is no check mate
        move_possible = []
        # we select all the move possible for the color player
        for i in range(8):
            for j in range(8):
                piece = self.get(i, j)
                if piece != Vide and piece.color == color:  # if the piece has not the same color
                    for elem in (self.move_possible_echec(i, j, player_white, player_black)):
                        move_possible.append([[i, j], elem])
        if not move_possible:  # if there is no moving possibilities
            return True
        return False
