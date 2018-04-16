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
Utilizando Terrier indexe la colección provista por el equipo docente. Tome 5 necesidades de información y – de forma manual – derive una consulta (query). Para cada una, pruebe la recuperación por los modelos basados en TF_IDF y BM25. 
- ¿Cómo se comportan los rankings?
- Calcule el coeficiente de correlación para los primeros 10, 25 y 50 resultados. ¿Qué conclusiones obtiene?