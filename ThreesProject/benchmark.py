import ai
import board as bd

import matplotlib.pyplot as plt

# Iniciamos la clase board y automaticamente genera la matriz del tablero
seed_array = [1,1,2,0,1,1,2,0,0,0,1,0,0,0,0,0,10340203,45849032]
board = bd.Board(seed_array)

# Lo suyo seria cambiar este a 100,1000,5000 y 10000 aunque ya cuando tengamos IDA* bien pq esto tarda en ejecutar...
X = [100,1000,5000,10000]
#Algoritmos Implementados
algoritmos=['BFS','DFS','A*','IDA*']

def benchmark(IA,algoritmo):

    Yt = []
    Yp = []
    Ym = []

    for i in X:
        if algoritmo == 'BFS':
            IA.BFS(i)
        elif algoritmo == 'DFS':
            IA.DFS(i)
        elif algoritmo == 'A*':
            IA.AStar(i)
        elif algoritmo == 'IDA*':
            IA.IDAStar(i)

        Yt.append(IA.tiempo_ejecucion)
        Yp.append(bd.Board.calcularPuntuacion(IA.nodo_ganador.board))
        Ym.append(len(IA.encontrar_path(IA.nodo_ganador)))

    plt.plot(X, Yt, label='Tiempo', marker='o', color='blue')  # Graficar Yt vs X
    plt.plot(X, Yp, label='Puntuación', marker='s', color='red')  # Graficar Yp vs X
    plt.plot(X, Ym, label='Movimientos', marker='^', color='green')  # Graficar Yp vs X

    # Etiquetas y título
    plt.xlabel('Nodos Expandidos')
    plt.ylabel('Tiempo, Puntuación y Movimientos')
    plt.title(f'Tiempo, Puntuación y Movimientos del algoritmo: {algoritmo} ')

    # Mostrar leyenda
    plt.legend()

    # Mostrar grid
    plt.grid(True)

    # Mostrar gráfico
    plt.show()

#Graficar las 4 a la vez se vuelve un trabajo computacional muy grande y al final es lo mismo que ir una a una y guardar captura, por tanto ejecutar segun sea necesario:
IA = ai.Ai(board)
#benchmark(IA, "DFS")
#benchmark(IA, "DFS")
#benchmark(IA, "A*")
benchmark(IA, "IDA*")
