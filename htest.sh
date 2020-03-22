#!/bin/bash

# ele procura dois arquivos na pasta atual
# Readme.md com a descrição da questão e os testes no formato ghci
# solver.hs com a solução da questão

if [ "$#" -eq 1 ]; then
    cd $1
fi

# gerando a main e os testes
hs.py Readme.md -v .vpl -m __MainOnly.hs --update &&

# montando a main
cat solver.hs > __Main.hs &&
echo "" >> __Main.hs &&
cat __MainOnly.hs >> __Main.hs &&

# compilando a main
ghc __Main.hs -o __Main.out &&

# rodando a main contra os testes
th run __Main.out .vpl

# apagando os arquivos temporários e deixando o .vpl e o Main.hs
rm __Main.out __Main.hs __Main.o __Main.hi __MainOnly.hs

