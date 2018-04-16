# -*- coding: utf-8 -*-
import codecs

def start():
    maxCantQueries = 5
    max_puestos = 50
    hitos = [10, 25, 50]
    correlaciones = []

    rankingTfIdf = getRankings("TF_IDF_1.res", maxCantQueries, max_puestos)
    rankingBm25 = getRankings("BM25b0.75_0.res", maxCantQueries, max_puestos)
    # Por cada hito recorremos los ranking y por cada query obtenemos la correlación para ese HITO
    for x in xrange(maxCantQueries):
        correlacionesSub = []
        for hito in hitos:
            resp = correlacionesAt(rankingTfIdf[x], rankingBm25[x], hito)
            resp.append(x+1)
            correlacionesSub.append(list(resp))
        correlaciones.append(list(correlacionesSub))
    
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

# Metodo para obtner la correlación de un hito en particular entre dos ranking.
# Hay que normalizar los ranking
def correlacionesAt(rankingA,rankingB,hito):
    # Normalizamos
    rankingAAux = rankingA[:hito]
    rankingBAux = rankingB[:hito]
    for idDoc in rankingAAux:
        if idDoc not in rankingBAux:
            rankingBAux.append(idDoc)
    for idDoc in rankingBAux:
        if idDoc not in rankingAAux:
            rankingAAux.append(idDoc)
    total = 0
    # Por cada idDoc sumo al total la distancia elevada al cuadrado
    for documento in rankingAAux:
        indexRankingA = rankingAAux.index(documento) + 1
        indexRankingB = rankingBAux.index(documento) + 1
        total += pow(indexRankingA - indexRankingB, 2)
    divisor = float(len(rankingAAux) * (pow(len(rankingAAux), 2) - 1))
    correlacion = (1 - ((6 * total) / float(divisor)))
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
    start()



