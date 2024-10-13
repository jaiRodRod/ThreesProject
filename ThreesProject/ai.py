import const
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

reglasProducción = [const.Movimiento.ABAJO,const.Movimiento.ARRIBA,const.Movimiento.DERECHA,const.Movimiento.IZQUIERDA]

import board as bd

class MiNodo(Node):
    """
    Creamos un nodo con la estructura de Node pero con atributos personalizados:

    :param board Tablero con la situación actual de juego
    :param movimiento: Movimiento que condujo del padre a ese estado de tablero
    :param valor_heuristico: Por defecto cero para cuando no se utiliza, valor obtenido del cálculo de una función heurística sobre el nodo
    :param valor_F: este valor será la suma de la profundidad a la que se encuentra nodo en el árbol (coste g(n)) + el valor heurístico proporcionado (h(n))
    """
    def __init__(self, name, padre, board, movimiento, valor_heuristico=0):
        super().__init__(name, padre)
        self.board = board
        self.valor_F = self.depth + valor_heuristico
        self.movimiento = movimiento

class Ai:

    """
    Este constructor inicializa el algoritmo de búsqueda dado un tablero,
    inicializa la lista de abiertos y cerrados como lístas vacías, guarda
    el estado inicial del tablero, la raíz del arbol con el valor hash del tablero como
    nombre, con el board, sin padre ni movimiento y con el valor de la función heurística
    en el estado inicial. También guarda siempre el nodo con mejor puntuación y la
    función heurística en caso de que proceda.

    :param board: instancia inicial de la clase tablero en una nueva partida de Threes!
    :param funcion_heuristica: función heurística que se usará en el algoritmo de búsqueda
    por defecto es nula.
    """
    def __init__(self, board, funcion_heuristica=lambda x: 0):
        self.abiertos = []
        self.cerrados = []
        self.estadoInicial = board
        self.raiz = MiNodo(board.__hash__(), board=board, padre=None, movimiento=None, valor_heuristico=funcion_heuristica(self.estadoInicial))
        self.nodo_ganador = self.raiz
        self.funcion_heuristica = funcion_heuristica

    """
    Recorre el árbol desde el nodo ganador hasta la raíz guardando los tableros en una lista
    
    :param nodoGanador: nodo con más puntuación encontrado con un algoritmo de búsqueda determinado
    :return: Lista de tableros ordenada desde la raíz hasta el nodoGanador
    """
    def encontrar_path(self, nodo_ganador):
        path = []
        while nodo_ganador is not None:
            path.append(nodo_ganador.board)
            nodo_ganador = nodo_ganador.parent
        return path[::-1]

    """
    Muestra por consola el árbol de búsqueda obtenido tras desarrollar un algoritmo de búsqueda
    también importa este árbol en formato .dot
    """
    def mostrar_arbol(self):
        for pre, fill, node in RenderTree(self.raiz):
            print(f"{pre}{node.name} (Puntuación: {node.board.calcularPuntuacion()})")
        DotExporter(self.raiz).to_dotfile("arbol_busqueda.dot")

    """
    Añade a abiertos los nodos resultantes de la expansión del nodo "nodo_padre" aplicando
    las  diferentes reglas de producción del juego Threes!. Se guardan los tableros a expandir como 
    una copia independiente del nodo padre para evitar que la regla de producción altere al 
    nodo padre.
    
    Cada regla de producción se intenta aplicar a la copia del tablero padre y se comprueba que se 
    obtenga un nuevo tablero y este no haya sido explorado antes (no se encuentra ni en abiertos ni
    en cerrados) si se cumple esta condición, se calcula su heurístico, se crea el nodo hijo cuyo nombre 
    es el hash del nuevo tablero y guarda el nuevo tablero, un puntero al nodo padre, el movimiento que
    se acaba de aplicar y el valor heurístico calculado.
    
    Para cada nuevo nodo se comprueba que sea el de mejor puntuación en tal caso se guarda.
    
    :param nodo_padre:  nodo que queremos expandir.
    """
    def calcularAbiertos(self, nodo_padre):
        for i in range (len(reglasProducción)):
            padre = nodo_padre.board
            nuevoTablero = bd.Board.__copy__(padre)

            nuevoTablero.moverTablero(reglasProducción[i])

            if nuevoTablero and self.esNuevo(nuevoTablero):
                    resultado_heuristico = self.funcion_heuristica(nuevoTablero);
                
                    nodoHijo = MiNodo(nuevoTablero.__hash__(),board = nuevoTablero, padre=nodo_padre, movimiento=reglasProducción[i], valor_heuristico=resultado_heuristico)

                    if bd.Board.calcularPuntuacion(self.nodo_ganador.board) < bd.Board.calcularPuntuacion(nuevoTablero):
                        self.nodo_ganador = nodoHijo

                    self.abiertos.append(nodoHijo)

    """ 
    Comprueba usando equals si un tablero se encuentra en cerrados
    
    :param tablero: tablero a buscar en la lista de cerrados
    :return: True si está en cerrados False en caso contrario
    """
    def estaEnCerrados(self, tablero):
        for cerrado in self.cerrados:
            if tablero.__eq__(cerrado.board):
                return True
        return False

    """ 
    Comprueba usando equals si un tablero se encuentra en abiertos

    :param tablero: tablero a buscar en la lista de abiertos
    :return: True si está en abiertos False en caso contrario
    """
    def estaEnAbiertos(self, tablero):
        for abierto in self.abiertos:
            if tablero.__eq__(abierto.board):
                return True
        return False

    """
    Nos dice si un tablero es nuevo en el árbol de exploración
    comprobando que no esté en cerrados ni abiertos
    :param tablero: tablero a comprbar
    _return: True si es nuevo en la búsueda False en caso contrario
    """
    def esNuevo(self,tablero):
        return not self.estaEnCerrados(tablero) and not self.estaEnAbiertos(tablero)

    """
    Muestra los resultados tras la aplicación de un algoritmo de búsqueda
    Mostrando por pantalla el estado con mejor puntución y el camino desde la raíz
    a ese estado.
    """
    def mostrarResultado(self):
        print("\nEstado ganador:\n", self.nodo_ganador.board.board)
        print("\nPath ganador:")
        path = self.encontrar_path(self.nodo_ganador)
        for estado in path:
            print(estado)
            print("\n")
    
    """
    :param porMenorValorF: 
        True si busca el nodo con menor valor_F,
        False si busca el nodo con mayor valor_F
    :param porAntiguedad: 
        True si siempre se queda con el primer nodo que encuentra con mejor valor_F (el más antiguo)
        False si siempre se queda con el último nodo que encuentra con mejor valor_F (el más nuevo)
    :return: indice del nodo con mejor valor_F según criterio dado
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

    """
    Búsqueda en amplitud, calcula los abiertos de la raiz y va iterativamente
    sacando nodos de abiertos (antiguos primeros), metiendolos en cerrados y
    calculando los abiertos del nuevo nodo hasta que se de la condición de parada
    que puede ser que se alcance al máximo de expansiones permitidas o que no queden
    más nodos por abrir (se acaba el propio juego). Tras finalizar siempre muestra resultados
    
    :param max_steps: parámetro opcional para regular el número de expansiones permitidos en la exploracion
    por defecto tiene valor 100
    """
    def BFS(self,max_steps=100):
        self.calcularAbiertos(self.raiz)
        step = 1
        while step<=max_steps:
            n = self.abiertos.pop(0)
            self.cerrados.append(n)
            self.calcularAbiertos(n)

            step += 1

        self.mostrarResultado()

    """
    Búsqueda en profundidad, calcula los abiertos de la raiz y va iterativamente
    sacando nodos de abiertos (nuevos primeros), metiendolos en cerrados y
    calculando los abiertos del nuevo nodo hasta que se de la condición de parada
    que puede ser que se alcance al máximo de expansiones permitidas o  que no queden
    más nodos por abrir (se acaba el propio juego). Tras finalizar siempre muestra resultados

    :param max_steps: parámetro opcional para regular el número de expansiones permitidos en la exploracion
    por defecto tiene valor 100
    """
    def DFS(self,max_steps=100):
        self.calcularAbiertos(self.raiz)
        step = 1
        while step <= max_steps:
            n = self.abiertos.pop()
            self.cerrados.append(n)
            self.calcularAbiertos(n)

            step += 1

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