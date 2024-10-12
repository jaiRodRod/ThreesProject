import const
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

reglasProducción = [const.Movimiento.ABAJO,const.Movimiento.ARRIBA,const.Movimiento.DERECHA,const.Movimiento.IZQUIERDA]

import board as bd

"""
Creamos un nodo con la estructura de Node pero con los atributos personalizados:
    board: Tablero con la situación actual de juego
    movimiento: Movimiento que condujo del padre a ese estado de tablero
    valor_heuristico: Por defecto cero para cuando no se utiliza, valor obtenido del cálculo de una función heurística sobre el nodo
Esta clase contiene además un atributo valor_F, este valor será la suma de la profundidad a la que se encuentra nodo en el árbol + el valor heurístico proporcionado
"""
class MiNodo(Node):
    def __init__(self, name, padre, board, movimiento, valor_heuristico=0):
        super().__init__(name, padre)
        self.board = board
        self.valor_F = self.depth + valor_heuristico # El coste de la función para lo que llevo hasta ahora corresponde con la profundidad + valor heurístico calculado
        self.movimiento = movimiento # Guardamos que movimiento desde el padre ha llevado a este estado

# En este problema carecemos de estado objetivo, se juega hasta que la lista de abiertos esté vacia y luego nos quedamos con el mejor resultado
class Ai:

    def __init__(self, board, funcion_heuristica=lambda x: 0):
        # Lista abiertos
        self.abiertos = []
        # Lista cerrados
        self.cerrados = []
        # Estado inicial
        self.estadoInicial = board
        # Guardamos la raíz árbol de búsqueda
        self.raiz = MiNodo(board.__hash__(), board=board, padre=None, movimiento=None, valor_heuristico=funcion_heuristica(self.estadoInicial))
        # Guardamos el nodo ganador, inicialmente raíz
        self.nodo_ganador = self.raiz
        # Guardamos la función heurística que se utilizará si se usa un algoritmo con ella
        self.funcion_heuristica = funcion_heuristica

        self.cont = 0

    # Se usa esta función para obtener el camino del nodo objetivo a la raíz
    def encontrar_path(self, nodo):
        path = []
        while nodo is not None:
            path.append(nodo.board)  # Guardamos el tablero en el camino
            nodo = nodo.parent  # Movemos al padre
        return path[::-1]  # Invertimos el camino

    # Dibuja el arbol y lo exporta en formato .dot
    def mostrar_arbol(self):
        for pre, fill, node in RenderTree(self.raiz):
            print(f"{pre}{node.name} (Puntuación: {node.board.calcularPuntuacion()})")
        # Exportamos el árbol a un formato gráfico (graphviz)
        DotExporter(self.raiz).to_dotfile("arbol_busqueda.dot")

    # Añade a abiertos los nodos resultantes de la expansión del nodo "nodo_padre"
    def calcularAbiertos(self, nodo_padre):
        for i in range (len(reglasProducción)):
            # Obtenemos el tablero del nodo padre
            padre = nodo_padre.board
            # Creamos un tablero nuevo para evitar usar la misma referencia y alterar el nodo padre
            nuevoTablero = bd.Board.__copy__(padre)

            # Copiamos el tablero del padre al nuevo tablero

            #Movemos el nuevo tablero según la regla de producción correspondiente
            nuevoTablero.moverTablero(reglasProducción[i])

            #Si la regla ha sido aplicable y obtenemos tableros que no estén en cerrados ni abiertos (nodo nuevo)
            if nuevoTablero is not None and self.esNuevo(nuevoTablero):
                    # Calculamos el heurístico
                    resultado_heuristico = self.funcion_heuristica(nuevoTablero);
                
                    # Añadimos información al arbol creando un nodoHijo y poniendo el puntero al nodo padre
                    nodoHijo = MiNodo(nuevoTablero.__hash__(),board = nuevoTablero, padre=nodo_padre, movimiento=reglasProducción[i], valor_heuristico=resultado_heuristico)

                    # Mantenemos actualizado el estado con mejor puntuación
                    if bd.Board.calcularPuntuacion(self.nodo_ganador.board) < bd.Board.calcularPuntuacion(nuevoTablero):
                        self.nodo_ganador = nodoHijo

                    #Añadimos el nodo a abiertos
                    self.abiertos.append(nodoHijo)

    # Comprueba usando equals si el nuevo tablero se encuentra en cerrados
    def estaEnCerrados(self, tablero):
        for cerrado in self.cerrados:
            if tablero.__eq__(cerrado.board):
                return True
        return False

    # Comprueba usando equals si el nuevo tablero se encuentra en abiertos
    def estaEnAbiertos(self, tablero):
        for abierto in self.abiertos:
            if tablero.__eq__(abierto.board):
                return True
        return False

    # Nos dice si un tablero es nuevo en el árbol de exploración
    def esNuevo(self,tablero):
        return not self.estaEnCerrados(tablero) and not self.estaEnAbiertos(tablero)

    def mostrarResultado(self):
        # Mostramos resultados obtenidos
        print("\nEstado ganador:\n", self.nodo_ganador.board.board)
        print("\nPath ganador:")
        path = self.encontrar_path(self.nodo_ganador)
        for estado in path:
            print(estado)
            print("\n")
    
    """
    Devuelve el índice del nodo con valor_F mejor (según se le indique)
        porMenorValorF: 
            True si busca el nodo con menor valor_F,
            False si busca el nodo con mayor valor_F
        porAntiguedad: 
            True si siempre se queda con el primer nodo que encuentra con mejor valor_F (el más antiguo)
            False si siempre se queda con el último nodo que encuentra con mejor valor_F (el más nuevo)
    """
    def obtenerIndiceMejorValorF(self, porMenorValorF=True, porAntiguedad=True):
        mejor_valor_F = self.abiertos[0].valor_F;
        indice_mejor_nodo = 0;
        
        # Buscamos en toda la lista, sabiendo el índice, qué nodo tiene mejor valor_F
        for index, nodo in enumerate(self.abiertos):
            
            # Caso normal en el que se encuentra un mejor valor_F
            if((porMenorValorF and nodo.valor_F < mejor_valor_F) or (not porMenorValorF and nodo.valor_F > mejor_valor_F)):
                mejor_valor_F = nodo.valor_F;
                indice_mejor_nodo = index;
                
            # Caso especial en el que se encuentra un valor_F igual al que se tiene como mejor
            elif(not porAntiguedad and nodo.valor_F == mejor_valor_F):
                indice_mejor_nodo = index;
            
        return indice_mejor_nodo;    

    # Búsqueda en amplitud, tiene el parámetro opcional max_steps para regular el número de expansiones permitidos en la exploracion, si no acotamos, tardará mucho...
    def BFS(self,max_steps=100):
        # Calculamos nodos abiertos en la raíz
        self.calcularAbiertos(self.raiz)
        # La lista de nodos cerrados se inicializa a vacia en el propio constructor
        step = 1
        while step<=max_steps:
            # Sacamos el nodo n de abiertos, al sacar el primero estamos sacando el de mayor antigüedad (Amplitud)
            n = self.abiertos.pop(0)
            # Añadimos nodo n a Cerrados
            self.cerrados.append(n)
            # Expandimos n obteniendo nuevos nodos en abiertos
            self.calcularAbiertos(n)

            #Avanzamos un paso de expansion
            step += 1

        # Mostramos resultados obtenidos
        self.mostrarResultado()

    # Búsqueda en profundidad, tiene el parámetro opcional max_steps para regular el número de expansiones permitidos en la exploracion, si no acotamos, tardará mucho...
    def DFS(self,max_steps=100):
        # Calculamos nodos abiertos en la raíz
        self.calcularAbiertos(self.raiz)
        # La lista de nodos cerrados se inicializa a vacia en el propio constructor
        step = 1
        while step <= max_steps:
            # Sacamos el nodo n de abiertos, al sacar el último estamos sacando el de menor antigüedad
            n = self.abiertos.pop()
            # Añadimos nodo n a Cerrados
            self.cerrados.append(n)
            # Expandimos n obteniendo nuevos nodos en abiertos
            self.calcularAbiertos(n)

            #Avanzamos un paso de expansion
            step += 1

        # Mostramos resultados obtenidos
        self.mostrarResultado()
        
    # Algoritmo A*
    def AStar(self, max_steps=100):
        # Calculamos nodos abiertos en la raíz
        self.calcularAbiertos(self.raiz)
        # La lista de nodos cerrados se inicializa a vacia en el propio constructor
        step = 1
        
        while step <= max_steps:
            # Obtenemos el índice del nodo abierto con menor valor_F (el más antiguo)
            n_index = self.obtenerIndiceMejorValorF(); # Menor valor + Por Antigüedad
            # Sacamos el nodo n de abiertos, sacamos siempre el que menor valor_F tiene
            n = self.abiertos.pop(n_index)
            # Añadimos nodo n a Cerrados
            self.cerrados.append(n)
            # Expandimos n obteniendo nuevos nodos en abiertos
            self.calcularAbiertos(n)

            #Avanzamos un paso de expansion
            step += 1
        
        # Mostramos resultados obtenidos
        self.mostrarResultado()
        
        
def FuncionHeuristica_CasillasVacias(board):
    return board.huecos();

board = bd.Board()
ai = Ai(board, funcion_heuristica=FuncionHeuristica_CasillasVacias)

print("Estado inicial:")
print(ai.estadoInicial)

#ai.BFS()
#ai.DFS()
ai.AStar()
ai.mostrar_arbol()


# print("A*")
# ai2 = Ai(board)
# print("Estado inicial:")
# print(ai2.estadoInicial)
# ai2.AStar()
# ai2.mostrar_arbol()