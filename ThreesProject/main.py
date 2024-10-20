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
seed_array = [1,1,2,0,1,1,2,0,0,0,1,0,0,0,0,0,10340203,45849032]
board = bd.Board(seed_array)
#board = bd.Board()

# Variable para capturar el número de nodos a explorar que será introducido por el usuario
input_text = ""
capturando_input = False
modo = 0

def draw_menu(modo=modo):
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

    # Mostrar el campo de entrada si está capturando el input
    if capturando_input:
        seleccionado = ""
        if modo == 2: seleccionado = "busqueda en amplitud"
        elif modo == 3: seleccionado = "busqueda en profundidad"
        elif modo == 4: seleccionado = "A*"
        elif modo == 5: seleccionado = "IDA*"
        font_input = pygame.font.SysFont(None, 40)
        input_prompt = font_input.render("Has seleccionado " + seleccionado +" , ingrese el número de nodos y presione Enter:", True, const.BLACK)
        input_rect = input_prompt.get_rect(center=(600, 665))
        screen.blit(input_prompt, input_rect)

        # Mostramos el texto que el usuario ha ingresado
        user_input = font_input.render(input_text, True, const.BLACK)
        input_text_rect = user_input.get_rect(center=(600, 715))
        screen.blit(user_input, input_text_rect)

def draw_screen():
    screen.fill(const.WHITE)
    font = pygame.font.SysFont(None, 50)

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
                text_rect = text.get_rect(center=(j * const.CELL_FULLSIZE + const.CELL_FULLSIZE / 2, i * const.CELL_FULLSIZE + const.CELL_FULLSIZE / 2))
                screen.blit(text, text_rect)

    text = font.render("Siguiente Ficha:", True, const.BLACK)
    text_rect = text.get_rect(center=(1000, 325))
    screen.blit(text, text_rect)
    value = board.siguienteFicha
    color = const.GREY
    if value == 1:
        color = const.BLUE
    elif value == 2:
        color = const.RED
    pygame.draw.rect(screen, color, (950, 350, 100, 100), 0, 10)

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

# Bucle principal
running = True
partidaPerdida = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()

            # Si estamos capturando input del usuario
            if capturando_input:
                if event.key == pygame.K_RETURN:
                    # Cuando el usuario presiona Enter, convierte el texto a entero
                    if input_text.isdigit():
                        num_nodos = int(input_text)
                        capturando_input = False
                        input_text = ""
                        # Llamamos a la IA seleccionada con el número de nodos a expandir introducido
                        inteligenciaArtificial = ai.Ai(board)
                        if modo == 2:
                            inteligenciaArtificial.BFS(num_nodos)
                        elif modo == 3:
                            inteligenciaArtificial.DFS(num_nodos)
                        elif modo == 4:
                            inteligenciaArtificial = ai.Ai(board,funcion_heuristica=ai.FuncionHeuristica_distanciaDeUnionPoderosa, funcion_coste=ai.FuncionCoste_distanciaDeUnionPoderosa)
                            inteligenciaArtificial.AStar(num_nodos)
                        elif modo == 5:
                            inteligenciaArtificial = ai.Ai(board,funcion_heuristica=ai.FuncionHeuristica_distanciaDeUnionPoderosa, funcion_coste=ai.FuncionCoste_distanciaDeUnionPoderosa)
                            inteligenciaArtificial.IDAStar(num_nodos)
                        path = inteligenciaArtificial.encontrar_path_interfaz(inteligenciaArtificial.nodo_ganador)
                        for movimiento in path:
                            board.moverTablero(movimiento)
                            draw_screen()
                            pygame.display.update()
                            time.sleep(1)
                        # Esperamos 3 segundos por movimiento
                        time.sleep(3)
                        puntuacion = str(bd.Board.calcularPuntuacion(board))
                        draw_screen_end(puntuacion)
                        pygame.display.update()
                        time.sleep(5)
                        partidaPerdida = True
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    # Elimina el último carácter si se presiona la tecla de retroceso
                    input_text = input_text[:-1]
                else:
                    # Añade el número que se haya presionado (si es un dígito)
                    if event.unicode.isdigit():
                        input_text += event.unicode

            # Manejamos los eventos para el modo menú
            elif modo == 0:
                if event.key == pygame.K_2:
                    # Si elige un algoritmo de IA, activamos el input de nodos a explorar
                    capturando_input = True
                    modo = 2
                elif event.key == pygame.K_3:
                    capturando_input = True
                    modo = 3
                elif event.key == pygame.K_4:
                    capturando_input = True
                    modo = 4
                elif event.key == pygame.K_5:
                    capturando_input = True
                    modo = 5

    # Dibujar el menú o la pantalla de juego
    if modo in [0,2,3,4,5]:
        draw_menu(modo)
    elif modo == 1:
        if bd.Board.partidaPerdida(board):
            puntuacion = str(bd.Board.calcularPuntuacion(board))
            draw_screen_end(puntuacion)
            partidaPerdida = True
        else:
            draw_screen()

    pygame.display.update()
