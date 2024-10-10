import numpy as np

import const


class Board:

    board = np.zeros((4,4),np.dtype('uint8'))
    siguienteFicha = 0
    randomNextFicha = np.random.default_rng()
    randomNextPosition = np.random.default_rng()

    #El constructor del tablero
    def __init__(self, seed=None):
        """
        Este constructor genera un estado inicial aleatorio o
        segun una semilla del tablero 4x4 que añade las semillas
        del generador de valores de la ficha y el generador de
        posicion de la ficha
        :param seed: Una semilla que es una lista de 16 numeros que
        representan el tablero de izquierda a derecha y de arriba a
        abajo respectivamente, el valor 17 de la lista es la seed que
        genera el random concreto para generar fichas y el valor 18
        es la seed del random para la posicion en la que se colocaran
        las nuevas fichas
        """
        if seed:
            n = 0
            for i in range(0,4):
                for j in range(0,4):
                    self.board[i,j] = seed[n]
                    n+=1
            self.randomNextFicha = np.random.default_rng(seed[n])
            self.randomNextPosition = np.random.default_rng(seed[n+1])
            self.siguienteFicha = self.randomSiguienteFicha()
        else:
            for i in range(0,4):
                for j in range(0,4):
                    #Generamos un valor inicial
                    randomInitInt = np.random.randint(0,10)
                    self.board[i,j] = self.generarFicha(randomInitInt)
            self.siguienteFicha = self.randomSiguienteFicha()

    def copy(self, boardToCopy):
        """
        Esta funcion sirve para copiar el estado de un board.

        :param boardToCopy: Instancia de la clase board con los datos a copiar
        :return: Copia al board actual el boardToCopy
        """
        self.board = boardToCopy.board
        self.siguienteFicha = boardToCopy.siguienteFicha
        rnFichaState = boardToCopy.randomNextFicha.get_state()
        self.randomNextFicha.__setstate__(rnFichaState)
        rnPositionState = boardToCopy.randomNextPosition.get_state()
        self.randomNextPosition.__setstate__(rnPositionState)
        

    def calcularPuntuacion(self):
        """
        Recorre el tablero y consultando la funcion en constantes
        obtiene la puntuacion que vale el tablero
        :return: Valor en int de la puntuacion
        """
        puntuacion = 0
        for i in range(0,4):
            for j in range(0,4):
                puntuacion += int(const.PUNTOS(self.board[i,j]) or 0)
        return puntuacion

    def quedanHuecos(self):
        """
        Esta función comprueba si quedan huecos
        libres en el tablero
        :return: Booleano que es False si no hay huecos
        y True si quedan huecos
        """
        huecos = False
        for i in range(0,4):
            for j in range(0,4):
                if self.board[i,j] == 0:
                    huecos = True
        return huecos

    def unionDisponible(self):
        """
        Es una condicion larga que comprueba si es posible
        de algun modo hacer una union entre 2 fichas
        :return: Booleano que es False si no hay union
        disponible o True si es posible la union
        """
        union = False
        for i in range(0,3):
            for j in range(0,3):
                if ((self.board[i,j] >= 3 and (self.board[i,j] == self.board[i+1,j] or self.board[i,j] == self.board[i,j+1]))
                or ((self.board[i,j] == 1 and self.board[i,j+1] == 2) or (self.board[i,j] == 2 and self.board[i,j+1] == 1) 
                or (self.board[i,j] == 1 and self.board[i+1,j] == 2) or (self.board[i,j] == 2 and self.board[i+1,j] == 1)
                
                or (self.board[3,j] == 1 and self.board[3,j+1]==2) or (self.board[3,j] == 2 and self.board[3,j+1]==1)
                or (self.board[i,3] == 1 and self.board[i+1,3]==2) or (self.board[i,3] == 2 and self.board[i+1,3]==1)
                or (self.board[3,j] >= 3 and (self.board[3,j+1] == self.board[3,j]))
                or (self.board[i,3] >= 3 and (self.board[i+1,3] == self.board[i,3])))):
                    union = True
                
        return union

    def partidaPerdida(self):
        """
        Para dar una partida por perdida comprobamos
        que no haya huecos ni tampoco ninguna union disponible
        :return: Booleano que devuelve False si no se ha perdido
        la partida o True si se da por perdida
        """
        partidaPerdida = False
        if not self.quedanHuecos() and not self.unionDisponible():
            partidaPerdida = True
        return partidaPerdida

    def moverTablero(self, direccionMovimiento):
        """
        Esta funcion es la que define el movimiento y la logica
        del juego, controlando el movimiento de las piezas por el tablero

        :param direccionMovimiento: Se trata de la direccion en la que se
        moverá el tablero
        """
        moved = False
        if direccionMovimiento == const.Movimiento.IZQUIERDA:
            for i in range(0,4):
                for j in range(0,4):
                    # Caso en el que en una fila se encuentre
                    # una union junto al borde
                    if j == 0 and ((self.board[i,j] == self.board[i,j+1] and self.board[i,j] >= 3) or (self.board[i,j] == 1 and self.board[i,j+1] == 2) or (self.board[i,j] == 2 and self.board[i,j+1] == 1)):
                        self.board[i,j] = self.board[i,j] + self.board[i,j+1]
                        self.board[i,j+1] = 0
                        moved = True
                    # Caso en el que una ficha se mueva a un hueco vacio
                    elif j > 0 and self.board[i,j-1] == 0:
                        if (self.board[i,j] != 0):
                            moved = True
                            self.board[i,j-1] = self.board[i,j]
                            self.board[i,j] = 0
                    # Caso en el que una ficha se encuentre otra
                    # a la izquierda y pueda unirse con la de la derecha
                    elif j > 0 and j < 3 and ((self.board[i,j] == self.board[i,j+1] and self.board[i,j-1] != self.board[i,j] and self.board[i,j] >= 3) or (self.board[i,j] == 1 and self.board[i,j+1] == 2) or (self.board[i,j] == 2 and self.board[i,j+1] == 1)):
                        self.board[i,j] = self.board[i,j] + self.board[i,j+1]
                        self.board[i,j+1] = 0
                        moved = True
            if (moved):
                self.desplegarFicha(const.Movimiento.IZQUIERDA,self.siguienteFicha)
        if direccionMovimiento == const.Movimiento.DERECHA:
            
            for i in range(0,4):
                for j in reversed(range(0,4)):
                    if j == 3 and ((self.board[i,j] == self.board[i,j-1] and self.board[i,j] >= 3) or (self.board[i,j] == 1 and self.board[i,j-1] == 2) or (self.board[i,j] == 2 and self.board[i,j-1] == 1)):
                        self.board[i,j] = self.board[i,j] + self.board[i,j-1]
                        self.board[i,j-1] = 0
                        moved = True
                    elif j < 3 and self.board[i,j+1] == 0:
                        if (self.board[i,j] != 0):
                            moved = True
                            self.board[i,j+1] = self.board[i,j]
                            self.board[i,j] = 0
                    elif j > 0 and j < 3 and ((self.board[i,j] == self.board[i,j-1] and self.board[i,j+1] != self.board[i,j] and self.board[i,j] >= 3) or (self.board[i,j] == 1 and self.board[i,j-1] == 2) or (self.board[i,j] == 2 and self.board[i,j-1] == 1)):
                        self.board[i,j] = self.board[i,j] + self.board[i,j-1]
                        self.board[i,j-1] = 0
                        moved = True
            if (moved):
                self.desplegarFicha(const.Movimiento.DERECHA,self.siguienteFicha)
        if direccionMovimiento == const.Movimiento.ARRIBA:
            for i in range(0,4):
                for j in range(0,4):
                    if j == 0 and ((self.board[j,i] == self.board[j+1,i] and self.board[j,i] >= 3) or (self.board[j,i] == 1 and self.board[j+1,i] == 2) or (self.board[j,i] == 2 and self.board[j+1,i] == 1)):
                        self.board[j,i] = self.board[j,i] + self.board[j+1,i]
                        self.board[j+1,i] = 0
                        moved = True
                    elif j > 0 and self.board[j-1,i] == 0:
                        if (self.board[j,i] != 0):
                            moved = True
                            self.board[j-1,i] = self.board[j,i]
                            self.board[j,i] = 0
                    elif j > 0 and j < 3 and ((self.board[j,i] == self.board[j+1,i] and self.board[j-1,i] != self.board[j,i] and self.board[j,i] >= 3) or (self.board[j,i] == 1 and self.board[j+1,i] == 2) or (self.board[j,i] == 2 and self.board[j+1,i] == 1)):
                        self.board[j,i] = self.board[j,i] + self.board[j+1,i]
                        self.board[j+1,i] = 0
                        moved = True
            if (moved):
                self.desplegarFicha(const.Movimiento.ARRIBA,self.siguienteFicha)
        if direccionMovimiento == const.Movimiento.ABAJO:
            for i in range(0,4):
                for j in reversed(range(0,4)):
                    if j == 3 and ((self.board[j,i] == self.board[j-1,i] and self.board[j,i] >= 3) or (self.board[j,i] == 1 and self.board[j-1,i] == 2) or (self.board[j,i] == 2 and self.board[j-1,i] == 1)):
                        self.board[j,i] = self.board[j,i] + self.board[j-1,i]
                        self.board[j-1,i] = 0
                        moved = True
                    elif j < 3 and self.board[j+1,i] == 0:
                        if (self.board[j,i] != 0):
                            moved = True
                            self.board[j+1,i] = self.board[j,i]
                            self.board[j,i] = 0
                    elif j > 0 and j < 3 and ((self.board[j,i] == self.board[j-1,i] and self.board[j+1,i] != self.board[j,i] and self.board[j,i] >= 3) or (self.board[j,i] == 1 and self.board[j-1,i] == 2) or (self.board[j,i] == 2 and self.board[j-1,i] == 1)):
                        self.board[j,i] = self.board[j,i] + self.board[j-1,i]
                        self.board[j-1,i] = 0
                        moved = True
            if (moved): 
                self.desplegarFicha(const.Movimiento.ABAJO,self.siguienteFicha)

    def desplegarFicha(self,direccionUltimoMovimiento,siguienteFicha):
        """
        Esta funcion coloca en el tablero la nueva ficha
        en base al ultimo movimiento y un valor aleatorio
        que decide donde se coloca en la fila deseada

        :param direccionUltimoMovimiento: Un enum declarado en
        const que puede ser IZQUIERDA, DERECHA, ARRIBA o ABAJO
        :param siguienteFicha: se trata del valor guardado de
        la siguiente ficha
        """
        placed = False
        if direccionUltimoMovimiento == const.Movimiento.IZQUIERDA:
                while placed == False and (self.board[0,3] == 0 or self.board[1,3] == 0 or self.board[2,3] == 0 or self.board[3,3] == 0):
                    posRandom = self.randomNextPosition.integers(0,4)
                    if self.board[posRandom,3] == 0:
                        self.board[posRandom,3] = siguienteFicha
                        placed = True
        elif direccionUltimoMovimiento == const.Movimiento.DERECHA:
                while placed == False and (self.board[0,0] == 0 or self.board[1,0] == 0 or self.board[2,0] == 0 or self.board[3,0] == 0):
                    posRandom = self.randomNextPosition.integers(0,4)
                    if self.board[posRandom,0] == 0:
                        self.board[posRandom,0] = siguienteFicha
                        placed = True
        elif direccionUltimoMovimiento == const.Movimiento.ARRIBA:
                while placed == False and (self.board[3,0] == 0 or self.board[3,1] == 0 or self.board[3,2] == 0 or self.board[3,3] == 0):
                    posRandom = self.randomNextPosition.integers(0,4)
                    if self.board[3,posRandom] == 0:
                        self.board[3,posRandom] = siguienteFicha
                        placed = True
        elif direccionUltimoMovimiento == const.Movimiento.ABAJO:
                while placed == False and (self.board[0,0] == 0 or self.board[0,1] == 0 or self.board[0,2] == 0 or self.board[0,3] == 0):
                    posRandom = self.randomNextPosition.integers(0,4)
                    if self.board[0,posRandom] == 0:
                        self.board[0,posRandom] = siguienteFicha
                        placed = True
        if placed: self.siguienteFicha = self.randomSiguienteFicha()

    def randomSiguienteFicha(self):
        """
        Cuando se ejecuta se guarda en "self.siguienteFicha"
        el valor de la siguiente ficha en salir al tablero
        :param seed: Es la semilla del random en caso de haberla
        para generar una secuencia de fichas concreta
        :return: Devuelve el valor de la siguiente ficha
        """
        return self.generarFicha(self.randomNextFicha.integers(0,5))

    def generarFicha(self, value):
        """
        Esta función es util para la construccion inicial del tablero y para el despliegue de fichas durante la partida

        Para el inicio -> El value es un valor entre 0 y 9 (incluidos):
            - Si sale 0 o 1 es un 1 [20%]
            - Si sale 2 o 3 es un 2 [20%]
            - Si sale un 4 es un 3 [10%]
            - Si sale un valor entre 5 y 9 (incluidos) es un 0 (casilla vacía) [50%]


        Para el despliegue -> El value es un valor entre 0 y 4 (incluidos):
            - Si sale 0 o 1 es un 1 [40%]
            - Si sale 2 o 3 es un 2 [40%]
            - Si sale un 4 es un 3 [20%]

        :param value: Un valor entre 0 y 9 para la construccion inicial o entre 0 y 4 para el despliegue de fichas
        :return: El valor en integer de la ficha generada
        """

        # La ficha por defecto está vacia
        ficha = 0
        # Si el numero es 0 o 1
        if value == 0 or value == 1:
            ficha = 1
        elif value == 2 or value == 3:
            ficha = 2
        elif value == 4:
            ficha = 3
        return ficha

    def obtenerEstado(self):
        return self.board