import ai
import board as bd
import matplotlib.ticker as ticker

import matplotlib.pyplot as plt

# Iniciamos la clase board y automaticamente genera la matriz del tablero
seed_array = [1,1,2,0,1,1,2,0,0,0,1,0,0,0,0,0,10340203,45849032]
board = bd.Board(seed_array)

# Lista de nodos a expandir, cambiar según sea necesario para probar diferentes benchmarks
X = [100,500,1000,1500,2000]
#Algoritmos Implementados
algoritmos=['BFS','DFS','A*','IDA*']

def benchmark(algoritmo):

    Yt = []
    Yp = []
    Ym = []

    IA = ai.Ai(board)

    for i in X:
        if algoritmo == 'BFS':
            IA.BFS(i)
        elif algoritmo == 'DFS':
            IA.DFS(i)
        elif algoritmo == 'A*':
            IA = ai.Ai(board, funcion_heuristica=ai.FuncionHeuristica_FichaMasAlta)
            IA.AStar(i)
        elif algoritmo == 'IDA*':
            IA = ai.Ai(board, funcion_heuristica=ai.FuncionHeuristica_distanciaDeUnionPoderosa,funcion_coste=ai.FuncionCoste_distanciaDeUnionPoderosa)
            IA.IDAStar(i)

        Yt.append(IA.tiempo_ejecucion)
        Yp.append(bd.Board.calcularPuntuacion(IA.nodo_ganador.board))
        Ym.append(len(IA.encontrar_path(IA.nodo_ganador)))

    for i in Yp:
        print(i)

    plt.plot(X, Yt, label='Tiempo', marker='o', color='blue')  # Graficar Yt vs X
    plt.plot(X, Yp, label='Puntuación', marker='s', color='red')  # Graficar Yp vs X
    plt.plot(X, Ym, label='Movimientos', marker='^', color='green')  # Graficar Yp vs X

    # Etiquetas y título
    plt.xlabel('Nodos Expandidos')
    plt.ylabel('Tiempo, Puntuación y Movimientos')
    plt.title(f'Tiempo, Puntuación y Movimientos del algoritmo: {algoritmo} ')

    # Creamos ticks adaptativos en el eje Y usando MaxNLocator
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))  # Cambiar n para modificar el número máximo de tics en el eje Y (un tick es un valor resaltado en el eje)

    # Mostrar leyenda
    plt.legend()

    # Mostrar grid
    plt.grid(True)

    # Mostrar gráfico
    plt.show()

#Graficar las 4 a la vez se vuelve un trabajo computacional muy grande y al final es lo mismo que ir una a una y guardar captura, por tanto ejecutar segun sea necesario:
benchmark("BFS")
#benchmark("DFS")
#benchmark("A*")
#benchmark("IDA*")
