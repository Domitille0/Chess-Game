from Board import *
from Player import *


def show_piece(board, x, y, surf):
    pawn = board.get(x, y)
    if pawn != Vide:
        img = pawn.image
        transform.scale(img, (c, c))
        surf.blit(img, (x * c+L, y * c+L))
        return img


def show_move_possible(board, surf, move_possible):
    for x in move_possible:
        draw.rect(surf, (200, 200, 0), Rect(c * x[0]+L, c * x[1]+L, c, c))
        show_piece(board, x[0], x[1], surf)


def show_interface(board, surf, player_white, player_black):
    rect = (2*c-10, 2*c-10, H+20, H+20)
    draw.rect(surf, (0, 0, 0), rect)
    # show the board
    for i in range(8):
        for j in range(8):
            if (i % 2) == 0 and j % 2 == 0:
                draw.rect(surf, "Brown", Rect(c * i+L, c * j+L, c, c))
                show_piece(board, i, j, surf)
            elif (i % 2) == 1 and j % 2 == 1:
                draw.rect(surf, "Brown", Rect(c * i+L, c * j+L, c, c))
                show_piece(board, i, j, surf)
            else:
                draw.rect(surf, "White", Rect(c * i+L, c * j+L, c, c))
                show_piece(board, i, j, surf)
    # show the piece eaten
    for i in range(len(player_white.eat)):
        piece = player_white.eat[i]
        img = piece.image
        transform.scale(img, (c/2, c/2))
        if i <= 7:
            surf.blit(img, (0, c*(i+2)))
        else:
            surf.blit(img, (c, c * (i - 6)))
    for i in range(len(player_black.eat)):
        piece = player_black.eat[i]
        img = piece.image
        transform.scale(img, (c/2, c/2))
        if i <= 7:
            surf.blit(img, (H+200-L+c, c*(i+2)))
        else:
            surf.blit(img, (H + 200 - L, c * (i - 6)))

# show some message
def message(surf, msg, x, y):
    font.init()
    myfont = font.SysFont('Comic Sans MS', 50)
    text = myfont.render(msg, True, (255, 0, 0))
    surf.blit(text, (x, y))


def message_haut(surf, msg):
    font.init()
    myfont2 = font.SysFont('Comic Sans MS', 50)
    text = myfont2.render(msg, True, (255, 0, 0))
    surf.blit(text, (H/2 + 25, 25))
    display.flip()


def message_bas(surf, msg):
    font.init()
    myfont = font.SysFont('Comic Sans MS', 25)
    text = myfont.render(msg, True, (0, 255, 0))
    surf.blit(text, (160, H + 125))
    display.flip()


def erase_bas(surf):
    erase = Rect(0, H + 120, H + 200, H + 200)
    draw.rect(surf, (255, 255, 255), erase)
    display.flip()


def erase_haut(surf):
    erase = Rect(0, 0, H + 200, 200)
    draw.rect(surf, (255, 255, 255), erase)
    display.flip()
