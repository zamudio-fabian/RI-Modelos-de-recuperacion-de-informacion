# RI-Modelos-de-recuperacion-de-informacion
@author - Zamudio Fabian (2018)
Repositorio de Recuperación de Información

### Ejemplo de uso
```
./terrier-4.0/bin/trec_setup.sh PATH/TO/CORPUS

./terrier-4.0/bin/trec_terrier.sh -i -Dtrec.collection.class=SimpleFileCollection

./terrier-4.0/bin/trec_terrier.sh -r -Dtrec.model=BM25 -Dignore.low.idf.terms=false -Dtrec.topics=PATH/TO/QUERY

./terrier-4.0/bin/trec_terrier.sh -r -Dtrec.model=TF_IDF -Dignore.low.idf.terms=false -Dtrec.topics=PATH/TO/QUERY
```


### Ejercicio
Escriba un pequeño programa que lea un directorio con documentos de texto y arme una estructura de datos en memoria para soportar la recuperación. Luego, debe permitir ingresar un query y devolver un ranking de los documentos relevantes utilizando el modelo vectorial. Se debe soportar la ponderación de los términos de la consulta. Implemente las versiones sugeridas en [MIR].