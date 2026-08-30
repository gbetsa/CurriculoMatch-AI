"""Funcoes de sanitizacao e validacao adversarial contra prompt injection."""

import re

# Padrões de prompt injection conhecidos (EN + PT)
INJECTION_PATTERNS: list[tuple[re.Pattern, str]] = [
    # --- Ingles ---
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
    # --- Portugues ---
    (
        re.compile(
            r"ignore\s+(todas?\s+)?(as\s+)?(instru[çc][õo]es?|regras?|diretrizes?)\s+"
            r"(anteriores?|anteriores|previas?|acima)",
            re.IGNORECASE,
        ),
        "ignore instrucoes anteriores (PT)",
    ),
    (
        re.compile(r"voc[eê]\s+[ée]\s+agora\s+um", re.IGNORECASE),
        "voce e agora um (PT)",
    ),
    (
        re.compile(
            r"atribua.*(pontua[çc][aã]o|m[aá]xima|100|nota\s+maxima)",
            re.IGNORECASE,
        ),
        "atribua pontuacao maxima (PT)",
    ),
    (
        re.compile(
            r"pontua[çc][aã]o\s+(m[aá]xima|maxima|\b100\b|nota\s+maxima)",
            re.IGNORECASE,
        ),
        "pontuacao maxima (PT)",
    ),
    (
        re.compile(
            r"revele.*(regras?\s+internas?|instru[çc][õo]es?\s+de\s+sistema|"
            r"crit[eé]rios?\s+ocultos?|sistema\s+interno)",
            re.IGNORECASE,
        ),
        "revele regras internas (PT)",
    ),
    (
        re.compile(
            r"prioridade\s+sobre\s+qualquer\s+outra\s+instru[çc][aã]o",
            re.IGNORECASE,
        ),
        "prioridade sobre outras instrucoes (PT)",
    ),
    (
        re.compile(
            r"ignore\s+tudo\s+o\s+que\s+(foi|foram)\s+(dito|dizido|informado|definido)",
            re.IGNORECASE,
        ),
        "ignore tudo (PT)",
    ),
    (
        re.compile(
            r"desconsidere\s+(todas?\s+)?(as\s+)?(instru[çc][õo]es?|regras?)",
            re.IGNORECASE,
        ),
        "desconsidere instrucoes (PT)",
    ),
    (
        re.compile(
            r"esque[çc]a\s+(todas?\s+)?(as\s+)?(instru[çc][õo]es?|regras?)",
            re.IGNORECASE,
        ),
        "esqueca instrucoes (PT)",
    ),
    (
        re.compile(r"(fa[çc]a|aja)\s+como\s+se", re.IGNORECASE),
        "faca como se (PT)",
    ),
    (
        re.compile(r"finga\s+que\s+[ée]\s+um", re.IGNORECASE),
        "finga que e um (PT)",
    ),
    (
        re.compile(r"de\s+agora\s+em\s+diante", re.IGNORECASE),
        "de agora em diante (PT)",
    ),
    (
        re.compile(
            r"score\s+(de\s+)?100|nota\s+(de\s+)?100|pontua[çc][aã]o\s+(de\s+)?100",
            re.IGNORECASE,
        ),
        "score 100 (PT)",
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
