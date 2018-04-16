# RI-Modelos-de-recuperacion-de-informacion
@author - Zamudio Fabian (2018)
Repositorio de Recuperación de Información

### Ejercicio
Utilizando la colección provista por el equipo docente1, cuya estructura es la siguiente:

- vocabulary.txt → [id_termino, idf, término]
- documentVectors.txt → [id_doc, lista(id_terminos)]
- queries.txt → [id_query, lista(id_terminos)]
- relevants.txt → [id_query, listarelevantes (id_doc)]
- informationNeeds.txt → [id_in, texto_libre]

calcule los conjuntos de respuestas usando el modelo booleano y el modelo vectorial (asuma en todos los casos TF = 1) y compare los resultados contra los relevantes. Trate de explicar las diferencias. A continuación, usando las necesidades de información reescriba los 5 queries y repita la operación. Indique si pudo mejorar la eficiencia a partir de las nuevas consultas.