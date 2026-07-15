import os
import sys
import argparse
from dotenv import load_dotenv


def parse_args() -> argparse.Namespace:
    """
    Configura e processa os argumentos de linha de comando da aplicação.

    Returns:
        argparse.Namespace: Objeto contendo os argumentos 'curriculo' e 'vaga'.
    """
    parser = argparse.ArgumentParser(
        prog="CurriculoMatch AI",
        description="Analisa a compatibilidade entre um currículo (PDF) e uma descrição de vaga (TXT).",
    )
    parser.add_argument(
        "--curriculo",
        type=str,
        default="input/curriculo.pdf",
        help="Caminho para o arquivo PDF do currículo. (padrão: input/curriculo.pdf)",
    )
    parser.add_argument(
        "--vaga",
        type=str,
        default="input/vaga.txt",
        help="Caminho para o arquivo TXT da vaga. (padrão: input/vaga.txt)",
    )
    return parser.parse_args()


def main():
    """Ponto de entrada principal da aplicação CurriculoMatch AI."""

    # --- 1. Carregamento de Variáveis de Ambiente ---
    load_dotenv()

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("[ERRO] A variavel de ambiente GROQ_API_KEY nao esta definida.")
        print("   Crie um arquivo .env com base no .env.example e preencha sua chave.")
        sys.exit(1)

    # --- 2. Parse dos Argumentos ---
    args = parse_args()

    # --- 3. Importação Tardia do Grafo (após o .env estar carregado) ---
    from graph.workflow import app

    # --- 4. Estado Inicial do Agente ---
    initial_state = {
        "curriculum_path": args.curriculo,
        "job_path": args.vaga,
        "is_valid": True,
    }

    # --- 5. Execução do Grafo com Logs Informativos ---
    print("\n>> CurriculoMatch AI --- Iniciando analise...")
    print(f"   Curriculo : {args.curriculo}")
    print(f"   Vaga      : {args.vaga}\n")

    print("[1/6] Validando arquivos de entrada...")
    print("[2/6] Lendo curriculo...")
    print("[3/6] Lendo descricao da vaga...")
    print("[4/6] Extraindo informacoes estruturadas via LLM...")
    print("[5/6] Analisando compatibilidade...")
    print("[6/6] Gerando e salvando relatorio...\n")

    final_state = app.invoke(initial_state)

    # --- 6. Verificação do Resultado ---
    if not final_state.get("is_valid", True) or final_state.get("error_message"):
        error_msg = final_state.get("error_message", "Erro desconhecido.")
        print(f"[ERRO] PIPELINE ENCERRADO:\n   {error_msg}")
        sys.exit(1)

    print("[OK] Analise concluida com sucesso!")
    print("   O relatorio foi salvo em: output/relatorio.md\n")


if __name__ == "__main__":
    main()
