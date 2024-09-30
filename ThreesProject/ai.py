import pandas as pd
import numpy as np
import const

#https://builtin.com/articles/tree-python (referencias para el árbol)
from bigtree import dataframe_to_tree

reglasProducción = [const.Movimiento.ABAJO,const.Movimiento.ARRIBA,const.Movimiento.DERECHA,const.Movimiento.IZQUIERDA]

import board as bd


# En este problema carecemos de estado objetivo, se juega hasta que la lista de abiertos esté vacia y luego nos quedamos con el mejor resultado
class Ai:

    def __init__(self,board):
        #Lista abiertos
        self.abiertos = []
        #Lista cerrados
        self.cerrados = []
        #Guardamos el tablero
        self.estadoInicial = board
        #Guardamos el estado ganador inicialmente s
        self.estadoGanador = self.estadoInicial
        #Guardamos el árbol de búsqueda
        self.path_data = pd.DataFrame(
            [
                ["1",self.estadoInicial,0,None]
            ],
            columns=["PATH","Estado","Valor_F","Puntero"],
        )

    # Buscar en el DataFrame (árbol) la fila que tenga un estado igual a n y devuelvo el path
    def encontrar_path(self, n):
        for index, row in self.path_data.iterrows():
            estado_actual = row['Estado']
            # Usamos np.array_equal si los estados son arrays o estructuras similares
            if np.array_equal(estado_actual, n):
                return row['PATH']  # Devolver el valor de la columna PATH correspondiente a ese estado
        return None  # Si no se encuentra el estado

    # Devuelve una lista de nodos tras la expansion de un nodo
    def calcularAbiertos(self,n,orden):
        for i in range (len(reglasProducción)):
            n2 = n.moverTablero(n,reglasProducción[i]).obtenerEstado()
            # Obtenemos nodos n2 que no estén en cerrados ni abiertos
            if not any(np.array_equal(n2, cerrado) for cerrado in self.cerrados) and not any(np.array_equal(n2, abierto) for abierto in self.abiertos):
                orden += 1
                # Mantenemos actualizado el estado con mejor puntuación
                if bd.calcularPuntuacion(self.estadoGanador) < bd.calcularPuntuacion(n2):
                    self.estadoGanador = n2
                # Guardamos n2 en abiertos
                self.abiertos.append(n2)
                # Añadimos información al path_data poniendo el puntero al nodo anterior (n)
                # Primero recuperamosel path anterior
                path_anterior = self.encontrar_path(n)
                nueva_fila = pd.DataFrame(
                    [[ path_anterior +"/" + str(orden), n2, 0, n]],
                    columns=["PATH", "Estado", "A", "Puntero"]
                )
                self.path_data = pd.concat([self.path_data, nueva_fila], ignore_index=True)
        return orden

    #Búsquedda en amplitud
    def BFS(self):
        orden = 1
        # Calculamos nodos abiertos en s
        orden = self.calcularAbiertos(self.estadoInicial,orden)
        # La lista de nodos cerrados se inicializa a vacia
        while len(self.abiertos)>0:
            # Sacamos el nodo n de abiertos, al sacar el primero estamos sacando el de mayor antigüedad
            n = self.abiertos.pop(0)
            # Añadimos n a Cerrados
            self.cerrados.append(n)
            # Expandimos n obteniendo M
            orden = self.calcularAbiertos(n,orden)

        # Al finalizar, estadoGanador contiene el estado con la mejor puntuación
        print("Estado ganador:", self.estadoGanador)
        print("Path ganador:", self.encontrar_path(self.estadoGanador))

    #Búsqueda en profuncidad
    def DFS(self):
        orden = 1
        # Calculamos nodos abiertos en s
        orden = self.calcularAbiertos(self.estadoInicial, orden)
        # La lista de nodos cerrados se inicializa a vacia
        while len(self.abiertos) > 0:
            # Sacamos el nodo n de abiertos, al sacar el último estamos sacando el más nuevo
            n = self.abiertos.pop()
            # Añadimos n a Cerrados
            self.cerrados.append(n)
            # Expandimos n obteniendo M
            orden = self.calcularAbiertos(n, orden)

        # Al finalizar, estadoGanador contiene el estado con la mejor puntuación
        print("Estado ganador:", self.estadoGanador)
        print("Path ganador:", self.encontrar_path(self.estadoGanador))