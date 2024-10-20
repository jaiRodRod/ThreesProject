import ai
import board as bd

import matplotlib.pyplot as plt

# Iniciamos la clase board y automaticamente genera la matriz del tablero
seed_array = [1,1,2,0,1,1,2,0,0,0,1,0,0,0,0,0,10340203,45849032]
board = bd.Board(seed_array)

# Lo suyo seria cambiar este a 100,1000,5000 y 10000 aunque ya cuando tengamos IDA* bien pq esto tarda en ejecutar...
X = [100,1000]
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

    return Yt,Yp,Ym

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Graficamos el tiempo de ejecución la puntuación y los movimientos de juego de cada algoritmo implementado en un numero de expansiones permitidas:
for idx,alg in enumerate(algoritmos):
    IA = ai.Ai(board)
    Yt, Yp,Ym = benchmark(IA, alg)

    ax = axs[idx // 2, idx % 2]

    ax.plot(X, Yt, label=f'{alg} - tiempo', marker='o', color='blue')
    ax.plot(X, Yp, label=f'{alg} - puntuación', marker='s', color='red')
    ax.plot(X, Ym, label=f'{alg} - movimientos', marker='^', color='green')


    ax.set_xlabel('Nodos Expandidos')
    ax.set_ylabel('Tiempo, Puntuación y Pasos')
    ax.set_title(f'Comparación {alg} vs nodos expandidos')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()
