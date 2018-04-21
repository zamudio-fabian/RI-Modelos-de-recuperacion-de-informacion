# -*- coding: utf-8 -*-

import re
import codecs
import sys
import subprocess
from collections import OrderedDict


def procesar_corpus(path_corpus):
    with codecs.open(path_corpus, mode="r", encoding="utf-8") as corpus:
        texto_corpus = corpus.read()
        lista_docs = re.findall("\n\.W([\s|\S]*?)\n\.X", texto_corpus)
    return lista_docs


def cargar_stopwords(path_stopwords):
    with codecs.open(path_stopwords, mode="r", encoding="utf-8") as stopwords:
        texto_stopwords = stopwords.read()
        texto_stopwords = texto_stopwords.lower()
        texto_stopwords = re.sub("[^a-z]", " ", texto_stopwords)
        lista_stopwords = texto_stopwords.split()
    return lista_stopwords


def procesar_queries(path_queries, lista_stopwords=None):
    with codecs.open(path_queries, mode="r", encoding="utf-8") as queries:
        texto_queries = queries.read()
        lista_queries = re.findall("\n\.W([\s|\S]*?)(?:\n\.I|\n\.B)", texto_queries)
        lista_queries_sin_duplicados = []
    for indice in xrange(len(lista_queries)):
        lista_queries[indice] = lista_queries[indice].lower()
        lista_queries[indice] = re.sub("[^a-z]", " ", lista_queries[indice])
        lista_queries[indice] = lista_queries[indice].split()
        lista_queries[indice] = [t for t in lista_queries[indice] if len(t) > 3]
        if lista_stopwords is not None:
            lista_queries[indice] = [t for t in lista_queries[indice] if t not in lista_stopwords]
        sin_duplicados = list(OrderedDict.fromkeys(lista_queries[indice]))
        lista_queries[indice] = " ".join(lista_queries[indice])
        lista_queries_sin_duplicados.append(" ".join(sin_duplicados))
    return lista_queries, lista_queries_sin_duplicados


def procesar_relevantes(path_relevantes):
    with codecs.open(path_relevantes, mode="r", encoding="utf-8") as relevantes:
        lista_relevantes = []
        for linea in relevantes:
            lista_items = linea.split()
            lista_items[1], lista_items[2] = lista_items[2], lista_items[1]
            lista_items[3] = "1"
            texto_items = " ".join(lista_items)
            lista_relevantes.append(texto_items)
    return lista_relevantes


def guardar_corpus(path_corpus_trec, lista_docs):
    with codecs.open(path_corpus_trec, mode="w", encoding="utf-8") as corpus_trec:
        for indice, documento in enumerate(lista_docs):
            corpus_trec.write("<DOC>\n<DOCNO>" + str(indice+1) + "</DOCNO>")
            corpus_trec.write(documento + "\n</DOC>\n")


def guardar_queries(path_queries_trec, lista_queries):
    with codecs.open(path_queries_trec, mode="w", encoding="utf-8") as queries_trec:
        for indice, query in enumerate(lista_queries):
            queries_trec.write("<TOP>\n<NUM>" + str(indice+1) + "<NUM>\n")
            queries_trec.write("<TITLE>" + query + "\n</TOP>\n")


def guardar_relevantes(path_relevantes_trec, lista_relevantes):
    with codecs.open(path_relevantes_trec, mode="w", encoding="utf-8") as relevantes_trec:
        for linea in lista_relevantes:
            relevantes_trec.write(linea + "\n")


def start(path_cisi, path_stopwords):
    lista_stopwords = [];
    path_corpus = path_cisi+"/CISI.ALL"
    path_queries = path_cisi+"/CISI.QRY"
    path_relevantes = path_cisi+"/CISI.REL"
    path_corpus_trec = "documentos.trec"
    path_queries_trec = "queries.txt"
    path_queries_con_TF_trec = "queries_con_TF.txt"
    path_relevantes_trec = "relevantes.txt"
    lista_docs = procesar_corpus(path_corpus)
    if(path_stopwords != ''): 
        lista_stopwords = cargar_stopwords(path_stopwords)
    lista_queries, lista_queries_sin_duplicados = procesar_queries(path_queries, lista_stopwords)
    lista_relevantes = procesar_relevantes(path_relevantes)
    guardar_corpus(path_corpus_trec, lista_docs)
    guardar_queries(path_queries_con_TF_trec, lista_queries)
    guardar_queries(path_queries_trec, lista_queries_sin_duplicados)
    guardar_relevantes(path_relevantes_trec, lista_relevantes)


if __name__ == "__main__":
    path_vacias = '';
    path_cisi = '';

    if "-h" in sys.argv:
        print "MODO DE USO: python evaluador.py -c <path_directorio_cisi> [-v <path_archivo_stopwords>] "
        sys.exit(0)
    if len(sys.argv) < 3:
        print "ERROR: Debe ingresar el directorio con los archivos cisi. Use -h para más información"
        sys.exit(1)
    if "-c" in sys.argv:
        if sys.argv.index("-c") + 1 == len(sys.argv):
            print "ERROR: Debe ingresar el path del directorio CISI"
            sys.exit(1)
        else:
            path_cisi = sys.argv[sys.argv.index("-c") + 1]
    if "-v" in sys.argv:
        if sys.argv.index("-v") + 1 == len(sys.argv):
            print "ERROR: Debe ingresar el path del archivo de palabras vacias"
            sys.exit(1)
        else:
            path_vacias = sys.argv[sys.argv.index("-v") + 1]


    start(path_cisi, path_vacias)
    subprocess.call("evaluador.sh", shell=True)
