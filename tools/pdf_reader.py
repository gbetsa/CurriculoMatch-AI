import os

import fitz  # PyMuPDF


def read_curriculum(file_path: str) -> str:
    """
    Lê e extrai o conteúdo textual de um arquivo PDF.

    Args:
        file_path (str): Caminho para o arquivo PDF do currículo.

    Returns:
        str: Texto extraído do PDF.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o arquivo for inválido ou não contiver camada de texto.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Erro: Arquivo não encontrado no caminho {file_path}")

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise ValueError(f"Erro ao abrir o PDF: {e!s}")

    text = ""
    for page in doc:
        text += page.get_text()

    doc.close()

    # Se extraiu menos de 50 caracteres, muito provavelmente é baseado em imagem.
    if len(text.strip()) < 50:
        raise ValueError(
            "O PDF parece ser baseado apenas em imagens ou está vazio. O CurriculoMatch AI requer PDFs com camada de texto."
        )

    return text
