"""Funcoes de sanitizacao e validacao adversarial contra prompt injection."""

import re

# Padrões de prompt injection conhecidos
INJECTION_PATTERNS: list[tuple[re.Pattern, str]] = [
    (
        re.compile(
            r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|rules|prompts)",
            re.IGNORECASE,
        ),
        "ignore previous instructions",
    ),
    (re.compile(r"you\s+are\s+now\s+a", re.IGNORECASE), "you are now a"),
    (re.compile(r"system\s*:", re.IGNORECASE), "system:"),
    (re.compile(r"<|im_start|>", re.IGNORECASE), "<|im_start|>"),
    (re.compile(r"ignore\s+all\s+rules", re.IGNORECASE), "ignore all rules"),
    (
        re.compile(r"disregard\s+(all|any|previous)", re.IGNORECASE),
        "disregard previous",
    ),
    (re.compile(r"forget\s+(all|any|previous)", re.IGNORECASE), "forget previous"),
    (re.compile(r"new\s+instructions?\s*:", re.IGNORECASE), "new instructions:"),
    (
        re.compile(r"override\s+(all|any)?\s*(instructions?|rules?)", re.IGNORECASE),
        "override instructions",
    ),
    (re.compile(r"you\s+must\s+ignore", re.IGNORECASE), "you must ignore"),
    (re.compile(r"do\s+not\s+follow", re.IGNORECASE), "do not follow"),
    (re.compile(r"act\s+as\s+if", re.IGNORECASE), "act as if"),
    (re.compile(r"pretend\s+you\s+are", re.IGNORECASE), "pretend you are"),
    (re.compile(r"role\s*play\s+as", re.IGNORECASE), "role play as"),
    (re.compile(r"from\s+now\s+on", re.IGNORECASE), "from now on"),
    (re.compile(r"score\s+this\s+candidate\s+(a\s+)?100", re.IGNORECASE), "score 100"),
    (
        re.compile(
            r"give\s+(this|the)\s+candidate\s+a\s+score\s+of\s+100", re.IGNORECASE
        ),
        "give score of 100",
    ),
]


def sanitize_text(text: str) -> tuple[str, list[str]]:
    """
    Detecta e neutraliza padroes de prompt injection em texto.

    Args:
        text: Texto a ser sanitizado (curriculo ou descricao de vaga).

    Returns:
        Tupla com (texto sanitizado, lista de padroes detectados).
    """
    sanitized = text
    detected = []

    for pattern, description in INJECTION_PATTERNS:
        if pattern.search(sanitized):
            detected.append(description)
            sanitized = pattern.sub("[SANITIZED]", sanitized)

    return sanitized, detected


def detect_injection(text: str) -> bool:
    """
    Verifica se o texto contem padroes de prompt injection.

    Args:
        text: Texto a ser analisado.

    Returns:
        True se injection detectada, False caso contrario.
    """
    for pattern, _ in INJECTION_PATTERNS:
        if pattern.search(text):
            return True
    return False
