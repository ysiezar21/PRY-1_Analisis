from flask import Flask, render_template, Response, request
import time

app = Flask(__name__)


velocidad_global = 1.0

class Caballo:
    def __init__(self, n, modo):
        self.n = n
        self.matriz = self.crear_matriz(n)
        self.posiciones_jugadas = []
        self.posiciones_disponibles = []
        self.contador = 1
        self.modo = modo
        self.posiciones_validas_iniciales = []

    def obtener_modo(self):
        return self.modo
    def validar_posicion_final_inicial(self):
        if self.posiciones_jugadas[-1] in self.posiciones_validas_iniciales:
            return True
        return False
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

    def colocar_caballo(self, x, y):
        self.matriz[x][y] = self.contador
        self.posiciones_jugadas.append([x, y])
        self.posiciones_validas_iniciales.append(self.validar_posiciones_jugables(self.n, x, y))

    def validar_matriz_completa(self):
        for fila in self.matriz:
            for valor in fila:
                if valor == 0:
                    return False
        
        return True

    def mover_caballo(self):
        if self.posiciones_disponibles[-1] == []:
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
        self.matriz[x][y] = 0
        self.posiciones_jugadas.remove([x, y])
        self.contador -= 1
        self.posiciones_disponibles = self.posiciones_disponibles[:-1]
        self.posiciones_disponibles[-1].remove([x, y])

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


def generar_pasos():
    global velocidad_global  
    n = 5
    modo = True
    juego = Caballo(n, modo)
    juego.colocar_caballo(0, 0)
    juego.posiciones_disponibles.append(juego.validar_posiciones_jugables(n, 0, 0))

    while True:
        if juego.validar_matriz_completa():
            print("Resolvio la matriz")
            
            if juego.obtener_modo():
                print("Modo restringido activado, validando si vuelve al punto inicial")
                if not juego.validar_posicion_final_inicial():
                    print("No se encontro una solucion que vuelva al punto inicial")
                    juego.deshacer_movimiento(juego.posiciones_jugadas[-1][0], juego.posiciones_jugadas[-1][1])
                else:
                    print("Matriz completa y vuelve al punto inicial:")
                    juego.imprimir_matriz()
                    break
            else:
                print("Matriz completa:")
                juego.imprimir_matriz()
                break

        if not juego.posiciones_disponibles or not juego.posiciones_disponibles[-1]:
            if len(juego.posiciones_jugadas) == 1:
                print("No existe una solución posible para este tamaño de tablero")
                break

        if juego.posiciones_disponibles:
            juego.mover_caballo()

            paso_str = ';'.join([','.join(map(str, fila)) for fila in juego.matriz])
            yield f"data:{paso_str}\n\n"

            
            time.sleep(velocidad_global)
        else:
            break


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(generar_pasos(), mimetype="text/event-stream")


@app.route('/set_velocidad', methods=['POST'])
def set_velocidad():
    global velocidad_global
    data = request.get_json()
    velocidad_global = float(data.get("velocidad", 1))
    return {"ok": True, "velocidad": velocidad_global}

if __name__ == '__main__':
    app.run(debug=True)
