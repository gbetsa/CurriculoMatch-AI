from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import (
    validate_inputs,
    read_curriculum_node,
    read_job_node,
    extract_information,
    analyze_match,
    generate_report,
    save_report_node,
)


def route_after_validation(state: AgentState) -> str:
    """
    Aresta condicional disparada após a validação dos arquivos de entrada.

    Retorna o nome do próximo nó baseado no resultado da validação:
    - 'read_curriculum' se os inputs forem válidos.
    - END se houver erro de validação (arquivo não encontrado ou tipo incorreto).
    """
    if state.get("is_valid"):
        return "read_curriculum"
    return END


def route_after_read(state: AgentState) -> str:
    """
    Aresta condicional disparada após cada etapa de leitura de arquivo.

    Garante que o fluxo principal só avança se nenhum erro de leitura ocorreu.
    """
    if state.get("is_valid", True) and not state.get("error_message"):
        return "continue"
    return END


def build_graph() -> StateGraph:
    """
    Constrói, configura e compila o grafo de execução do agente LangGraph.

    Estrutura do Grafo:
    - Ponto de Entrada -> validate_inputs
    - validate_inputs -> (condicional) -> read_curriculum | END
    - read_curriculum -> (condicional) -> read_job | END
    - read_job -> (condicional) -> extract_information | END
    - extract_information -> analyze_match
    - analyze_match -> generate_report
    - generate_report -> save_report
    - save_report -> END

    Returns:
        StateGraph: O grafo compilado e pronto para ser invocado.
    """
    graph = StateGraph(AgentState)

    # --- Registro dos Nós ---
    graph.add_node("validate_inputs", validate_inputs)
    graph.add_node("read_curriculum", read_curriculum_node)
    graph.add_node("read_job", read_job_node)
    graph.add_node("extract_information", extract_information)
    graph.add_node("analyze_match", analyze_match)
    graph.add_node("generate_report", generate_report)
    graph.add_node("save_report", save_report_node)

    # --- Ponto de Entrada ---
    graph.set_entry_point("validate_inputs")

    # --- Aresta Condicional: Pós-validação ---
    graph.add_conditional_edges(
        "validate_inputs",
        route_after_validation,
        {
            "read_curriculum": "read_curriculum",
            END: END,
        },
    )

    # --- Arestas Condicionais de Verificação de Leitura ---
    graph.add_conditional_edges(
        "read_curriculum",
        route_after_read,
        {
            "continue": "read_job",
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
    graph.add_edge("analyze_match", "generate_report")
    graph.add_edge("generate_report", "save_report")
    graph.add_edge("save_report", END)

    return graph.compile()


# Instância compilada do grafo, pronta para ser importada pelo main.py
app = build_graph()
