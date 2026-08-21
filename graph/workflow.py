import os
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import (
    validate_inputs,
    sanitize_inputs,
    load_history,
    read_curriculum_node,
    read_job_node,
    extract_information,
    analyze_match,
    request_approval,
    generate_report,
    save_report_node,
)


def route_after_validation(state: AgentState) -> str:
    """
    Aresta condicional disparada apos a validacao dos arquivos de entrada.

    Retorna o nome do proximo no baseado no resultado da validacao:
    - 'sanitize_inputs' se os inputs forem validos.
    - END se houver erro de validacao (arquivo nao encontrado ou tipo incorreto).
    """
    if state.get("is_valid"):
        return "sanitize_inputs"
    return END


def route_after_read(state: AgentState) -> str:
    """
    Aresta condicional disparada apos cada etapa de leitura de arquivo.

    Garante que o fluxo principal so avanca se nenhum erro de leitura ocorreu.
    """
    if state.get("is_valid", True) and not state.get("error_message"):
        return "continue"
    return END


def build_graph():
    """
    Constroi, configura e compila o grafo de execucao do agente LangGraph.

    Estrutura do Grafo:
    - Ponto de Entrada -> validate_inputs
    - validate_inputs -> (condicional) -> sanitize_inputs | END
    - sanitize_inputs -> load_history
    - load_history -> read_curriculum | read_job (PARALELO)
    - read_curriculum -> (condicional) -> extract_information | END
    - read_job -> (condicional) -> extract_information | END
    - extract_information -> analyze_match
    - analyze_match -> request_approval
    - request_approval -> generate_report
    - generate_report -> save_report
    - save_report -> END

    Returns:
        O grafo compilado e pronto para ser invocado.
    """
    graph = StateGraph(AgentState)

    # --- Registro dos Nos ---
    graph.add_node("validate_inputs", validate_inputs)
    graph.add_node("sanitize_inputs", sanitize_inputs)
    graph.add_node("load_history", load_history)
    graph.add_node("read_curriculum", read_curriculum_node)
    graph.add_node("read_job", read_job_node)
    graph.add_node("extract_information", extract_information)
    graph.add_node("analyze_match", analyze_match)
    graph.add_node("request_approval", request_approval)
    graph.add_node("generate_report", generate_report)
    graph.add_node("save_report", save_report_node)

    # --- Ponto de Entrada ---
    graph.set_entry_point("validate_inputs")

    # --- Aresta Condicional: Pos-validacao ---
    graph.add_conditional_edges(
        "validate_inputs",
        route_after_validation,
        {
            "sanitize_inputs": "sanitize_inputs",
            END: END,
        },
    )

    # --- Sanitizacao -> Historico ---
    graph.add_edge("sanitize_inputs", "load_history")

    # --- Paralelizacao: load_history -> [read_curriculum | read_job] ---
    graph.add_edge("load_history", "read_curriculum")
    graph.add_edge("load_history", "read_job")

    # --- Arestas Condicionais de Verificacao de Leitura ---
    graph.add_conditional_edges(
        "read_curriculum",
        route_after_read,
        {
            "continue": "extract_information",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "read_job",
        route_after_read,
        {
            "continue": "extract_information",
            END: END,
        },
    )

    # --- Fluxo Sequencial Principal ---
    graph.add_edge("extract_information", "analyze_match")
    graph.add_edge("analyze_match", "request_approval")
    graph.add_edge("request_approval", "generate_report")
    graph.add_edge("generate_report", "save_report")
    graph.add_edge("save_report", END)

    # --- Compilacao com ou sem Checkpointer ---
    use_checkpointer = os.getenv("DATABASE_URL")
    if use_checkpointer:
        from graph.checkpointer import create_checkpointer

        checkpointer = create_checkpointer()
        return graph.compile(checkpointer=checkpointer)

    return graph.compile()


# Instancia compilada do grafo, pronta para ser importada pelo main.py
app = build_graph()
