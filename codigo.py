from flask import Flask, render_template, Response, request
import time

app = Flask(__name__)


velocidad_global = 1.0 # Variable global que sera el tiempo que esperara el programa para ejecutar el siguiente paso

# Clase Caballo
class Caballo:
    #Constructor
    def __init__(self, n, modo):
        self.n = n # Orden de la matriz, ejemplo: orden 4 (4x4), orden 7 (7x7)


        self.matriz = self.crear_matriz(n) # Crea la matriz y la guarda como un atributo

        self.posiciones_jugadas = [] # Guarda una lista de pares ordenados de las posiciones jugadas

        
        self.posiciones_disponibles = [] # Guarda una lista de listas de pares ordenados donde la posicion 0 de esta estará vinculada con la posicion 0 de posiciones_jugadas

        self.contador = 1 # Contador de movimientos realizados
        self.modo = modo # True = Cerrado, False = Abierto
        self.posiciones_validas_iniciales = [] # exclusivo para recorrido cerrado, guarda las posiciones disponibles de la casilla inicial
    """
    ***********************************************************************
    Descripcion: Esta funcion devuelve el valor del atributo modo
    ***********************************************************************
    Entrada: Sin entrada
    ***********************************************************************
    Salida: Valor del atributo modo
    ***********************************************************************
    Restricciones: Sin restricciones
    ***********************************************************************
    """
    def obtener_modo(self):
        return self.modo
    
    """
    ***********************************************************************
    Descripcion: Valida que la posicion final se encuentre en las
    posiciones validas para la posicion inicial
    ***********************************************************************
    Entrada: Sin entrada
    ***********************************************************************
    Salida: True en caso de cumplirse la condicion, False si no
    se cumple la condicion
    ***********************************************************************
    Restricciones: Sin restricciones
    ***********************************************************************
    """
    def validar_posicion_final_inicial(self):
        if self.posiciones_jugadas[-1] in self.posiciones_validas_iniciales:
            return True
        return False
    
    """
    ***********************************************************************
    Descripcion: Crea una matriz nxn llena de 0s
    ***********************************************************************
    Entrada: Orden de la matriz (n)
    ***********************************************************************
    Salida: Matriz llena de 0s
    ***********************************************************************
    Restricciones: Sin restricciones
    ***********************************************************************
    """
    def crear_matriz(self, n):
        matriz = []
        for i in range(n):
            fila = []
            for j in range(n):
                fila.append(0)
            matriz.append(fila)
        return matriz


    """
    ***********************************************************************
    Descripcion: Coloca el caballo en la posicion que se desea
    ***********************************************************************
    Entrada: Coordenadas de la casilla en la que desea colocar al caballo
    ***********************************************************************
    Salida: Sin salida
    ***********************************************************************
    Restricciones: Sin restricciones
    ***********************************************************************
    """
    def colocar_caballo(self, x, y):
        self.matriz[x][y] = self.contador
        self.posiciones_jugadas.append([x, y])
        if len(self.posiciones_jugadas) <= 1:
            self.posiciones_validas_iniciales = self.validar_posiciones_jugables(self.n, x, y)

    
    """
    ***********************************************************************
    Descripcion: Valida si la matriz esta completa
    ***********************************************************************
    Entrada: Sin entrada
    ***********************************************************************
    Salida: True si esta vacia, False si aun tiene por lo menos
    un 0
    ***********************************************************************
    Restricciones: Sin restricciones
    ***********************************************************************
    """

    def validar_matriz_completa(self):
        for fila in self.matriz:
            for valor in fila:
                if valor == 0:
                    return False
        
        return True
    """
    ***********************************************************************
    Descripcion: Mueve el caballo a alguna casilla que tenga
    disponible, de no ser el caso, se devuelve al paso anterior
    ***********************************************************************
    Entrada: Sin entrada
    ***********************************************************************
    Salida: deshacer_movimiento() o actualiza los atributos
    ***********************************************************************
    Restricciones: Sin restricciones
    ***********************************************************************
    """
    def mover_caballo(self):
        if self.posiciones_disponibles[-1] == []:
            return self.deshacer_movimiento(self.posiciones_jugadas[-1][0], self.posiciones_jugadas[-1][1])

        x_temporal = self.posiciones_disponibles[-1][0][0]
        y_temporal = self.posiciones_disponibles[-1][0][1]
        self.contador += 1
        self.colocar_caballo(x_temporal, y_temporal)
        nuevas_posiciones = self.validar_posiciones_jugables(self.n, x_temporal, y_temporal)
        self.posiciones_disponibles.append(nuevas_posiciones)

    """
    ***********************************************************************
    Descripcion: Valida si la posicion es jugable o no
    ***********************************************************************
    Entrada: Coordenadas de la posicion que se desea jugar
    ***********************************************************************
    Salida: True si es una posicion valida, False si no
    ***********************************************************************
    Restricciones: la posicion debe de estar dentro de 
    las dimensiones de la matriz
    ***********************************************************************
    """
    def validar_posicion(self, x, y):
        if [x, y] in self.posiciones_jugadas:
            return False
        return True
    """
    ***********************************************************************
    Descripcion: Cuando ya probo todas las posibles jugadas de una casilla
    y no encontro ninguna valida, se devuelve a la casilla anterior para
    intentar utilizar otra casilla
    ***********************************************************************
    Entrada: Posicion actual en fila y en columna
    ***********************************************************************
    Salida: Sin salidas
    ***********************************************************************
    Restricciones: Sin restricciones
    ***********************************************************************
    """
    def deshacer_movimiento(self, x, y):
        self.matriz[x][y] = 0
        self.posiciones_jugadas.remove([x, y])
        self.contador -= 1
        self.posiciones_disponibles = self.posiciones_disponibles[:-1]
        self.posiciones_disponibles[-1].remove([x, y])
    """
    ***********************************************************************
    Descripcion: Valida que posiciones pueden ser utilizadas por el
    caballo en un punto en especifico
    ***********************************************************************
    Entrada: tamaño de la matriz, posicion en fila y posicion en columna
    ***********************************************************************
    Salida: Lista con todas las posiciones validas para ser jugadas
    ***********************************************************************
    Restricciones: n debe de tener un rango de 4-7, x y y deben de ser
    numeros enteros entre 0 y n-1
    ***********************************************************************
    """
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
"""
***********************************************************************
Descripcion: Funcion principal, genera el juego
***********************************************************************
Entrada: tamaño de la matriz, el modo de juego, posicion inicial en fila
y posicion inicial en columna del caballo
***********************************************************************
Salida: Muestra en la interfaz el juego
***********************************************************************
Restricciones: el tamaño de la matriz debe de ser de un rango entre 4-7(n-1),
el modo debe de ser un valor booleano, la posicion inicial de fila y
columna del caballo debe de ser un valor entero positivo entre 0 y n-1
***********************************************************************
"""
def generar_pasos(n, modo, f, c):
    global velocidad_global # velocidad

    # Crear juego
    juego = Caballo(n, modo)
    juego.colocar_caballo(f, c)
    juego.posiciones_disponibles.append(juego.validar_posiciones_jugables(n, f, c))

    # Inicia el juego
    while True:
        if juego.validar_matriz_completa(): # Si la matriz esta completa, entra al bloque
            if juego.obtener_modo(): # Si el modo es cerrado, entra al bloque
                if not juego.validar_posicion_final_inicial(): # Valida si la posicion final no es valida
                    juego.deshacer_movimiento(juego.posiciones_jugadas[-1][0], juego.posiciones_jugadas[-1][1]) # Deshace el ultimo movimiento
                else: 
                    break # Si la posicion final es valida, termina el juego
            else:
                break # Si el modo es abierto y la matriz esta completa, termina el juego

        if not juego.posiciones_disponibles or not juego.posiciones_disponibles[-1]: # Si no hay posiciones disponibles, entra al bloque
            if len(juego.posiciones_jugadas) == 1: # Si solo queda la posicion inicial, termina el juego
                break

        if juego.posiciones_disponibles: # Si hay posiciones disponibles, entra al bloque
            juego.mover_caballo() # Mueve el caballo a una posicion valida

            paso_str = ';'.join([','.join(map(str, fila)) for fila in juego.matriz]) # Convierte la matriz en un string para enviarlo a la interfaz
            yield f"data:{paso_str}\n\n"
            time.sleep(velocidad_global)
        else:
            break # Si por alguna razon no entra en ningun bloque, termina el juego


"""
***********************************************************************
Descripcion: Carga la interfaz principal
***********************************************************************
Entrada: Sin entrada
***********************************************************************
Salida: Renderiza el archivo index html
***********************************************************************
Restricciones: Debe existir un archivo index html en la carpeta templates
***********************************************************************
"""
@app.route('/')
def index():
    return render_template('index.html')


"""
***********************************************************************
Descripcion: Transmite los datos del recorrido del caballo paso a paso
***********************************************************************
Entrada: Parametros de la solicitud n modo f c
***********************************************************************
Salida: Flujo de datos tipo text event stream
***********************************************************************
Restricciones: Los parametros deben ser validos y estar dentro del rango
***********************************************************************
"""
@app.route('/stream')
def stream():
    n = request.args.get('n', default=4, type=int)
    modo = request.args.get('modo', default='false', type=str).lower() == 'true'
    f = request.args.get('f', default=1, type=int)
    c = request.args.get('c', default=1, type=int)

    return Response(generar_pasos(n, modo, f, c), mimetype="text/event-stream")

"""
***********************************************************************
Descripcion: Ajusta la velocidad global de ejecucion del recorrido
***********************************************************************
Entrada: Recibe un JSON con el valor de velocidad
***********************************************************************
Salida: Retorna un JSON confirmando la velocidad establecida
***********************************************************************
Restricciones: La velocidad debe ser un valor numerico positivo
***********************************************************************
"""
@app.route('/set_velocidad', methods=['POST'])
def set_velocidad():
    global velocidad_global
    data = request.get_json()
    velocidad_global = float(data.get("velocidad", 1))
    return {"ok": True, "velocidad": velocidad_global}
"""
***********************************************************************
Descripcion: Punto de entrada principal del programa
***********************************************************************
Entrada: Sin entrada
***********************************************************************
Salida: Ejecuta el servidor flask en modo debug
***********************************************************************
Restricciones: Flask debe estar instalado correctamente
***********************************************************************
"""
if __name__ == '__main__':
    app.run(debug=True)
