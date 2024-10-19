import time

import pygame

import ai
import const
import board as bd

# Lanza el proyecto
pygame.init()

# Establece las dimensiones seteadas en const
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

# Iniciamos la clase board y automaticamente genera la matriz del tablero
#board = bd.Board()

# Como se inicia una seed:
# seed_array = [0,0,0,3,0,0,2,0,0,1,0,0,3,0,0,0,10340203,45849032]
# board = bd.Board(seed_array)

seed_array = [1,1,2,0,1,1,2,0,0,0,1,0,0,0,0,0,10340203,45849032]
board = bd.Board(seed_array)

def draw_menu():
    screen.fill(const.WHITE)
    font01 = pygame.font.SysFont(None, 50)
    text01 = font01.render("Jugar como humano (pulsa 1)", True, const.BLACK)
    text_rect01 = text01.get_rect(center=(600, 165))
    text02 = font01.render("Aplicar busqueda en amplitud (pulsa 2)", True, const.BLACK)
    text_rect02 = text02.get_rect(center=(600, 265))
    text03 = font01.render("Aplicar busqueda en profundidad (pulsa 3)", True, const.BLACK)
    text_rect03 = text03.get_rect(center=(600, 365))
    text04 = font01.render("Aplicar algoritmo A* (pulsa 4)", True, const.BLACK)
    text_rect04 = text04.get_rect(center=(600, 465))
    text05 = font01.render("Aplicar algoritmo IDA* (pulsa 5)", True, const.BLACK)
    text_rect05 = text05.get_rect(center=(600, 565))
    screen.blit(text01, text_rect01)
    screen.blit(text02, text_rect02)
    screen.blit(text03, text_rect03)
    screen.blit(text04, text_rect04)
    screen.blit(text05, text_rect05)

def draw_screen():
    screen.fill(const.WHITE)
    font = pygame.font.SysFont(None, 50)
    message_font = pygame.font.SysFont(None, 70, True)

    # Proceso para pintar cada ficha
    for i in range(0, 4):
        for j in range(0, 4):
            value = board.board[i][j]
            color = const.WHITE
            if value == 1:
                color = const.BLUE
            elif value == 2:
                color = const.RED
            elif value > 2:
                color = const.GREY
            # A la hora de dibujar el rectangulo se hace primero la coordenada de
            # la esquina superior izquierda y luego las dimensiones
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
                             , 0, 10)
            if value != 0:
                text = font.render(str(value), True, const.BLACK)
                text_rect = text.get_rect(center=(
                j * const.CELL_FULLSIZE + const.CELL_FULLSIZE / 2, i * const.CELL_FULLSIZE + const.CELL_FULLSIZE / 2))
                screen.blit(text, text_rect)

    # Pintar la siguiente ficha
    text = font.render("Siguiente Ficha:", True, const.BLACK)
    text_rect = text.get_rect(center=(1000, 325))
    screen.blit(text, text_rect)
    value = board.siguienteFicha
    color = const.GREY
    if value == 1:
        color = const.BLUE
    elif value == 2:
        color = const.RED
    pygame.draw.rect(screen, color,
                     (950, 350, 100, 100)
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


# Hacemos el bucle que refresca la ventana
running = True
partidaPerdida = False
modo = 0

while running:
    # Captura los eventos que ocurren en cualquier modo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()

            # Manejamos los eventos para el modo 0 (menú)
            if modo == 0:
                if event.key == pygame.K_1:
                    modo = 1  # Cambiamos a modo 1
                elif event.key == pygame.K_2:
                    modo = 2  # Cambiamos a modo 2

            # Manejamos los eventos para el modo 1 (juego)
            elif modo == 1:
                if not partidaPerdida:
                    if event.key == pygame.K_LEFT:
                        board.moverTablero(const.Movimiento.IZQUIERDA)
                    elif event.key == pygame.K_RIGHT:
                        board.moverTablero(const.Movimiento.DERECHA)
                    elif event.key == pygame.K_UP:
                        board.moverTablero(const.Movimiento.ARRIBA)
                    elif event.key == pygame.K_DOWN:
                        board.moverTablero(const.Movimiento.ABAJO)



    # Dibuja la pantalla del modo correspondiente
    if modo == 0:
        draw_menu()
    elif modo == 1:
        if bd.Board.partidaPerdida(board):
            puntuacion = str(bd.Board.calcularPuntuacion(board))
            draw_screen_end(puntuacion)
            partidaPerdida = True
        else:
            draw_screen()
    elif modo == 2:
        inteligenciaArtificial = ai.Ai(board)
        inteligenciaArtificial.BFS(1000)
        path = inteligenciaArtificial.encontrar_path_interfaz(inteligenciaArtificial.nodo_ganador)
        for movimiento in path:
            board.moverTablero(movimiento)
            draw_screen()
            pygame.display.update()
            time.sleep(1)
        time.sleep(3)
        puntuacion = str(bd.Board.calcularPuntuacion(board))
        draw_screen_end(puntuacion)
        pygame.display.update()
        time.sleep(5)
        partidaPerdida = True
        running = False

    # Actualizamos la pantalla en cada ciclo del while
    pygame.display.update()

