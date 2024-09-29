from enum import Enum

#DIMENSIONES EN PANTALLA
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200

CELL_FULLSIZE = SCREEN_HEIGHT/4
CELL_PADDING = 5
CELL_PADDED_SIZE = CELL_FULLSIZE - CELL_PADDING*2
CELL_BORDER_PADDING = 2
CELL_BORDER_PADDED_SIZE = CELL_FULLSIZE - CELL_BORDER_PADDING*2

#COLORES
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (50,160,220)
RED = (240,85,115)
GREY = (212,212,212)

#PUNTOS POR FICHA
def PUNTOS(value):
    if value == 3:
        return 3
    elif value == 6:
        return 9
    elif value == 12:
        return 27
    elif value == 24:
        return 81
    elif value == 48:
        return 243
    elif value == 96:
        return 729
    elif value == 192:
        return 2187
    elif value == 384:
        return 6561
    elif value == 768:
        return 19683

#MOVIMIENTOS
class Movimiento(Enum):
    IZQUIERDA = 0
    DERECHA = 1
    ARRIBA = 2
    ABAJO = 3