"""
Este archivo, contiene el codigo que realiza las tareas pedidas en la parte practica del examen parcial:
Encuentra la ruta mas corta entre dos localidades. Identifica las localidades con conexiones cortas (aquellas
que esta a una distancia menor a 15 km). Verifica la conectividad del grafo (las conexiones entre localidades).
Realiza rutas alternativas entre dos localidades.
"""
"""
La estructura del grafo es  como un diccionario de Python, donde cada localidad es un nodo, y las
conexiones son listas de tuplas con los vecinos y las distancias
"""
import heapq
from collections import defaultdict, deque

# Grafo de localidades
localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)]
}

# Ruta más corta entre dos localidades usando Dijkstra
"""
Utilizo Dijkstra, ya que de esta forma garantizo encontrar la ruta mínima en grafos ponderados 
como es el caso, donde la ponderacion es la distancia entre las localidades (nodos)
"""
def ruta_mas_corta(grafo, origen, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    previos = {nodo: None for nodo in grafo}
    cola = [(0, origen)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual == destino:
            break

        for vecino, peso in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                previos[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    # Reconstruir ruta
    ruta = []
    actual = destino
    while actual:
        ruta.append(actual)
        actual = previos[actual]

    ruta.reverse()
    return ruta, distancias[destino]

# Localidades con todas las conexiones menores a 15 km
"""
Para esto, recorro las conexiones de cada localidad y de esta forma, verifico si cumplen la condición
del ejercicio (distancia menor a 15 km) 
"""
def conexiones_cortas(grafo):
    localidades_cortas = []
    for localidad, conexiones in grafo.items():
        if all(distancia < 15 for _, distancia in conexiones):
            localidades_cortas.append(localidad)
    return localidades_cortas

# Verifica la conectividad del grafo (si es o no conexo)
"""
Para esto utilizo DFS, ya que es sencillo de implementar y consigue verificar si todos los nodos
son alcanzables desde un nodo (localidad) inicial
"""
def es_conexo(grafo):
    visitados = set()

    def dfs(nodo):
        visitados.add(nodo)
        for vecino, _ in grafo[nodo]:
            if vecino not in visitados:
                dfs(vecino)

    # Iniciar DFS desde cualquier nodo
    inicio = next(iter(grafo))
    dfs(inicio)

    # Si hemos visitado todos los nodos, el grafo es conexo
    return len(visitados) == len(grafo)

# Rutas alternativas sin ciclos
"""
Utilizo BFS para generar rutas alternativas, evitando localidades (nodos) ya visitados
"""
def rutas_sin_ciclos(grafo, origen, destino):
    rutas = []
    cola = deque([(origen, [origen])])

    while cola:
        nodo_actual, camino = cola.popleft()

        if nodo_actual == destino:
            rutas.append(camino)
            continue

        for vecino, _ in grafo[nodo_actual]:
            if vecino not in camino:  # Evitar ciclos
                cola.append((vecino, camino + [vecino]))

    return rutas

# Funciones de prueba
# 1. Ruta más corta
ruta, distancia = ruta_mas_corta(localidades, "Madrid", "Getafe")
print(f"Ruta más corta de Madrid a Getafe: {ruta} (Distancia: {distancia} km)")

# 2. Localidades con conexiones cortas
localidades_cortas = conexiones_cortas(localidades)
print(f"Localidades con todas las conexiones menores a 15 km: {localidades_cortas}")

# 3. Verificar conectividad del grafo
es_conexo_res = es_conexo(localidades)
print(f"El grafo es conexo: {'Sí' if es_conexo_res else 'No'}")

# 4. Rutas alternativas sin ciclos
rutas_alternativas = rutas_sin_ciclos(localidades, "Madrid", "Getafe")
print(f"Rutas alternativas de Madrid a Getafe:")
for ruta in rutas_alternativas:
    print(" -> ".join(ruta))

