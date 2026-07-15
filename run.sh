#!/bin/bash
export PYTHONIOENCODING=utf-8

if [ ! -d "venv" ]; then
    echo "[ERRO] Ambiente virtual 'venv' nao encontrado."
    echo "Por favor, crie o ambiente virtual 'python3 -m venv venv' e instale as dependencias 'pip install -r requirements.txt'."
    exit 1
fi

source venv/bin/activate

CURRICULO=$(ls input/*.pdf 2>/dev/null | head -n 1)
VAGA=$(ls input/*.txt 2>/dev/null | head -n 1)

if [ -z "$CURRICULO" ]; then
    echo "[ERRO] Nenhum arquivo PDF encontrado na pasta input/"
    echo "Por favor, coloque seu curriculo (PDF) dentro da pasta input/"
    exit 1
fi

if [ -z "$VAGA" ]; then
    echo "[ERRO] Nenhum arquivo TXT encontrado na pasta input/"
    echo "Por favor, coloque a descricao da vaga (TXT) dentro da pasta input/"
    exit 1
fi

echo ""
echo "==========================================="
echo "Arquivos identificados automaticamente:"
echo "Curriculo: $CURRICULO"
echo "Vaga     : $VAGA"
echo "==========================================="
echo ""

python3 main.py --curriculo "$CURRICULO" --vaga "$VAGA"
