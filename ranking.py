#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import re
import codecs
from nltk.stem import *
import math

MIN_LENGTH = 4
MAX_LENGTH = 32

def email(data):
	match = re.search("^[a-z0-9\-\.]+@[a-z0-9\-]+\.[a-z]+$", data)

	return match!=None

def abrev(data):
	match = re.search("^([A-Z][a-z]*\.)+$", data)
	return match!=None

def htmlentity(data):
	match = re.search("^&.+;$", data)
	return match!=None

def comentario_html(data):
	match = re.search("^<\!--.*-->", data)
	return match!=None

def translate(to_translate):
	to_translate = to_translate.decode('utf-8', errors='ignore')
	tabin = [u'áéíóúñ', u'àèìòùñ', u'äëïöüñ', u'âêîôûñ']
	tabout = u'aeioun'
	translate_table = {}
	for i in xrange(0, len(tabin)):
		translate_table.update(dict(zip([ord(char) for char in tabin[i]], tabout)))
	
	return to_translate.translate(translate_table).encode('utf-8')
	

def tokenizar(line):
	global stemmer
	return [word for word in line.split() if ((len(word) >= MIN_LENGTH) and (len(word) <= MAX_LENGTH))]

def sacar_palabras_vacias(lista_tokens, lista_vacias):
	return [token for token in lista_tokens if not token in lista_vacias]

def leer_palabras_vacias(file):
	vacias = []
	with open(file, 'r') as infile:
		for line in infile:
			for word in line.split():
				vacias.append(word)
	return vacias

def extraer_terminos(tokens):
	global stemmer
	return [stemmer.stem(termino.lower()) for termino in tokens if (not htmlentity(termino)) ]

def filtrar_documento(documento):
	documento = re.sub("<\!\-([^\-]|[\r\n]|(\-+([^\->]|[\r\n])))*\-+>", '', documento)
	documento = documento.replace('\'', '')
	documento = documento.replace('-', '')
	documento = re.sub("[^a-zA-Z0-9áéíóúäëïöüâêîôûàèìòùñ]", ' ', documento)

	return documento

def procesar_terminos(terminos_archivos):
	terminos = {}
	total = 0
	for archivo in terminos_archivos:
		max_tf = 0
		for termino in terminos_archivos[archivo]['terminos']:
			tf = terminos_archivos[archivo]['terminos'][termino]
			total += tf
			if(not termino in terminos):
				terminos[termino] = {}
			terminos[termino]['cantidad'] = terminos[termino].get('cantidad', 0) + tf
			if(not 'df' in terminos[termino]):
				terminos[termino]['df'] = set([])
			terminos[termino]['df'].add(archivo)
			if(tf > max_tf):
				max_tf = tf
		terminos_archivos[archivo]['max_tf'] = max_tf

	for termino in terminos:
		terminos[termino]['freq'] = terminos[termino]['cantidad']/float(total)
		terminos[termino]['df'] = len(terminos[termino]['df'])

	return terminos

def calcular_tfs(terminos):
	ret = {}
	for termino in terminos:
		ret[termino] = ret.get(termino, 0) + 1
	return ret

def calcular_normas(terminos_archivos, terminos):
	for archivo in terminos_archivos:
		s = 0
		for termino in terminos_archivos[archivo]['terminos']:
			tf = float(terminos_archivos[archivo]['terminos'][termino])
			tf /= max(terminos_archivos[archivo]['terminos'].values())
			idf = calcular_idf(terminos_archivos, terminos, termino)
			tfidf = tf*idf
			s += tfidf**2

		terminos_archivos[archivo]['norma'] = math.sqrt(s)

def calcular_idf(terminos_archivos, terminos, termino):
	return math.log(float(len(terminos_archivos))/terminos[termino]['df'], 2)

def recuperar_archivos_opt_a(terminos, query, terminos_archivos):
	ret = {}
	for archivo in terminos_archivos:
		numerador = 0
		denominador = 0
		for termino in query:
			if(not termino in terminos):
				continue
			if(len(terminos_archivos[archivo]['terminos']) == 0):
				continue

			qtf = float(query.get(termino, 0)*0.5)
			qtf /= max(query.values())
			qtf += 0.5

			dtf = float(terminos_archivos[archivo]['terminos'].get(termino, 0))
			dtf /= max(terminos_archivos[archivo]['terminos'].values())

			idf = calcular_idf(terminos_archivos, terminos, termino)
			dtfidf = dtf*idf
			qtfidf = qtf*idf

			numerador += qtfidf * dtfidf
			denominador += qtfidf**2

		denominador = math.sqrt(denominador) * terminos_archivos[archivo]['norma']
		ret[archivo] = numerador/denominador if denominador != 0 else 0
	return ret

def recuperar_archivos_opt_b(terminos, query, terminos_archivos):
	ret = {}
	for archivo in terminos_archivos:
		numerador = 0
		denominador = 0
		for termino in query:
			if(not termino in terminos):
				continue
			if(len(terminos_archivos[archivo]['terminos']) == 0):
				continue

			qtf = float(query.get(termino, 0)*0.5)
			qtf /= max(query.values())
			qtf += 0.5

			dtf = float(terminos_archivos[archivo]['terminos'].get(termino, 0))
			dtf /= max(terminos_archivos[archivo]['terminos'].values())

			idf = 1
			dtfidf = dtf*idf
			qtfidf = math.log(1 + float(len(terminos_archivos))/terminos[termino]['df'],2) * idf

			numerador += qtfidf * dtfidf
			denominador += qtfidf**2

		denominador = math.sqrt(denominador) * terminos_archivos[archivo]['norma']
		ret[archivo] = numerador/denominador if denominador != 0 else 0
	return ret

def recuperar_archivos_opt_c(terminos, query, terminos_archivos):
	ret = {}
	for archivo in terminos_archivos:
		numerador = 0
		denominador = 0
		for termino in query:
			if(not termino in terminos):
				continue
			if(len(terminos_archivos[archivo]['terminos']) == 0):
				continue

			qtf = float(query.get(termino, 0)*0.5)
			qtf /= max(query.values())
			qtf += 0.5

			dtf = float(terminos_archivos[archivo]['terminos'].get(termino, 0))
			dtf /= max(terminos_archivos[archivo]['terminos'].values())

			idf = calcular_idf(terminos_archivos, terminos, termino)
			dtfidf = dtf*idf
			qtfidf = math.log(1 + query.get(termino, 0),2) * idf

			numerador += qtfidf * dtfidf
			denominador += qtfidf**2

		denominador = math.sqrt(denominador) * terminos_archivos[archivo]['norma']
		ret[archivo] = numerador/denominador if denominador != 0 else 0
	return ret

if __name__ == "__main__":
	directory = sys.argv[1]
	vacias = []
	typeTFIDF = 'A'
	if "-h" in sys.argv:
		print "MODO DE USO: python ranking.py <PATH/TO/CORPUS> [-v <PATH/TO/PALABRAS/VACIAS>] [-t <A|B|C>]"
		sys.exit(0)
	if len(sys.argv) < 2:
		print "ERROR: Debe ingresar el directorio con los archivos a analizar"
		sys.exit(1)
	if "-v" in sys.argv:
		if sys.argv.index("-v") + 1 == len(sys.argv):
			print "ERROR: Debe ingresar el nombre del archivo con palabras vacias"
			sys.exit(1)
		else:
			vacias = leer_palabras_vacias(sys.argv[sys.argv.index("-v") + 1])
	if "-t" in sys.argv:
		if sys.argv.index("-t") + 1 == len(sys.argv):
			print "ERROR: Debe ingresar el tipo de ponderación que desea utilizar en la query"
			sys.exit(1)
		else:
			typeTFIDF = sys.argv[sys.argv.index("-t") + 1]

	global stemmer

	stemmer = SnowballStemmer("spanish")

	terminos_archivos = {}
	docid=0
	for archivo in sorted(os.listdir(directory)):
		print 'archivo', directory + archivo
		with codecs.open(directory + archivo, errors='ignore') as infile:
			documento = filtrar_documento(infile.read())
			tokens_file = tokenizar(translate(documento))
			terminos_file = calcular_tfs(extraer_terminos(sacar_palabras_vacias(tokens_file, vacias)))
			terminos_archivos[archivo] = {'terminos':terminos_file, 'docid': docid}
			docid += 1

	terminos = procesar_terminos(terminos_archivos)
	calcular_normas(terminos_archivos, terminos)

	query = raw_input('Ingrese un query(\'\' para salir): ')
	while (query != ''):
		tokens_query = tokenizar(translate(filtrar_documento(query)))
		terminos_query = calcular_tfs(extraer_terminos(sacar_palabras_vacias(tokens_query, vacias)))
		if (typeTFIDF == 'C') :
			ret = recuperar_archivos_opt_c(terminos, terminos_query, terminos_archivos)
		elif (typeTFIDF == 'B') :
			ret = recuperar_archivos_opt_b(terminos, terminos_query, terminos_archivos)
		else :
			ret = recuperar_archivos_opt_a(terminos, terminos_query, terminos_archivos)
		ranking = sorted(ret.items(), key=lambda x: x[1], reverse=True)
		
		for r in xrange(0, min(15, len(ranking))):
			if(ranking[r][1] < 0.02):
				continue
			print (r+1),'-', terminos_archivos[ranking[r][0]]['docid'], ranking[r]
		query = raw_input('Ingrese un query(\'\' para salir): ')
	
	sys.exit(0)
