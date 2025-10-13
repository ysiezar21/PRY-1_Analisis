from flask import Flask, render_template, Response, request
import time, json

app = Flask(__name__)

# Variable global para la velocidad (en segundos por paso)
velocidad_global = 1.0


class Caballo:
    def __init__(self, n):
        self.n = n
        self.matriz = [[0 for _ in range(n)] for _ in range(n)]
        self.movimientos_posibles = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        self.movimientos = 0
        self.retrocesos = 0

    # Verificar si la posición está dentro del tablero y libre
    def es_valido(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n and self.matriz[x][y] == 0

    # Función recursiva principal con backtracking
    def resolver(self, x, y, contador):
        # Si ya se visitaron todas las casillas, se encontró una solución
        if contador > self.n * self.n:
            return True

        # Intenta cada movimiento posible del caballo
        for mov_x, mov_y in self.movimientos_posibles:
            nuevo_x, nuevo_y = x + mov_x, y + mov_y
            if self.es_valido(nuevo_x, nuevo_y):
                self.matriz[nuevo_x][nuevo_y] = contador
                self.movimientos += 1
                yield self.crear_estado("avance")  # Enviar paso "avance"
                time.sleep(velocidad_global)

                # Llamada recursiva
                yield from self.resolver(nuevo_x, nuevo_y, contador + 1)

                # Si no conduce a una solución = retrocede
                if any(0 in fila for fila in self.matriz):
                    self.matriz[nuevo_x][nuevo_y] = 0
                    self.retrocesos += 1
                    yield self.crear_estado("retroceso")
                    time.sleep(velocidad_global)

        # Si no se encuentra un camino válido, retorna
        return

    # Crear un diccionario con el estado actual del tablero
    def crear_estado(self, tipo):
        return {
            "matriz": self.matriz,
            "tipo": tipo,
            "movimientos": self.movimientos,
            "retrocesos": self.retrocesos
        }


# Generador que emite los pasos del recorrido del caballo
def generar_pasos(n):
    global velocidad_global
    caballo = Caballo(n)

    # Punto inicial
    caballo.matriz[0][0] = 1

    # Mide el tiempo de ejecución
    inicio = time.time()

    # Genera pasos mediante backtracking
    for estado in caballo.resolver(0, 0, 2):
        yield f"data:{json.dumps(estado)}\n\n"

    # Enviar mensaje final con estadísticas
    fin = time.time()
    total = {
        "matriz": caballo.matriz,
        "tipo": "final",
        "movimientos": caballo.movimientos,
        "retrocesos": caballo.retrocesos,
        "tiempo": round(fin - inicio, 2)
    }
    yield f"data:{json.dumps(total)}\n\n"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stream')
def stream():
    n = int(request.args.get("n", 5))  # Valor por defecto: tablero 5x5
    return Response(generar_pasos(n), mimetype="text/event-stream")


@app.route('/set_velocidad', methods=['POST'])
def set_velocidad():
    global velocidad_global
    data = request.get_json()
    velocidad_global = float(data.get("velocidad", 1))
    return {"ok": True, "velocidad": velocidad_global}


if __name__ == '__main__':
    app.run(debug=True)
