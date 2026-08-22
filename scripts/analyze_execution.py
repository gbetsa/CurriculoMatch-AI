#!/usr/bin/env python3
"""Script para investigar execucoes a partir de logs estruturados."""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from typing import Optional


def load_logs(log_dir: str = "logs") -> list:
    """Carrega todos os logs JSON de um diretorio."""
    logs = []
    if not os.path.exists(log_dir):
        print(f"Diretorio de logs nao encontrado: {log_dir}")
        return logs

    for filename in os.listdir(log_dir):
        if filename.endswith(".jsonl"):
            filepath = os.path.join(log_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            log_entry = json.loads(line)
                            logs.append(log_entry)
                        except json.JSONDecodeError:
                            continue

    return logs


def filter_by_correlation_id(logs: list, correlation_id: str) -> list:
    """Filtra logs por correlation_id."""
    return [log for log in logs if log.get("correlation_id") == correlation_id]


def analyze_execution(logs: list) -> dict:
    """Analisa uma execucao a partir dos logs filtrados."""
    if not logs:
        return {"error": "Nenhum log encontrado para o correlation_id fornecido"}

    # Ordenar por timestamp
    logs.sort(key=lambda x: x.get("timestamp", ""))

    # Extrair informacoes
    analysis = {
        "correlation_id": logs[0].get("correlation_id", "unknown"),
        "started_at": logs[0].get("timestamp", "unknown"),
        "ended_at": logs[-1].get("timestamp", "unknown"),
        "nodes": [],
        "errors": [],
        "total_duration_ms": 0,
    }

    # Rastrear nos
    node_starts = {}
    node_completions = {}

    for log in logs:
        event = log.get("event", "")
        node = log.get("node", "")

        if event == "node_started" and node:
            node_starts[node] = log
        elif event == "node_completed" and node:
            node_completions[node] = log
            duration = log.get("duration_ms", 0) or 0
            analysis["total_duration_ms"] += duration
        elif event == "node_error" and node:
            analysis["errors"].append(
                {
                    "node": node,
                    "error_type": log.get("error_type", "unknown"),
                    "error_message": log.get("error_message", "unknown"),
                    "timestamp": log.get("timestamp", "unknown"),
                }
            )

    # Construir lista de nos
    for node_name in node_starts:
        node_info = {
            "name": node_name,
            "started_at": node_starts[node_name].get("timestamp", "unknown"),
        }
        if node_name in node_completions:
            node_info["completed_at"] = node_completions[node_name].get(
                "timestamp", "unknown"
            )
            node_info["duration_ms"] = node_completions[node_name].get("duration_ms", 0)
            node_info["status"] = node_completions[node_name].get("status", "unknown")
        else:
            node_info["status"] = "incomplete"

        analysis["nodes"].append(node_info)

    return analysis


def generate_report(analysis: dict) -> str:
    """Gera um relatorio Markdown a partir da analise."""
    report = []
    report.append("# Relatorio de Execucao\n")
    report.append(f"**Correlation ID:** `{analysis.get('correlation_id', 'unknown')}`")
    report.append(f"**Inicio:** {analysis.get('started_at', 'unknown')}")
    report.append(f"**Fim:** {analysis.get('ended_at', 'unknown')}")
    report.append(f"**Duracao Total:** {analysis.get('total_duration_ms', 0):.2f}ms\n")

    report.append("## Sequencia de Nos\n")
    report.append("| No | Status | Duracao (ms) |")
    report.append("|-----|--------|--------------|")

    for node in analysis.get("nodes", []):
        status = node.get("status", "unknown")
        duration = node.get("duration_ms", "N/A")
        if isinstance(duration, (int, float)):
            duration = f"{duration:.2f}"
        report.append(f"| {node['name']} | {status} | {duration} |")

    if analysis.get("errors"):
        report.append("\n## Erros\n")
        for error in analysis["errors"]:
            report.append(
                f"- **{error['node']}**: {error['error_type']} - {error['error_message']}"
            )

    report.append("\n## Resumo\n")
    total_nodes = len(analysis.get("nodes", []))
    completed_nodes = len(
        [n for n in analysis.get("nodes", []) if n.get("status") == "success"]
    )
    report.append(f"- Total de nos: {total_nodes}")
    report.append(f"- Nos concluidos: {completed_nodes}")
    report.append(f"- Erros: {len(analysis.get('errors', []))}")

    return "\n".join(report)


def main():
    """Funcao principal do script."""
    if len(sys.argv) < 2:
        print("Uso: python analyze_execution.py <correlation_id>")
        print("Ou: python analyze_execution.py --all (para listar todas as execucoes)")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--all":
        logs = load_logs()
        if not logs:
            print("Nenhum log encontrado.")
            sys.exit(0)

        # Agrupar por correlation_id
        executions = defaultdict(list)
        for log in logs:
            cid = log.get("correlation_id", "unknown")
            executions[cid].append(log)

        print(f"Total de execucoes encontradas: {len(executions)}\n")
        for cid, exec_logs in executions.items():
            analysis = analyze_execution(exec_logs)
            print(
                f"- {cid}: {analysis.get('started_at', 'unknown')} "
                f"({len(exec_logs)} logs)"
            )
        sys.exit(0)

    correlation_id = arg
    logs = load_logs()
    filtered_logs = filter_by_correlation_id(logs, correlation_id)

    if not filtered_logs:
        print(f"Nenhum log encontrado para correlation_id: {correlation_id}")
        sys.exit(1)

    analysis = analyze_execution(filtered_logs)
    report = generate_report(analysis)

    print(report)

    # Salvar relatorio
    output_dir = "docs/evidencias"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"execution_trace_{correlation_id[:8]}.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nRelatorio salvo em: {output_file}")


if __name__ == "__main__":
    main()
