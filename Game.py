from show import *


def playwhite(board, plateau, player_white, player_black, surf):
    erase_bas(surf)
    show_interface(board, plateau, player_white, player_black)
    display.flip()
    message_bas(surf, "White player must play")
    piece = select_interface()
    if board.get(piece[0], piece[1]) != Vide:
        if board.get(piece[0], piece[1]).color == Color.WHITE:
            play(board, plateau, piece,  player_white, player_black)
            if board.old_move[0] == board.old_move[1]:
                return playwhite(board, plateau, player_white, player_black, surf)
            else:
                show_interface(board, plateau, player_white, player_black)
                erase_bas(surf)
                display.flip()
        else:
            print("white must play")
            return playwhite(board, plateau, player_white, player_black, surf)
    else:
        return playwhite(board, plateau, player_white, player_black, surf)


def playblack(board, plateau, player_white, player_black, surf):
    erase_bas(surf)
    show_interface(board, plateau,  player_white, player_black)
    display.flip()
    message_bas(surf, "Black player must play")
    piece = select_interface()
    if board.get(piece[0], piece[1]) != Vide:
        if board.get(piece[0], piece[1]).color == Color.BLACK:
            play(board, plateau, piece,  player_white, player_black)
            if board.old_move[0] == board.old_move[1]:
                return playblack(board, plateau, player_white, player_black, surf)
            else:
                show_interface(board, plateau, player_white, player_black)
                erase_bas(surf)
                display.flip()
        else:
            return playblack(board, plateau, player_white, player_black, surf)
    else:
        return playblack(board, plateau, player_white, player_black, surf)


def play(board, plateau, piece, player_white, player_black):
    if type(board.get(piece[0], piece[1])) == King:
        return playking(board, plateau, piece, player_white, player_black)
    elif type(board.get(piece[0], piece[1])) == Pawn:
        return playpawn(board, plateau, piece, player_white, player_black)
    else:
        return playother(board, plateau, piece, player_white, player_black)


def select_interface():
    while True:
        ev = event.get()
        for e in ev:
            if e.type == MOUSEBUTTONUP:
                pos = mouse.get_pos()
                x = int((pos[0]-L)//c)
                y = int((pos[1]-L)//c)
                return [x, y]


def playother(board, plateau, piece,  player_white, player_black):
    piece_possible = board.move_possible_echec(piece[0], piece[1], player_white, player_black)
    show_move_possible(board, plateau, piece_possible)
    display.flip()
    new_piece = select_interface()
    old_destination = board.choice_case(piece, new_piece, piece_possible, player_white, player_black)
    if type(board.get(new_piece[0], new_piece[1])) == Rook and (piece[0], piece[1]) == (7, 7):
        player_white.rook_little_castling = True
    if type(board.get(new_piece[0], new_piece[1])) == Rook and (piece[0], piece[1]) == (0, 7):
        player_white.rook_large_castling = True
    if type(board.get(new_piece[0], new_piece[1])) == Rook and (piece[0], piece[1]) == (7, 0):
        player_black.rook_little_castling = True
    if type(board.get(new_piece[0], new_piece[1])) == Rook and (piece[0], piece[1]) == (0, 0):
        player_black.rook_large_castling = True
    display.flip()
    old_origin = piece
    board.old_move = [old_origin, old_destination]


def playpawn(board, plateau, piece, player_white, player_black):
    piece_possible = board.move_possible_echec(piece[0], piece[1], player_white, player_black)
    show_move_possible(board, plateau, piece_possible)
    display.flip()
    new_piece = select_interface()
    pawn = board.get(piece[0], piece[1])
    pawn_passing = pawn.move_possible_passing(piece[0], piece[1], board)[1]
    if new_piece == pawn_passing:  # If we do the pawn passing
        old_destination = board.choice_case(piece, new_piece, piece_possible, player_white, player_black)
        board.board[board.old_move[1][1]][board.old_move[1][0]] = Vide
    else:
        old_destination = board.choice_case(piece, new_piece, piece_possible, player_white, player_black)
    old_origin = piece
    board.old_move = [old_origin, old_destination]
    display.flip()


def playking(board, plateau, piece, player_white, player_black):
    piece_possible = board.move_possible_echec(piece[0], piece[1], player_white, player_black)
    # We will remove the possibility of a castling if the rook in question have already moved
    if [6, 7] in piece_possible and player_white.rook_little_castling:
        piece_possible.remove([6, 7])
    if [2, 7] in piece_possible and player_white.rook_large_castling:
        piece_possible.remove([2, 7])
    if [6, 0] in piece_possible and player_black.rook_little_castling:
        piece_possible.remove([6, 0])
    if [2, 0] in piece_possible and player_black.rook_large_castling:
        piece_possible.remove([2, 0])
    show_move_possible(board, plateau, piece_possible)
    display.flip()
    new_piece = select_interface()
    if board.get(piece[0], piece[1]).color == Color.WHITE:  # If the King have moved and is white
        board.white_king_move = True
        if (new_piece[0], new_piece[1]) == (6, 7) and [6, 7] in piece_possible:
            print(0)
            board.little_castling(board.get(piece[0], piece[1]).color)
            old_destination = [new_piece[0], new_piece[1]]
            return 0
        if (new_piece[0], new_piece[1]) == (2, 7) and [2, 7] in piece_possible:
            board.large_castling(board.get(piece[0], piece[1]).color)
            old_destination = [new_piece[0], new_piece[1]]
        else:
            old_destination = board.choice_case(piece, new_piece, piece_possible, player_white, player_black)
        old_origin = piece
        board.old_move = [old_origin, old_destination]
        return 0
    elif board.get(piece[0], piece[1]).color == Color.BLACK:  # If the King have moved and is black
        player_black.king_move = True
        if (new_piece[0], new_piece[1]) == (6, 0) and [6, 0] in piece_possible:
            board.little_castling(board.get(piece[0], piece[1]).color)
            old_destination = [new_piece[0], new_piece[1]]
            return 0
        elif (new_piece[0], new_piece[1]) == (2, 0) and [2, 0] in piece_possible:
            board.large_castling(board.get(piece[0], piece[1]).color)
            old_destination = [new_piece[0], new_piece[1]]
        else:
            old_destination = board.choice_case(piece, new_piece, piece_possible, player_white, player_black)
        old_origin = piece
        board.old_move = [old_origin, old_destination]
        return 0


def endgame(board, surf, color, player_white, player_black):
    if board.check(color, player_white, player_black, surf):
        if color == Color.BLACK:
            message(surf, 'Checkmate!', H/4, H/4)
            message(surf, 'White player wins!', H/4, H/2 + H/4)
        else:
            message(surf, 'Checkmate!', H/4, H/4)
            message(surf, 'Black player wins!', H/4, H/2 + H/4)
        display.flip()
        return True
    else:
        return False
