#!/bin/bash

rm -r ./terrier-4.0/var/index/*
rm -r ./terrier-4.0/var/results/*

./terrier-4.0/bin/trec_setup.sh $1

./terrier-4.0/bin/trec_terrier.sh -i -Dtrec.collection.class=SimpleFileCollection

./terrier-4.0/bin/trec_terrier.sh -r -Dtrec.model=BM25 -Dignore.low.idf.terms=false -Dtrec.topics=$2

./terrier-4.0/bin/trec_terrier.sh -r -Dtrec.model=TF_IDF -Dignore.low.idf.terms=false -Dtrec.topics=$2

