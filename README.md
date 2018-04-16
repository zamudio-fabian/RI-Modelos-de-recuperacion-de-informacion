# RI-Modelos-de-recuperacion-de-informacion
@author - Zamudio Fabian (2018)
Repositorio de Recuperación de Información

### Ejercicio
2) Dados los siguientes documentos, arme la matriz término-documento (TD). Nota: No tenga en cuenta los artículos, preposiciones y conectores.

Doc 1: “El software libre ha tenido un papel fundamental en el crecimiento de Internet. Además, Internet ha favorecido la comunicación entre los desarrolladores de software.”
Doc 2: “La mayor riqueza que tiene un país es la cultura, eso lo hace más libre. ”
Doc 3: “La producción de software es fundamental para nuestro país, como así también lo es la producción de tecnología de hardware y comunicación.”
Doc 4: “La cultura del software libre está en crecimiento. Es fundamental que nuestro país incopore software libre en el estado.” ¿Que documentos se recuperan en cada caso para las siguientes consultas booleanas?

a) (not software) or (pais and fundamental)
b) producción and (cultura or libre)
c) fundamental or libre or país

Muestre mediante operaciones con conjuntos cómo se resuelven las consultas.

3) Utilizando los documentos del ejercicio anterior arme la matriz TD pero calculando wij como la frecuencia del i-ésimo término en el j-ésimo documento. Calcule el ranking para la siguientes consultas utilizando como métrica el producto escalar y luego repita con la métrica del coseno.

a) software
b) país libre
c) producción software país

4) Rearme la matriz del ejercicio anterior pero calcule los pesos de acuerdo a TF*IDF. Repita todas las consultas (por ambas métricas). ¿Puede obtener alguna conclusión?