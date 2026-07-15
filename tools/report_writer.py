from pathlib import Path


def save_report(content: str, output_path: str = "output/relatorio.md") -> bool:
    """
    Salva o conteúdo Markdown final no diretório especificado.
    Cria o diretório se ele não existir.

    Args:
        content (str): Texto do relatório final gerado pelo agente.
        output_path (str): Caminho final do arquivo. Padrão é output/relatorio.md.

    Returns:
        bool: True se salvo com sucesso.
    """
    try:
        path = Path(output_path)

        # Garante que o diretório pai ('output') existe
        path.parent.mkdir(parents=True, exist_ok=True)

        # Escreve o conteúdo forçando utf-8
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return True
    except Exception as e:
        print(f"Erro ao salvar o relatório: {e}")
        return False
