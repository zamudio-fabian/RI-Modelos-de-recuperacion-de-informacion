#!/bin/bash

rm -r ./terrier-4.0/var/index/*
rm -r ./terrier-4.0/var/results/*

./terrier-4.0/bin/trec_setup.sh 'documentos.trec'

./terrier-4.0/bin/trec_terrier.sh -i

./terrier-4.0/bin/trec_terrier.sh -r -Dtrec.model=TF_IDF -Dignore.low.idf.terms=false -Dtrec.topics='queries.txt'

./terrier-4.0/bin/trec_terrier.sh -e -Dtrec.qrels='relevantes.txt'

./terrier-4.0/bin/trec_terrier.sh -r -Dtrec.model=TF_IDF -Dignore.low.idf.terms=false -Dtrec.topics='queries_con_duplicados.txt'

./terrier-4.0/bin/trec_terrier.sh -e -Dtrec.qrels='relevantes.txt'

cp ./terrier-4.0/var/results/TF_IDF_0.eval queries_evaluacion.txt

cp ./terrier-4.0/var/results/TF_IDF_1.eval queries_con_duplicados_evaluacion.txt