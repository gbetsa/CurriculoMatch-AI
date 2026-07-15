@echo off
set PYTHONIOENCODING=utf-8

if not exist venv\Scripts\activate.bat (
    echo [ERRO] Ambiente virtual 'venv' nao encontrado.
    echo Por favor, crie o ambiente virtual "python -m venv venv" e instale as dependencias "pip install -r requirements.txt".
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

:: Procura automaticamente o primeiro PDF e o primeiro TXT na pasta input
set CURRICULO=
set VAGA=

for %%f in (input\*.pdf) do (
    set "CURRICULO=%%f"
    goto :found_pdf
)
:found_pdf

for %%f in (input\*.txt) do (
    set "VAGA=%%f"
    goto :found_txt
)
:found_txt

if "%CURRICULO%"=="" (
    echo [ERRO] Nenhum arquivo PDF encontrado na pasta input\
    echo Por favor, coloque seu curriculo na pasta input\
    pause
    exit /b 1
)

if "%VAGA%"=="" (
    echo [ERRO] Nenhum arquivo TXT encontrado na pasta input\
    echo Por favor, coloque a descricao da vaga na pasta input\
    pause
    exit /b 1
)

echo.
echo ===========================================
echo Arquivos identificados automaticamente:
echo Curriculo: %CURRICULO%
echo Vaga     : %VAGA%
echo ===========================================
echo.

python main.py --curriculo "%CURRICULO%" --vaga "%VAGA%"

pause
