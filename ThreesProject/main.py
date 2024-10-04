import pygame

import const
import board as bd
import ai

#Lanza el proyecto
pygame.init()

#Establece las dimensiones seteadas en const
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

#Iniciamos la clase board y automaticamente genera la matriz del tablero
board = bd.Board()

#Como se inicia una seed:
#seed_array = [0,0,0,3,0,0,2,0,0,1,0,0,3,0,0,0,10340203,45849032]
#board = bd.Board(seed_array)

#seed_array = [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,10340203,45849032]
#board = bd.Board(seed_array)

def draw_screen():
    screen.fill(const.WHITE)
    font = pygame.font.SysFont(None, 50)
    message_font = pygame.font.SysFont(None, 70, True)

    #Proceso para pintar cada ficha
    for i in range(0,4):
        for j in range(0,4):
            value = board.board[i][j]
            color = const.WHITE
            if value == 1:
                color = const.BLUE
            elif value == 2:
                color = const.RED
            elif value > 2:
                color = const.GREY
            #A la hora de dibujar el rectangulo se hace primero la coordenada de
            #la esquina superior izquierda y luego las dimensiones
            if value != 0:
                pygame.draw.rect(screen, const.BLACK,
                                 (j * const.CELL_FULLSIZE + const.CELL_BORDER_PADDING,
                                  i * const.CELL_FULLSIZE + const.CELL_BORDER_PADDING,
                                  const.CELL_BORDER_PADDED_SIZE,
                                  const.CELL_BORDER_PADDED_SIZE)
                                , 15, 10)
            pygame.draw.rect(screen, color,
                             (j * const.CELL_FULLSIZE + const.CELL_PADDING,
                              i * const.CELL_FULLSIZE + const.CELL_PADDING,
                              const.CELL_PADDED_SIZE,
                              const.CELL_PADDED_SIZE)
                             ,0, 10)
            if value != 0:
                text = font.render(str(value),True,const.BLACK)
                text_rect = text.get_rect(center=(j * const.CELL_FULLSIZE + const.CELL_FULLSIZE/2, i * const.CELL_FULLSIZE + const.CELL_FULLSIZE/2))
                screen.blit(text,text_rect)

    #Pintar la siguiente ficha
    text = font.render("Siguiente Ficha:",True,const.BLACK)
    text_rect = text.get_rect(center=(1000, 325))
    screen.blit(text,text_rect)
    value = board.siguienteFicha
    color = const.GREY
    if value == 1:
        color = const.BLUE
    elif value == 2:
        color = const.RED
    pygame.draw.rect(screen, color,
                     (950,350,100,100)
                     , 0, 10)

def draw_screen_end(puntuacion):
    screen.fill(const.WHITE)
    font01 = pygame.font.SysFont(None, 50)
    font02 = pygame.font.SysFont(None, 40)
    text01 = font01.render("Has perdido", True, const.BLACK)
    text02 = font02.render("Puntuación: " + puntuacion, True, const.BLACK)
    text_rect01 = text01.get_rect(center=(600, 365))
    text_rect02 = text02.get_rect(center=(600, 400))
    screen.blit(text01, text_rect01)
    screen.blit(text02, text_rect02)

#Hacemos el bucle que refresca la ventana
running = True
while running:
    #Captura los eventos en la interfaz
    for event in pygame.event.get():
        #QUIT representa un clic a la cruz de cerrar una ventana
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                board.moverTablero(const.Movimiento.IZQUIERDA)
            elif event.key == pygame.K_RIGHT:
                board.moverTablero(const.Movimiento.DERECHA)
            elif event.key == pygame.K_UP:
                board.moverTablero(const.Movimiento.ARRIBA)
            elif event.key == pygame.K_DOWN:
                board.moverTablero(const.Movimiento.ABAJO)
    if bd.Board.partidaPerdida(board):
        puntuacion = str(bd.Board.calcularPuntuacion(board))
        draw_screen_end(puntuacion)
    else:
        draw_screen()
    pygame.display.update()