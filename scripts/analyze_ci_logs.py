#!/usr/bin/env python3
"""Script para analise de logs do CI com IA.

Este script le logs de pipelines CI (GitHub Actions) e utiliza IA para
analisar falhas, identificar padroes e sugerir correcoes.

Uso:
    python scripts/analyze_ci_logs.py <log_file>
    python scripts/analyze_ci_logs.py --demo
"""

import json
import os
import sys
from datetime import datetime, timedelta


def load_ci_logs(log_file: str) -> list:
    """Carrega logs do CI de um arquivo JSONL."""
    logs = []
    if not os.path.exists(log_file):
        print(f"Arquivo nao encontrado: {log_file}")
        return logs

    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    log_entry = json.loads(line)
                    logs.append(log_entry)
                except json.JSONDecodeError:
                    continue

    return logs


def generate_demo_logs() -> list:
    """Gera logs simulados de um pipeline CI para demonstracao."""
    base_time = datetime.now() - timedelta(hours=2)

    logs = [
        {
            "timestamp": base_time.isoformat(),
            "stage": "lint",
            "status": "success",
            "duration_ms": 1250,
            "output": "All checks passed",
        },
        {
            "timestamp": (base_time + timedelta(seconds=2)).isoformat(),
            "stage": "typecheck",
            "status": "warning",
            "duration_ms": 3400,
            "output": "Found 5 errors in 3 files (run with --check for details)",
            "errors": [
                {
                    "file": "graph/nodes.py",
                    "line": 45,
                    "message": "Incompatible types in assignment",
                },
                {
                    "file": "api/main.py",
                    "line": 23,
                    "message": "Missing return type annotation",
                },
            ],
        },
        {
            "timestamp": (base_time + timedelta(seconds=6)).isoformat(),
            "stage": "test-unit",
            "status": "success",
            "duration_ms": 8200,
            "output": "85 passed, 2 warnings",
        },
        {
            "timestamp": (base_time + timedelta(seconds=15)).isoformat(),
            "stage": "test-integration",
            "status": "failed",
            "duration_ms": 12500,
            "output": "FAILED tests/test_integration.py::test_extract_information_success",
            "errors": [
                {
                    "file": "tests/test_integration.py",
                    "line": 78,
                    "message": "AssertionError: assert 'extracted_information' in {}",
                }
            ],
        },
        {
            "timestamp": (base_time + timedelta(seconds=28)).isoformat(),
            "stage": "docker-build",
            "status": "success",
            "duration_ms": 45000,
            "output": "Successfully built abc123def456",
        },
    ]

    return logs


def analyze_logs(logs: list) -> dict:
    """Analisa logs do CI e identifica problemas."""
    analysis = {
        "total_stages": len(logs),
        "successful_stages": 0,
        "failed_stages": 0,
        "warning_stages": 0,
        "total_duration_ms": 0,
        "issues": [],
        "recommendations": [],
    }

    for log in logs:
        status = log.get("status", "unknown")
        duration = log.get("duration_ms", 0)

        analysis["total_duration_ms"] += duration

        if status == "success":
            analysis["successful_stages"] += 1
        elif status == "failed":
            analysis["failed_stages"] += 1
            analysis["issues"].append(
                {
                    "stage": log.get("stage", "unknown"),
                    "error": log.get("output", "Unknown error"),
                    "details": log.get("errors", []),
                }
            )
        elif status == "warning":
            analysis["warning_stages"] += 1
            analysis["issues"].append(
                {
                    "stage": log.get("stage", "unknown"),
                    "warning": log.get("output", "Unknown warning"),
                    "details": log.get("errors", []),
                }
            )

    # Gerar recomendacoes
    if analysis["failed_stages"] > 0:
        analysis["recommendations"].append(
            "Corrija os erros de teste antes de fazer merge na branch principal."
        )

    if analysis["warning_stages"] > 0:
        analysis["recommendations"].append(
            "Considere corrigir os warnings de typecheck para melhorar a qualidade do codigo."
        )

    if analysis["total_duration_ms"] > 60000:
        analysis["recommendations"].append(
            "Pipeline lenta (>60s). Considere paralelizar etapas ou otimizar dependencias."
        )

    return analysis


def generate_report(analysis: dict) -> str:
    """Gera um relatorio Markdown a partir da analise."""
    report = []
    report.append("# Analise de Logs do CI\n")
    report.append(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Total de etapas:** {analysis['total_stages']}")
    report.append(f"**Sucesso:** {analysis['successful_stages']}")
    report.append(f"**Falhas:** {analysis['failed_stages']}")
    report.append(f"**Warnings:** {analysis['warning_stages']}")
    report.append(f"**Duracao total:** {analysis['total_duration_ms'] / 1000:.2f}s\n")

    if analysis["issues"]:
        report.append("## Problemas Encontrados\n")
        for issue in analysis["issues"]:
            stage = issue.get("stage", "unknown")
            error = issue.get("error") or issue.get("warning", "Unknown")
            report.append(f"### {stage}")
            report.append(f"- **Problema:** {error}")
            if issue.get("details"):
                for detail in issue["details"]:
                    report.append(
                        f"  - `{detail.get('file', 'unknown')}:{detail.get('line', '?')}` - {detail.get('message', '')}"
                    )
            report.append("")

    if analysis["recommendations"]:
        report.append("## Recomendacoes\n")
        for rec in analysis["recommendations"]:
            report.append(f"- {rec}")

    return "\n".join(report)


def main():
    """Funcao principal do script."""
    if len(sys.argv) < 2:
        print("Uso: python analyze_ci_logs.py <log_file>")
        print("Ou: python analyze_ci_logs.py --demo (para logs simulados)")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--demo":
        logs = generate_demo_logs()
        print("Usando logs simulados para demonstracao...\n")
    else:
        logs = load_ci_logs(arg)
        if not logs:
            print("Nenhum log encontrado.")
            sys.exit(1)

    analysis = analyze_logs(logs)
    report = generate_report(analysis)

    print(report)

    # Salvar relatorio
    output_dir = "docs/evidencias"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "ci_log_analysis.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nRelatorio salvo em: {output_file}")


if __name__ == "__main__":
    main()
