# coding: utf-8
"""
Camino mas corto entre 2 puntos de un grafo ponderado
utilizando el algoritmo de Dijkstra.

Matematica Discreta - TP Anual
Nahuel Lattessi
2014
"""

import sys


#--- FUNCIONES ---#
def menorNodo(distancias, no_analizados):
	"""Devuelve el nodo de 'no_analizados' de menor distancia"""

	# Funcion auxiliar necesaria para devolver
	# el nodo minimo en el siguiente paso.
	def valor_distancia(nodo):
		return distancias[nodo]

	nodo = min(no_analizados, key=valor_distancia)
	return nodo

def camino(nodos_previos, a, z):
	"""Devuelve el camino mas corto al nodo 'z'"""
	
	salida = []
	nodo = z
	while nodo != a:
		salida.append(nodo)
		nodo = nodos_previos[nodo]
	salida.append(a)
	salida.reverse()
	return salida


def leer_archivo_grafo(archivo):
	"""Lee el grafo desde un archivo de texto"""
	import ast

	with open(archivo, 'r') as f:
		s = f.read()
		grafo = ast.literal_eval(s)

	return grafo


def main(archivo, a, z):
	"""Punto de entrada principal del script."""

	grafo = leer_archivo_grafo(archivo)

	# Da error si no existen 'a' o 'z' en el grafo.
	assert a in grafo
	assert z in grafo

	# Guardo un valor que es la suma de todas las distancias
	# para usar como infinito
	inf = 0
	for n in grafo:
		for v, w in grafo[n]:
			inf += w

	# Inicializo estructuras auxiliares:
	# 	distancias = Diccionario que guarda las distancias del nodo inicial a cada nodo del grafo. Inicializo seteando a cada nodo su distancia en infinito.
	#	no_analizados = Lista que guarda los nodos NO analizados aun. Inicializo con todos los nodos del grafo.
	#	nodos_previos = Diccionario que guarda el nodo previo (de menor distancia) de cada nodo analizado. Se inicializa vacio.
	distancias = dict([(n, inf) for n in grafo])
	no_analizados = set([n for n in grafo])
	nodos_previos = {}

	distancias[a] = 0 # Seteo en 0 la distancia del nodo inicial a si mismo

	# Mientras haya nodos sin analizar:
	# 	Analizo el primer nodo de ellos que tenga la menor distancia
	# 	y lo descarto de de la lista de nodos no analizados.
	while len(no_analizados): # Mientras haya nodos sin analizar
		nodoActual = menorNodo(distancias, no_analizados)
		no_analizados.discard(nodoActual)
		
		# Por cada nodo adyacente, compruebo si su distancia es menor a la guardada.
		# De ser asi, actualizo las distancias y lo seteo como nodo previo.
		for nodoAdyacente, distancia in grafo[nodoActual]:
			if nodoAdyacente in no_analizados:
				if distancias[nodoActual] + distancia < distancias[nodoAdyacente]:
					distancias[nodoAdyacente] = distancias[nodoActual] + distancia
					nodos_previos[nodoAdyacente] = nodoActual


	print "Distancias mas cortas desde el nodo {}: {}".format(a, distancias)
	print "Camino mas corto entre {} y {}: {}".format(a, z, camino(nodos_previos, a, z))


if __name__ == '__main__':
	sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))