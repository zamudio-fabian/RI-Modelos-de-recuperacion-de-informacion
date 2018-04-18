# RI-Modelos-de-recuperacion-de-informacion
@author - Zamudio Fabian (2018)
Repositorio de Recuperación de Información

### Ejemplo de uso

```
python estructura.py <PATH/TO/CORPUS> [<PATH/TO/PALABRAS/VACIAS>]
```
Luego se pueden ingresar las queries para ver los resultados

### Ejercicio
Se requiere evaluar la performance en la recuperación de un sistema. Para una consulta q1, dicho sistema entregó la siguiente salida.

1(R) 2 (N) 3(N) 4(R) 5(R) 6(N) 7(N) 8(N) 9(N) 10(R) 11(N) 12(N) 13(N) 14(R) 15(N)
Los documentos identificados como R son los relevantes, mientras que las N’s corresponden a documentos no relevantes a q1. 

Suponga – además – que existen en el corpus otros 6 documentos relevantes a q1 que el sistema no recuperó. A partir de esta salida calcule las siguientes medidas:

- a) Recall y Precision para cada posición j
- b) Recall y Precision promedio
- c) Precisión al 50% de Recall
- d) Precisión interpolada al 50% de Recall
- e) Precisión-R

Finalmente, realice las gráficas interpolada y sin interpolar. Luego, interprete brevemente los resultados y brinde una explicación