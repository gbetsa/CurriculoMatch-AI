import os


def read_job(file_path: str) -> str:
    """
    Lê e carrega a descrição de vaga de um arquivo de texto.

    Args:
        file_path (str): Caminho para o arquivo txt da vaga.

    Returns:
        str: Conteúdo textual da vaga.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se houver erro de decodificação (encoding incorreto).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Erro: Arquivo não encontrado no caminho {file_path}")

    # Tentativa primária com UTF-8
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        # Fallback para cp1252/latin-1 (comum em arquivos salvos no Bloco de Notas no Windows)
        try:
            with open(file_path, "r", encoding="cp1252") as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Erro de encoding ao ler o arquivo {file_path}: {e!s}")
