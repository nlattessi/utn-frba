# coding: utf-8
"""
Analizador de poroposiciones.

Matematica Discreta - TP Anual
Nahuel Lattessi
2014
"""

# http://www.portalhacker.net/b64/programa-que-construye-tablas-verdad-proposiciones-logicas/109660/

import sys
import math
import pdb

CONECTORES = ['!', '&', '|', ':', '=', '(', ')']

#--- FUNCIONES ---#
def get_variables(proposiciones, vars):
	"""Guarda en el segundo argumento las variables unicas 
	del conjunto de proposiciones y devuelve la cantidad de ellas.
	"""
	nvars = 0
	for i in range(0, len(proposiciones)):
		if proposiciones[i] not in CONECTORES:
			existe = False
			for j in range(0, len(vars)):
				if proposiciones[i] == vars[j]:
					existe = True
					break
			if not existe:
				vars[nvars] = proposiciones[i]
				nvars += 1

	return nvars

def get_precedencia(c):
	"""Devuelve la precedencia de un conector."""
	if c == '!':
		return 2
	elif c == '&':
		return 3
	elif c == '|':
		return 3
	elif c == ':':
		return 4
	elif c == '=':
		return 5
	else:
		return 1

def max_precedencia(proposiciones, inicio, fin):
	"""Determina la maxima precedencia entre inicio y fin
	de un conjunto de proposiciones.
	"""
	npar = 0
	precedencia = 0
	anidado = 0
	index = 0
	primero = True
	
	for i in range(inicio, fin):
		if proposiciones[i] == '(':
			npar += 1
		elif proposiciones[i] == ')':
			npar -= 1
		else:
			p = get_precedencia(proposiciones[i])
			if primero:
				anidado = npar
				precedencia = p
				index = i
				primero = False
				continue
			if npar < anidado:
				anidado = npar
				precedencia = p
				index = i
			elif anidado == npar:
				if p > precedencia:
					precedencia = p
					index = i
				elif p == precedencia:
					if proposiciones[index] != proposiciones[i]:
						return -1
					if proposiciones[index] != '!':
						index = i

	return index				


def evaluar_proposicion(prop, vals, vars, resp, inicio, fin):
	"""Evalua entre inicio y fin las proposiciones dadas guardando en
	resp el valor de verdad de cada variable o conector. Esto se
	realiza de forma recursiva.
	"""
	index = max_precedencia(prop, inicio, fin)
	
	if prop[index] == '!':
		b = not evaluar_proposicion(prop, vals, vars, resp, index+1, fin)
		if b:
			resp[index] = 'V'
		else:
			resp[index] = 'F'
		return b
	
	elif prop[index] == '&' or prop[index] == '|' or prop[index] == ':' or prop[index] == '=':
		# Recursividad a izquierda del indice
		p = evaluar_proposicion(prop, vals, vars, resp, inicio, index)
		# Recursividad a derecha del indice
		q = evaluar_proposicion(prop, vals, vars, resp, index+1, fin)
		if prop[index] == '&':
			r = p and q
		elif prop[index] == '|':
			r = p or q
		elif prop[index] == ':':
			r = not p or q
		elif prop[index] == '=':
			r = (not p or q) and (not q or p)
		if r:
			resp[index] = 'V'
		else:
			resp[index] = 'F'
		return r

	else:
		i = 0
		while vars[i] != '\0':
			if prop[index] == vars[i]:
				if vals[i]:
					resp[index] = 'V'
				else:
					resp[index] = 'F'				
				return vals[i]
			i += 1


def main(entrada):
	"""Punto de entrada principal del script."""
	proposiciones = entrada.replace(" ", "")
	n = len(proposiciones)
	vars = ['\0' for x in range(0, n)]
	nvars = get_variables(proposiciones, vars)
	reps = int(math.pow(2, nvars))
	vals = [False for x in range(0, n)]
	resp = [' ' for x in range(0, n)]
	
	maximo_precedente = max_precedencia(proposiciones, 0, n)
	conclusion = []
	
	# Imprimo variables
	for i in range(0, nvars):
		print vars[i],
	print "| ",
	
	# Imprimo proposiciones
	for i in range(0, n):
		print proposiciones[i],
	print '\n\n'
	
	# Imprimo tabla de verdad
	for i in range(0, reps):
		for j in range(0, nvars):
			if i % int(math.pow(2, nvars-j-1)) == 0:
				vals[j] = not vals[j]
			if vals[j]:
				print "V",
			else:
				print "F",
		print "| ",
		evaluar_proposicion(proposiciones, vals, vars, resp, 0, n)
		for j in range(0, n):
			print resp[j],
			if j == maximo_precedente:
				conclusion.append(resp[j])
		print '\n'
	
	print
	if 'V' in conclusion:
		if 'F' in conclusion:
			print "Es contingencia"
		else:
			print "Es tautologia"
	else:
		print "Es contradicion"


if __name__ == '__main__':
	sys.exit(main(sys.argv[1]))