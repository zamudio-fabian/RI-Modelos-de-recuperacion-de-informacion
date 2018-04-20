# -*- coding: utf-8 -*-
import codecs
import subprocess
import sys

def start():
    maxCantQueries = 5
    max_puestos = 50
    # Hitos para calcular las correlaciones de los rankings
    hitos = [10, 25, 50]
    correlaciones = []

    # Obtenemos los rankings y normalizamos ambos
    rankingTfIdf = getRankings("TF_IDF_1.res", maxCantQueries, max_puestos)
    rankingBm25 = getRankings("BM25b0.75_0.res", maxCantQueries, max_puestos)
    # Por cada hito recorremos los ranking y por cada query obtenemos la correlación para ese HITO
    for x in xrange(maxCantQueries):
        correlacionesSub = []
        for hito in hitos:
            resp = correlacionAt(rankingTfIdf[x], rankingBm25[x], hito)
            resp.append(x+1)
            correlacionesSub.append(list(resp))
        correlaciones.append(list(correlacionesSub))
    
    # Almacenamos las correlaciones
    with codecs.open("correlaciones.txt", mode="w", encoding="utf-8") as archivo:
        for queryNro,resp in enumerate(correlaciones):
            archivo.write("QUERY NRO "+str(queryNro+1)+"\n")
            archivo.write("".ljust(24,"-")+"\n\n")
            for indexHito, hito in enumerate(hitos):
                archivo.write("".ljust(50,"=")+"\n")
                archivo.write("CANTIDAD DE RESPUESTAS = "+str(hito)+"\n")
                archivo.write(u"COEFICIENTE DE CORRELACIÓN: " + str(resp[indexHito][2]) + "\n")
                archivo.write("CANTIDAD DE RESPUESTAS EFECTIVAS = "+str(len(resp[indexHito][0]))+"\n")
                archivo.write("".ljust(50,"=")+"\n\n")
                archivo.write("Ranking".ljust(8)+"TF-IDF".ljust(8)+"BM25".ljust(8)+"\n")
                for rank in xrange(len(resp[indexHito][0])):
                    archivo.write(str(rank + 1).ljust(8) + resp[indexHito][0][rank].ljust(8)  + resp[indexHito][1][rank].ljust(8) + "\n")
                archivo.write("\n\n")

# Metodo para obtener la correlación de un hito en particular entre dos ranking.
# Hay que normalizar los ranking
def correlacionAt(rankingA,rankingB,hito):
    # Obtenemos los X elementos dados por el hito
    rankingAAux = rankingA[:hito]
    rankingBAux = rankingB[:hito]
    # En el caso de que un Doc este en un ranking pero no en el otro hay que agregarlo
    for idDoc in rankingAAux:
        if idDoc not in rankingBAux:
            rankingBAux.append(idDoc)
    for idDoc in rankingBAux:
        if idDoc not in rankingAAux:
            rankingAAux.append(idDoc)
    # Por cada idDoc sumo al total la distancia elevada al cuadrado
    diferencias = 0
    for documento in rankingAAux:
        indexRankingA = rankingAAux.index(documento) + 1
        indexRankingB = rankingBAux.index(documento) + 1
        diferencias += pow(indexRankingA - indexRankingB, 2)
    # Sacamos la correlación mediante el Coeficiente de Correlación de Spearman
    # https://es.wikipedia.org/wiki/Coeficiente_de_correlaci%C3%B3n_de_Spearman
    cantidadElementos = len(rankingAAux)
    divisor = float( cantidadElementos * (pow(cantidadElementos, 2) - 1))
    correlacion = (1 - ((6 * diferencias) / float(divisor)))
    return  [rankingAAux,rankingBAux,correlacion]

# Genera la lista de ranking
def getRankings(ranking_file, maxCantQueries, max_puestos):
    idQueryActual = 1
    rankingAux = []
    rankings = []
    # Recorremos el archivo .res - cada linea es una posición en el ranking generado por Terrier
    with codecs.open(ranking_file, mode="r", encoding="utf-8") as archivo:
        for linea in archivo:
            detalle = linea.split()
            idQuery = detalle[0]
            idDoc = detalle[2]
            if idQuery == str(idQueryActual):
                rankingAux.append(idDoc)
            if len(rankingAux) >= max_puestos:
                rankings.append(list(rankingAux))
                idQueryActual += 1
                rankingAux = []
            if idQueryActual > maxCantQueries:
                break
    return rankings

if __name__ == "__main__":
    if "-h" in sys.argv:
        print "MODO DE USO: correlacion.py -c <path_directorio_archivos> -q <path_archivo_queries>]"
        sys.exit(0)
    if len(sys.argv) < 5:
        print "ERROR: Debe ingresar el directorio con los archivos a analizar y el archivo con las queries. Use -h para más información"
        sys.exit(1)
    if "-c" in sys.argv:
        if sys.argv.index("-c") + 1 == len(sys.argv):
            print "ERROR: Debe ingresar el nombre del archivo con palabras vacias"
            sys.exit(1)
        else:
            path_corpus = sys.argv[sys.argv.index("-c") + 1]
    if "-q" in sys.argv:
        if sys.argv.index("-q") + 1 == len(sys.argv):
            print "ERROR: Debe ingresar el path del archivo con las consultas"
            sys.exit(1)
        else:
            file_queries = sys.argv[sys.argv.index("-q") + 1]

    subprocess.call("preprocesador.sh "+path_corpus+" "+file_queries, shell=True)
    start()



