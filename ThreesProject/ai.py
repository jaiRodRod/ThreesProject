import const
import time
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
    def __init__(self, name, padre, board, movimiento, valor_heuristico=0, valor_coste=None):
        super().__init__(name, padre)
        self.board = board
        if valor_coste == None: valor_coste = self.depth
        self.valor_F = valor_coste + valor_heuristico
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
    def __init__(self, board, funcion_heuristica=lambda x: 0, funcion_coste = None):
        self.abiertos = []
        self.cerrados = []
        self.estadoInicial = board
        self.raiz = MiNodo(board.__hash__(), board=board, padre=None, movimiento=None, valor_heuristico=funcion_heuristica(self.estadoInicial))
        self.nodo_ganador = self.raiz
        self.funcion_heuristica = funcion_heuristica
        self.funcion_coste = None
        if funcion_coste != None: self.funcion_coste = funcion_coste

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

    def encontrar_path_interfaz(self, nodo_ganador):
        path = []
        while nodo_ganador is not None:
            path.append(nodo_ganador.movimiento)
            nodo_ganador = nodo_ganador.parent
        return path[::-1]

    """
    Muestra por consola el árbol de búsqueda obtenido tras desarrollar un algoritmo de búsqueda
    también importa este árbol en formato .dot
    """
    def mostrar_arbol(self):
        for pre, fill, node in RenderTree(self.raiz):
            print(f"{pre}{node.name} | Valor_F {node.valor_F} (Puntuación: {node.board.calcularPuntuacion()})")
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
            resultado_coste = None
            if self.funcion_coste != None:
                resultado_coste = self.funcion_coste(nodo_padre.board)

            nuevoTablero.moverTablero(reglasProducción[i])

            if nuevoTablero and self.esNuevo(nuevoTablero):
                    resultado_heuristico = self.funcion_heuristica(nuevoTablero)
                
                    nodoHijo = MiNodo(nuevoTablero.__hash__(),board = nuevoTablero, padre=nodo_padre, movimiento=reglasProducción[i], valor_heuristico=resultado_heuristico, valor_coste=resultado_coste)

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
    def mostrarResultado(self,tiempo_ejecucion,steps):
        print("\nEstado ganador:\n", self.nodo_ganador.board.board)
        print(f"Con puntuación: {bd.Board.calcularPuntuacion(self.nodo_ganador.board)}\nTiempo de ejecución {tiempo_ejecucion} segundos y se han expandido {steps-1} nodos")
        print("\nSecuencia de movimientos:")
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
        mejor_valor_F = self.abiertos[0].valor_F
        indice_mejor_nodo = 0;
        
        # Buscamos en toda la lista, sabiendo el índice, qué nodo tiene mejor valor_F
        for index, nodo in enumerate(self.abiertos):
            
            # Caso normal en el que se encuentra un mejor valor_F
            if((porMenorValorF and nodo.valor_F < mejor_valor_F) or (not porMenorValorF and nodo.valor_F > mejor_valor_F)):
                mejor_valor_F = nodo.valor_F
                indice_mejor_nodo = index
                
            # Caso especial en el que se encuentra un valor_F igual al que se tiene como mejor
            elif(not porAntiguedad and nodo.valor_F == mejor_valor_F):
                indice_mejor_nodo = index
            
        return indice_mejor_nodo
    
    """
    Función recursiva para el algoritmo IDA*. Realiza búsqueda en profundidad limitada por F(n).
    
    :param nodo: nodo actual en la búsqueda
    :param limite: límite de F(n) en la iteración actual
    :param step: paso actual en la búsqueda
    :param max_steps: número máximo de expansiones permitidas
    :return: Si se encuentra solución, devuelve el nodo ganador; si no, devuelve el nuevo límite más bajo que supera el límite actual.
    """
    def IDAStar_Recursivo(self, nodo, limite, step, max_steps):
    
        # Si el valor F(n) del nodo actual excede el límite, devolvemos el valor F(n)
        if nodo.valor_F > limite:
            return None, nodo.valor_F
        
        # Si el nodo actual es el nodo ganador, devolvemos el nodo
        if bd.Board.calcularPuntuacion(self.nodo_ganador.board) < bd.Board.calcularPuntuacion(nodo.board):
            self.nodo_ganador = nodo
        
        # Inicializamos el siguiente límite como infinito
        nuevo_limite = float('inf')
        
        # Expandimos el nodo actual
        self.calcularAbiertos(nodo)
        
        # Recorremos los nodos hijos en la búsqueda
        for hijo in self.abiertos:
            # Llamamos recursivamente a IDAStar_recursivo con los nodos hijos
            resultado, temp_limite = self.IDAStar_Recursivo(hijo, limite, step + 1, max_steps)
            
            # Si encontramos la solución, devolvemos el nodo
            if resultado is not None:
                return resultado, None
            
            # Actualizamos el nuevo límite si encontramos un valor F(n) menor
            if temp_limite < nuevo_limite:
                nuevo_limite = temp_limite

            # Avanzamos un paso de expansión
            step += 1
        
        # Si no encontramos la solución, devolvemos el nuevo límite más bajo que excede el actual
        return None, nuevo_limite

    """
    Búsqueda en amplitud, calcula los abiertos de la raiz y va iterativamente
    sacando nodos de abiertos (antiguos primeros), metiendolos en cerrados y
    calculando los abiertos del nuevo nodo hasta que se de la condición de parada
    que puede ser que se alcance al máximo de expansiones permitidas o que no queden
    más nodos por abrir (se acaba el propio juego). Tras finalizar siempre muestra resultados.
    
    :param max_steps: parámetro opcional para regular el número de expansiones permitidos en la exploracion
    por defecto tiene valor 100
    """
    def BFS(self,max_steps=100):
        print("[ Algoritmo BFS ]")
        inicio = time.time()
        
        self.calcularAbiertos(self.raiz)
        step = 1
        
        while step<=max_steps:
            n = self.abiertos.pop(0)
            
            self.cerrados.append(n)
            
            self.calcularAbiertos(n)
            
            print("Calculando: " + str(step))
            step += 1
            
        final = time.time()
        self.mostrarResultado(final-inicio,step)

    """
    Búsqueda en profundidad, calcula los abiertos de la raiz y va iterativamente
    sacando nodos de abiertos (nuevos primeros), metiendolos en cerrados y
    calculando los abiertos del nuevo nodo hasta que se de la condición de parada
    que puede ser que se alcance al máximo de expansiones permitidas o  que no queden
    más nodos por abrir (se acaba el propio juego). Tras finalizar siempre muestra resultados.

    :param max_steps: parámetro opcional para regular el número de expansiones permitidos en la exploracion
    por defecto tiene valor 100
    """
    def DFS(self,max_steps=100):
        print("[ Algoritmo DFS ]")
        inicio = time.time()
        
        self.calcularAbiertos(self.raiz)
        step = 1
        
        while step <= max_steps:
            n = self.abiertos.pop()
            
            self.cerrados.append(n)
            
            self.calcularAbiertos(n)
            
            print("Calculando: " + str(step))
            step += 1

        final = time.time()
        self.mostrarResultado(final-inicio,step)
        
    """
    Búsqueda A*, calcula los abiertos de la raiz y va iterativamente
    sacando nodos de abiertos (el de mejor valor F, por defecto el menor), metiéndolos en cerrados y
    calculando los abiertos del nuevo nodo hasta que se de la condición de parada
    que puede ser que se alcance al máximo de expansiones permitidas o que no queden
    más nodos por abrir (se acaba el propio juego). Tras finalizar siempre muestra resultados.

    :param max_steps: parámetro opcional para regular el número de expansiones permitidos en la exploración
    por defecto tiene valor 100
    """
    def AStar(self, max_steps=100):
        print("[ Algoritmo A* ]")
        inicio = time.time()
        
        # Calculamos nodos abiertos en la raíz
        self.calcularAbiertos(self.raiz)
        # La lista de nodos cerrados se inicializa a vacia en el propio constructor
        step = 1
        
        while step <= max_steps:
            # Obtenemos el índice del nodo abierto con menor valor_F (el más antiguo)
            n_index = self.obtenerIndiceMejorValorF() # Menor valor + Por Antigüedad
            # Sacamos el nodo n de abiertos, sacamos siempre el que menor valor_F tiene
            n = self.abiertos.pop(n_index)
            # Añadimos nodo n a Cerrados
            self.cerrados.append(n)
            # Expandimos n obteniendo nuevos nodos en abiertos
            self.calcularAbiertos(n)

            print("Calculando: " + str(step))
            step += 1

        final = time.time()
        # Mostramos resultados obtenidos
        self.mostrarResultado(final-inicio,step)
        
    """
    Búsqueda IDA* realiza una búsqueda iterativa en profundidad limitada
    en cada iteración aumenta el límite de profundidad según el valor F(n) más bajo que 
    sobrepasa el límite anterior. Se para cuando encuentra la solución o cuando no hay más nodos 
    por expandir. 

    :param max_steps: parámetro opcional para regular el número de expansiones permitidos en la exploración
    por defecto tiene valor 100
    """
    def IDAStar(self, max_steps=100):
        print("[ Algoritmo IDA* ]")
        inicio = time.time()
        
        # La lista de nodos cerrados se inicializa a vacia en el propio constructor
        step = 1
        # Lista con todo el historial de cotas usadas
        cotas = [] 
        # Inicializar el límite como el valor F de la raíz
        cotas.append(self.raiz.valor_F)
        
        while step <= max_steps:
            print("Intento con cota: " + str(cotas[-1]))
            
            # Siempre se reinicia la lista de abiertos con solo de raíz
            self.abiertos = [self.raiz]  
            # Reiniciamos los nodos cerrados a ninguno
            self.cerrados = []
            # Mantiene el menor F que sobrepasa la cota, ponemos por defecto infinito para cuando entre el primer candidato
            nueva_cota = float('inf')  

            # El bucle termina si la pila se queda sin nodos
            while self.abiertos:
                
                # Obtenemos el nodo más externo de la pila
                nodo_actual = self.abiertos.pop()
                #Guardamos temporalmente el nodo en cerrados 
                self.cerrados.append(nodo_actual)
                
                # Si el nodo excede el límite actual de F, actualiza la nueva cota candidata que habrá próxima para cuando actualicemos la cota
                if nodo_actual.valor_F > cotas[-1]:
                    # Nos quedamos con el valorF que supere nuestra cota actual pero que sea de menor valor
                    nueva_cota = min(nueva_cota, nodo_actual.valor_F)
                    # Con esto saltamos esta iteración y así no expandimos este nodo ahora mismo
                    continue 
                
                # Expandimos el nodo actual
                self.calcularAbiertos(nodo_actual)
                
                print("Calculando: " + str(step))
                step += 1
                
                # Si excedemos los pasos sale de este bucle para salir del otro también
                if step > max_steps:
                    break
            
            # Si encontramos la solución, salimos del bucle principal
            if self.nodo_ganador:
                break
            
            # Si no hemos encontrado solución, actualizamos el límite
            cotas.append(nueva_cota)
        
            # Si no hay más nodos por expandir y el nuevo límite es infinito
            if cotas[-1] == float('inf'):
                print("No se ha encontrado solución.")
                break
            
        final = time.time()
        # Mostramos resultados obtenidos
        self.mostrarResultado(final-inicio,step)
        
        

# Heurísticos
    
def FuncionHeuristica_CasillasVacias(board):
    return board.huecos()
        
def manhattan(a, b, c, d):
    return abs(a-c) + abs(b-d)

def FuncionHeuristica_FichaMasAlta(board):
    highestValue, X, Y = board.getHighestValue()
    return -min(manhattan(X,Y,0,0),manhattan(X,Y,0,3),manhattan(X,Y,3,0),manhattan(X,Y,3,3))

def unionMasAltaDelTablero(board):
    maxPair = 3
    listValues = []
    for i in range(0,4):
        for j in range(0,4):
            ficha = board.board[i][j]
            if listValues.__contains__(ficha) and ficha*2 > maxPair:
                maxPair = ficha*2
            else: listValues.append(ficha)
    return maxPair

def estimadorMovimientosHastaUnion(board):
    maxUnion = unionMasAltaDelTablero(board)
    numeroMovimientos = 0
    listFichas = []
    distanciaMinima = 7
    parejaMinima = []
    if maxUnion == 3:
        numeroMovimientos = 6
    else:
        for i in range(0,4):
            for j in range(0,4):
                ficha = board.board[i][j]
                if(ficha == maxUnion/2):
                    listFichas.append((i,j))
        for i in range(0,listFichas.__len__()):
            for j in range(i+1,listFichas.__len__()):
                if manhattan(listFichas[i][0],listFichas[i][1],listFichas[j][0],listFichas[j][1]) < distanciaMinima:
                    parejaMinima.clear()
                    parejaMinima.append(listFichas[i])
                    parejaMinima.append(listFichas[j])
        if parejaMinima[0][0] == parejaMinima[1][0]:
            if parejaMinima[0][1] == 0 or parejaMinima[0][1] == 3 or parejaMinima[1][1] == 0 or parejaMinima[1][1] == 3:
                numeroMovimientos = manhattan(parejaMinima[0][0], parejaMinima[0][1], parejaMinima[1][0], parejaMinima[1][1])
            else: numeroMovimientos = 2
        elif parejaMinima[0][1] == parejaMinima[1][1]:
            if parejaMinima[0][0] == 0 or parejaMinima[0][0] == 3 or parejaMinima[1][0] == 0 or parejaMinima[1][0] == 3:
                numeroMovimientos = manhattan(parejaMinima[0][0], parejaMinima[0][1], parejaMinima[1][0], parejaMinima[1][1])
            else: numeroMovimientos = 2
        else:
            numeroMovimientos = manhattan(parejaMinima[0][0], parejaMinima[0][1], parejaMinima[1][0], parejaMinima[1][1]) + min(
                manhattan(parejaMinima[0][0], parejaMinima[0][1],0,0),manhattan(parejaMinima[0][0], parejaMinima[0][1],0,3),
                manhattan(parejaMinima[0][0], parejaMinima[0][1],3,0),manhattan(parejaMinima[0][0], parejaMinima[0][1],3,3),
                manhattan(parejaMinima[1][0], parejaMinima[1][1],0,0),manhattan(parejaMinima[1][0], parejaMinima[1][1],0,3),
                manhattan(parejaMinima[1][0], parejaMinima[1][1],3,0),manhattan(parejaMinima[1][0], parejaMinima[1][1],3,3))
    return numeroMovimientos

maximoPlanteadoPuntuacionFicha = 98304
#maximoPlanteadoPuntuacionFicha = 768

def FuncionHeuristica_distanciaDeUnionPoderosa(board):
    return estimadorMovimientosHastaUnion(board) * (maximoPlanteadoPuntuacionFicha/(unionMasAltaDelTablero(board)/2))

def FuncionCoste_distanciaDeUnionPoderosa(board):
    return maximoPlanteadoPuntuacionFicha/unionMasAltaDelTablero(board)


# Ejecución

#board = bd.Board()
#seed_array = [0,0,0,3,0,0,2,0,0,1,0,0,3,0,0,0,10340203,45849032]
#board = bd.Board(seed_array)

#print("Unión más Alta del tablero: " + str(unionMasAltaDelTablero(board)))
#print("Estimador Movimientos hasta unión: " + str(estimadorMovimientosHastaUnion(board)))

#ai = Ai(board, funcion_heuristica=FuncionHeuristica_FichaMasAlta)
#ai = Ai(board, funcion_heuristica=FuncionHeuristica_CasillasVacias)
#ai = Ai(board, funcion_heuristica=FuncionHeuristica_distanciaDeUnionPoderosa, funcion_coste=FuncionCoste_distanciaDeUnionPoderosa)

#print("Estado inicial:")
#print(ai.estadoInicial)

#ai.BFS()
#ai.DFS()
#ai.AStar(1000)
#ai.IDAStar(2000)
#ai.mostrar_arbol()



#ai2 = Ai(board, funcion_heuristica=FuncionHeuristica_distanciaDeUnionPoderosa, funcion_coste=FuncionCoste_distanciaDeUnionPoderosa)

#print("Estado inicial:")
#print(ai2.estadoInicial)

#ai2.IDAStar(2000)
#ai2.mostrar_arbol()