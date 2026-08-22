#!/usr/bin/env python3
"""Script para deteccao de anomalias em metricas de execucao.

Este script simula metricas de execucao do agente (latencia, taxa de erro)
e utiliza analise simples para detectar anomalias e estimar tendencias.

Uso:
    python scripts/detect_anomaly.py
    python scripts/detect_anomaly.py --real-metrics
"""

import json
import os
import random
import sys
from datetime import datetime, timedelta
from typing import Optional


def generate_simulated_metrics(num_executions: int = 20) -> list:
    """Gera metricas simuladas de execucao do agente."""
    metrics = []
    base_time = datetime.now() - timedelta(days=7)

    for i in range(num_executions):
        timestamp = base_time + timedelta(hours=i * 8)

        # Simular latencia com tendencia de aumento
        base_latency = 2500  # 2.5s base
        trend_factor = i * 50  # Aumento gradual
        noise = random.uniform(-200, 200)
        latency_ms = base_latency + trend_factor + noise

        # Simular taxa de erro (0 = sucesso, 1 = falha)
        error_rate = 0.0 if i < 15 else random.uniform(0, 0.3)

        metrics.append(
            {
                "timestamp": timestamp.isoformat(),
                "execution_id": f"exec-{i + 1:03d}",
                "node": "extract_information",
                "latency_ms": round(latency_ms, 2),
                "error_rate": round(error_rate, 4),
                "tokens_used": random.randint(800, 1200),
            }
        )

    return metrics


def calculate_moving_average(values: list, window: int = 5) -> list:
    """Calcula media movel."""
    if len(values) < window:
        return values

    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        window_values = values[start : i + 1]
        result.append(sum(window_values) / len(window_values))

    return result


def detect_anomalies(metrics: list, threshold: float = 2.0) -> dict:
    """Detecta anomalias nas metricas usando regra de threshold."""
    latencies = [m["latency_ms"] for m in metrics]
    error_rates = [m["error_rate"] for m in metrics]

    # Calcular estatisticas
    avg_latency = sum(latencies) / len(latencies)
    std_latency = (
        sum((x - avg_latency) ** 2 for x in latencies) / len(latencies)
    ) ** 0.5

    avg_error_rate = sum(error_rates) / len(error_rates)

    # Media movel
    moving_avg = calculate_moving_average(latencies)

    # Detectar anomalias
    anomalies = []
    for i, m in enumerate(metrics):
        is_anomaly = False
        reason = ""

        # Verificar latencia alta
        if m["latency_ms"] > avg_latency + threshold * std_latency:
            is_anomaly = True
            reason = f"Latencia {m['latency_ms']:.0f}ms > threshold {avg_latency + threshold * std_latency:.0f}ms"

        # Verificar tendencia de aumento
        if i >= 5 and moving_avg[i] > moving_avg[i - 5] * 1.3:
            is_anomaly = True
            reason = f"Tendencia de aumento: media movel {moving_avg[i]:.0f}ms > {moving_avg[i - 5] * 1.3:.0f}ms"

        # Verificar taxa de erro
        if m["error_rate"] > 0.1:
            is_anomaly = True
            reason = f"Taxa de erro alta: {m['error_rate'] * 100:.1f}%"

        if is_anomaly:
            anomalies.append(
                {
                    "execution_id": m["execution_id"],
                    "timestamp": m["timestamp"],
                    "latency_ms": m["latency_ms"],
                    "error_rate": m["error_rate"],
                    "reason": reason,
                }
            )

    return {
        "total_executions": len(metrics),
        "anomalies_found": len(anomalies),
        "anomalies": anomalies,
        "statistics": {
            "avg_latency_ms": round(avg_latency, 2),
            "std_latency_ms": round(std_latency, 2),
            "avg_error_rate": round(avg_error_rate, 4),
            "max_latency_ms": round(max(latencies), 2),
            "min_latency_ms": round(min(latencies), 2),
        },
    }


def estimate_trend(metrics: list) -> dict:
    """Estima tendencia usando regressao linear simples."""
    latencies = [m["latency_ms"] for m in metrics]
    n = len(latencies)

    # Regressao linear simples: y = mx + b
    x_mean = (n - 1) / 2
    y_mean = sum(latencies) / n

    numerator = sum((i - x_mean) * (latencies[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator

    intercept = y_mean - slope * x_mean

    # Estimar latencia em 7 dias (mais ~21 execucoes)
    future_executions = 21
    future_latency = slope * (n + future_executions) + intercept

    # Calcular chance de falha
    avg_error_rate = sum(m["error_rate"] for m in metrics) / n
    if slope > 0:
        # Tendencia de aumento
        failure_probability = min(0.95, avg_error_rate + (slope / 1000) * 7)
    else:
        failure_probability = max(0.05, avg_error_rate - (abs(slope) / 1000) * 7)

    return {
        "trend_slope": round(slope, 4),
        "trend_direction": "aumento" if slope > 0 else "diminuicao",
        "current_avg_latency_ms": round(y_mean, 2),
        "estimated_future_latency_ms": round(future_latency, 2),
        "estimated_failure_probability_7d": round(failure_probability, 4),
        "interpretation": _interpret_trend(slope, failure_probability),
    }


def _interpret_trend(slope: float, failure_prob: float) -> str:
    """Interpreta a tendencia em linguagem natural."""
    if slope > 100:
        trend_desc = "aumento significativo"
    elif slope > 20:
        trend_desc = "aumento gradual"
    elif slope < -100:
        trend_desc = "diminuicao significativa"
    elif slope < -20:
        trend_desc = "diminuicao gradual"
    else:
        trend_desc = "estavel"

    if failure_prob > 0.7:
        risk_desc = "ALTO risco de falha"
    elif failure_prob > 0.4:
        risk_desc = "MEDIO risco de falha"
    else:
        risk_desc = "BAIXO risco de falha"

    return (
        f"Tendencia: {trend_desc}. {risk_desc} em 7 dias ({failure_prob * 100:.1f}%)."
    )


def generate_report(analysis: dict, trend: dict) -> str:
    """Gera um relatorio Markdown a partir da analise e tendencia."""
    report = []
    report.append("# Relatorio de Deteccao de Anomalias\n")
    report.append(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Total de execucoes analisadas:** {analysis['total_executions']}")
    report.append(f"**Anomalias encontradas:** {analysis['anomalies_found']}\n")

    report.append("## Estatisticas\n")
    stats = analysis["statistics"]
    report.append(f"- **Latencia media:** {stats['avg_latency_ms']:.2f}ms")
    report.append(f"- **Desvio padrao:** {stats['std_latency_ms']:.2f}ms")
    report.append(f"- **Latencia minima:** {stats['min_latency_ms']:.2f}ms")
    report.append(f"- **Latencia maxima:** {stats['max_latency_ms']:.2f}ms")
    report.append(f"- **Taxa de erro media:** {stats['avg_error_rate'] * 100:.2f}%\n")

    if analysis["anomalies"]:
        report.append("## Anomalias Detectadas\n")
        report.append("| Execucao | Timestamp | Latencia | Erro | Motivo |")
        report.append("|----------|-----------|----------|------|--------|")
        for anomaly in analysis["anomalies"]:
            report.append(
                f"| {anomaly['execution_id']} | {anomaly['timestamp'][:16]} | {anomaly['latency_ms']:.0f}ms | {anomaly['error_rate'] * 100:.1f}% | {anomaly['reason']} |"
            )
        report.append("")

    report.append("## Analise de Tendencia\n")
    report.append(f"- **Direcao:** {trend['trend_direction']}")
    report.append(f"- **Inclinacao:** {trend['trend_slope']:.4f}ms/execucao")
    report.append(f"- **Latencia atual:** {trend['current_avg_latency_ms']:.2f}ms")
    report.append(
        f"- **Latencia estimada (7 dias):** {trend['estimated_future_latency_ms']:.2f}ms"
    )
    report.append(
        f"- **Chance de falha (7 dias):** {trend['estimated_failure_probability_7d'] * 100:.1f}%"
    )
    report.append(f"\n**Interpretacao:** {trend['interpretation']}\n")

    report.append("## Recomendacoes\n")
    if trend["trend_slope"] > 50:
        report.append("- **URGENTE:** Investigar causa do aumento de latencia")
        report.append("- Verificar se ha leaks de memoria ou recursos")
        report.append("- Considerar otimizacao do node extract_information")
    elif trend["trend_slope"] > 10:
        report.append("- Monitorar latencia nas proximas execucoes")
        report.append("- Verificar se o aumento e significativo")
    else:
        report.append("- Sistema estavel, sem acoes imediatas necessarias")

    return "\n".join(report)


def main():
    """Funcao principal do script."""
    print("Gerando metricas simuladas...\n")

    # Gerar metricas simuladas
    metrics = generate_simulated_metrics(20)

    # Detectar anomalias
    analysis = detect_anomalies(metrics)

    # Estimar tendencia
    trend = estimate_trend(metrics)

    # Gerar relatorio
    report = generate_report(analysis, trend)

    print(report)

    # Salvar relatorio
    output_dir = "docs/evidencias"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "anomaly_report.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nRelatorio salvo em: {output_file}")


if __name__ == "__main__":
    main()
