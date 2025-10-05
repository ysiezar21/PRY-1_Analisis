


class Caballo:
    def __init__(self, n):
        self.n = n
        self.matriz = self.crear_matriz(n)
        self.posiciones_jugadas = []
        self.posiciones_disponibles = []
        self.contador = 1

    def crear_matriz(self, n):
        matriz = []
        for i in range(n):
            fila = []
            for j in range(n):
                fila.append(0)
            matriz.append(fila)
        return matriz

    def imprimir_matriz(self):
        for fila in self.matriz:
            print(fila)
        print()
        cont = 1
        for i in self.posiciones_disponibles:
            print(cont, i)
            cont += 1
        print()

    def colocar_caballo(self, x, y):
        self.matriz[x][y] = self.contador
        self.posiciones_jugadas.append([x, y])
        self.imprimir_matriz()

    def mover_caballo(self):
        if self.posiciones_disponibles[-1] == []:
            print(self.posiciones_jugadas[-1][0],self.posiciones_jugadas[-1][1])
            print (self.contador)
            return self.deshacer_movimiento(self.posiciones_jugadas[-1][0], self.posiciones_jugadas[-1][1])

        x_temporal = self.posiciones_disponibles[-1][0][0]
        y_temporal = self.posiciones_disponibles[-1][0][1]
        self.contador += 1
        self.colocar_caballo(x_temporal, y_temporal)
        

        nuevas_posiciones = self.validar_posiciones_jugables(self.n, x_temporal, y_temporal)
        self.posiciones_disponibles.append(nuevas_posiciones)

    def validar_posicion(self, x, y):
        if [x, y] in self.posiciones_jugadas:
            return False
        return True

    def deshacer_movimiento(self, x, y):
        self.matriz[x][y] = 0 # Eliminar el caballo de la posición actual
        self.posiciones_jugadas.remove([x, y]) # Eliminar la posición de las jugadas
        self.contador -= 1
        
        self.posiciones_disponibles = self.posiciones_disponibles[:-1]
        self.posiciones_disponibles[-1].remove([x, y])
        print("-------------------- Deshacer movimiento --------------------")
        self.imprimir_matriz()
        print("------------------------------------------------------------")
        return self.mover_caballo()

    def validar_posiciones_jugables(self, n, x, y):
        lista_temporal = []

        if x+2 < n and y+1 < n and self.validar_posicion(x+2, y+1):
            lista_temporal.append([x+2, y+1])
        if x+2 < n and y-1 >= 0 and self.validar_posicion(x+2, y-1):
            lista_temporal.append([x+2, y-1])
        if x-2 >= 0 and y+1 < n and self.validar_posicion(x-2, y+1):
            lista_temporal.append([x-2, y+1])
        if x-2 >= 0 and y-1 >= 0 and self.validar_posicion(x-2, y-1):
            lista_temporal.append([x-2, y-1])
        if x+1 < n and y+2 < n and self.validar_posicion(x+1, y+2):
            lista_temporal.append([x+1, y+2])
        if x+1 < n and y-2 >= 0 and self.validar_posicion(x+1, y-2):
            lista_temporal.append([x+1, y-2])
        if x-1 >= 0 and y+2 < n and self.validar_posicion(x-1, y+2):
            lista_temporal.append([x-1, y+2])
        if x-1 >= 0 and y-2 >= 0 and self.validar_posicion(x-1, y-2):
            lista_temporal.append([x-1, y-2])

        return lista_temporal