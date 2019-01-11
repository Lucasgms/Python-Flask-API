#!/bin/bash
mongoimport --host db --db lucas --collection estudantes --type csv --headerline --file /db/dataset_estudantes.csv
