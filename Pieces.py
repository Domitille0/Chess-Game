import enum

from pygame import *

H = 400
c = int(H/8)
L = 2*c
image_size = (c, c)
base = 'C:/Users/rayan/PycharmProjects/TDLOG/images/'


class Color(enum.Enum):
    BLACK = "Black"
    WHITE = "White"

    def __str__(self):
        return self._value_


class Pieces:
    def __init__(self, color):
        self.color = color

    def other_color(self):
        other_color = Color.BLACK
        if self.color == Color.BLACK:
            other_color = Color.WHITE
        return other_color


class King(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "♔"
        if self.color == Color.BLACK:
            self.image = transform.scale(image.load(base+"KingB.png"), image_size)
        else:
            self.image = transform.scale(image.load(base+"KingW.png"), image_size)
        transform.scale(self.image, image_size)

    def move_possible(self, x, y, board, player_white, player_black):
        # Classic move for the king
        position_possible = [[x-1, y+1], [x-1, y-1], [x-1, y], [x, y-1], [x+1, y+1], [x+1, y], [x+1, y-1], [x, y+1]]
        position_possible_final = []
        for elem in position_possible:
            if not board.out_of_range(elem[0], elem[1]):
                if board.is_empty(elem[0], elem[1]) or board.get_color(elem[0], elem[1]) != self.color:
                    position_possible_final.append(elem)
        # Then we are about to see if a castling is possible
        # As we are in the class King, we will not check if the rook have already moved
        if self.color == Color.WHITE:
            if not player_white.king_move:
                # King must be in his spot
                if type(board.get(4, 7)) == King:
                    # Same for the rook
                    if type(board.get(7, 7)) == Rook:
                        # Then, nothing between them
                        if board.is_empty(5, 7) and board.is_empty(6, 7):
                            position_possible_final.append([6, 7])
                    if type(board.get(0, 7)) == Rook:
                        if board.is_empty(1, 7) and board.is_empty(2, 7) and board.is_empty(3, 7):
                            position_possible_final.append([2, 7])
        if self.color == Color.BLACK:
            if not player_black.king_move:
                if type(board.get(4, 0)) == King:
                    if type(board.get(7, 0)) == Rook:
                        if board.is_empty(5, 0) and board.is_empty(6, 0):
                            position_possible_final.append([6, 0])
                    if type(board.get(0, 0)) == Rook:
                        if board.is_empty(1, 0) and board.is_empty(2, 0) and board.is_empty(3, 0):
                            position_possible_final.append([2, 0])
        return position_possible_final


class Queen(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "♕"
        if self.color == Color.BLACK:
            self.image = transform.scale(image.load(base+"QueenB.png"), image_size)
        else:
            self.image = transform.scale(image.load(base+"QueenW.png"), image_size)

    def move_possible(self, x, y, board, player_white, player_black):
        position_possible = []
        movement = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, 1], [1, -1], [-1, -1], [1, 1]]
        for elem in movement:
            x_move = x+elem[0]
            y_move = y+elem[1]
            if not board.out_of_range(x_move, y_move) and not board.is_empty(x_move, y_move) and \
                    board.get(x_move, y_move).color != self.color:
                position_possible.append([x_move, y_move])
            while not board.out_of_range(x_move, y_move) and board.is_empty(x_move, y_move):
                position_possible.append([x_move, y_move])
                x_move += elem[0]
                y_move += elem[1]
                if not board.out_of_range(x_move, y_move) and not board.is_empty(x_move, y_move):
                    if board.get(x_move, y_move).color != self.color:
                        position_possible.append([x_move, y_move])
        return position_possible


class Knight(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "♘"
        if self.color == Color.BLACK:
            self.image = transform.scale(image.load(base+"KnightB.png"), image_size)
        else:
            self.image = transform.scale(image.load(base+"KnightW.png"), image_size)

    def move_possible(self, x, y, board, player_white, player_black):
        position_possible = [[x-1, y-2], [x-2, y-1], [x-1, y+2], [x-2, y+1], [x+1, y-2], [x+2, y-1], [x+1, y+2],
                             [x+2, y+1]]
        position_possible_final = []
        for elem in position_possible:
            if not board.out_of_range(elem[0], elem[1]):
                if board.is_empty(elem[0], elem[1]) or board.get_color(elem[0], elem[1]) != self.color:
                    position_possible_final.append(elem)
        return position_possible_final


class Bishop(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "♗"
        if self.color == Color.BLACK:
            self.image = transform.scale(image.load(base+"BishopB.png"), image_size)
        else:
            self.image = transform.scale(image.load(base+"BishopW.png"), image_size)

    def move_possible(self, x, y, board, player_white, player_black):
        position_possible = []
        movement = [[-1, 1], [1, -1], [-1, -1], [1, 1]]
        for elem in movement:
            x_move = x + elem[0]
            y_move = y + elem[1]
            if not board.out_of_range(x_move, y_move) and not board.is_empty(x_move, y_move) and \
                    board.get(x_move, y_move).color != self.color:
                position_possible.append([x_move, y_move])
            while not board.out_of_range(x_move, y_move) and board.is_empty(x_move, y_move):
                position_possible.append([x_move, y_move])
                x_move += elem[0]
                y_move += elem[1]
                if not board.out_of_range(x_move, y_move) and not board.is_empty(x_move, y_move):
                    if board.get(x_move, y_move).color != self.color:
                        position_possible.append([x_move, y_move])
        return position_possible


class Rook(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "♖"
        if self.color == Color.BLACK:
            self.image = transform.scale(image.load(base+"RookB.png"), image_size)
        else:
            self.image = transform.scale(image.load(base+"RookW.png"), image_size)

    def move_possible(self, x, y, board, player_white, player_black):
        position_possible = []
        movement = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for elem in movement:
            x_move = x + elem[0]
            y_move = y + elem[1]
            if not board.out_of_range(x_move, y_move) and not board.is_empty(x_move, y_move) and \
                    board.get(x_move, y_move).color != self.color:
                position_possible.append([x_move, y_move])
            while not board.out_of_range(x_move, y_move) and board.is_empty(x_move, y_move):
                position_possible.append([x_move, y_move])
                x_move += elem[0]
                y_move += elem[1]
                if not board.out_of_range(x_move, y_move) and not board.is_empty(x_move, y_move):
                    if board.get(x_move, y_move).color != self.color:
                        position_possible.append([x_move, y_move])
        return position_possible


class Pawn(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "♙"
        if self.color == Color.BLACK:
            self.image = transform.scale(image.load(base+"PawnB.png"), image_size)
        else:
            self.image = transform.scale(image.load(base+"PawnW.png"), image_size)

    def move_possible_pawn(self, x, y, direction, board):
        #possible position without the passing pawn
        position_possible = []
        if not board.out_of_range(x-1, y + direction) and board.get_color(x - 1, y + direction) != self.color and not \
                board.is_empty(x - 1, y + direction):
            position_possible.append([x - 1, y + direction])
        if not board.out_of_range(x+1, y + direction) and board.get_color(x + 1, y + direction) != self.color and not \
                board.is_empty(x + 1, y + direction):
            position_possible.append([x + 1, y + direction])
        if not board.out_of_range(x, y+direction) and board.is_empty(x, y+direction):
            position_possible.append([x, y + direction])
        if not board.out_of_range(x, y+direction) and self.color == Color.BLACK and y == 1 and \
                board.is_empty(x, y+direction+direction) and board.is_empty(x, y+direction):
            position_possible.append([x, y + direction + direction])
        if not board.out_of_range(x, y+direction*2) and self.color == Color.WHITE and y == 6 and \
                board.is_empty(x, y+direction+direction) and board.is_empty(x, y+direction):
            position_possible.append([x, y + direction + direction])
        return position_possible

    def move_possible_passing(self, x, y, board):
        #move possible with the passing pawn
        position_possible = self.move_possible_pawn_color(x, y, board)
        pawn_move = []
        for i in range(8):
            pawn = board.get(i, 3)
            if type(pawn) == Pawn and pawn.color == Color.WHITE:
                if board.old_move:
                    last_origin = board.old_move[0]
                    last_destination = board.old_move[1]
                    if last_destination[1] == y:
                        if type(board.get(last_destination[0], last_destination[1])) == Pawn and \
                                board.get(last_destination[0], last_destination[1]).color == Color.BLACK:
                            if last_origin == [i - 1, 1] and i - 1 >= 0:
                                if last_destination == [i - 1, 3]:
                                    position_possible.append([i - 1, 2])
                                    pawn_move = [i - 1, 2]
                            if last_origin == [i + 1, 1] and i + 1 >= 0:
                                if last_destination == [i + 1, 3]:
                                    position_possible.append([i + 1, 2])
                                    pawn_move = [i + 1, 2]
            pawn2 = board.get(i, 4)
            if type(pawn2) == Pawn and pawn2.color == Color.BLACK:
                last_origin = board.old_move[0]
                last_destination = board.old_move[1]
                if last_destination[1] == y:
                    if type(board.get(last_destination[0], last_destination[1])) == Pawn and \
                            board.get(last_destination[0], last_destination[1]).color == Color.WHITE:
                        if last_origin == [i - 1, 6] and i - 1 >= 0:
                            if last_destination == [i - 1, 4]:
                                position_possible.append([i - 1, 5])
                                pawn_move = [i - 1, 5]
                        if last_origin == [i + 1, 6] and i + 1 >= 0:
                            if last_destination == [i + 1, 4]:
                                position_possible.append([i + 1, 5])
                                pawn_move = [i + 1, 5]
        return [position_possible, pawn_move]

    def move_possible_pawn_color(self, x, y, board):
        position_possible = []
        if self.color == Color.BLACK:
            position_possible = self.move_possible_pawn(x, y, 1, board)
        elif self.color == Color.WHITE:
            position_possible = self.move_possible_pawn(x, y, -1, board)
        return position_possible

    def move_possible(self, x, y, board, player_white, player_black):
        return self.move_possible_passing(x, y, board)[0]


class Vide:
    def __init__(self):
        self.symbol = ""
