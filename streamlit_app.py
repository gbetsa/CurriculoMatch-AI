"""Interface web Streamlit para o CurriculoMatch AI."""

import os

import requests
import streamlit as st

# Configuracao da pagina
st.set_page_config(
    page_title="CurriculoMatch AI",
    page_icon=":briefcase:",
    layout="wide",
)

# URLs (apenas n8n - API nao e chamada diretamente)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/analyze")
N8N_BATCH_WEBHOOK_URL = os.getenv(
    "N8N_BATCH_WEBHOOK_URL", "http://localhost:5678/webhook/analyze-batch"
)


def render_report(report: str, score: int):
    """Renderiza o relatorio com barra de progresso."""
    st.progress(score / 100)
    st.metric("Score de Aderencia", f"{score}/100")
    st.markdown("---")
    st.markdown(report)


def tab_new_analysis():
    """Aba 1: Nova Analise."""
    st.header("Nova Analise")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Curriculo")
        curriculum_file = st.file_uploader(
            "Selecione o curriculo (PDF)",
            type=["pdf"],
            key="curriculum_upload",
        )

    with col2:
        st.subheader("Vaga")
        job_title = st.text_input(
            "Titulo da Vaga", placeholder="Ex: Desenvolvedor Python"
        )
        job_description = st.text_area(
            "Descricao da Vaga",
            placeholder="Descreva os requisitos da vaga...",
            height=150,
        )

    if st.button("Analisar", type="primary", use_container_width=True):
        if not curriculum_file:
            st.error("Por favor, faca upload de um curriculo PDF.")
            return

        if not job_title or not job_description:
            st.error("Por favor, preencha o titulo e a descricao da vaga.")
            return

        with st.spinner("Analisando curriculo via n8n... Aguarde."):
            try:
                files = {
                    "curriculum": (
                        curriculum_file.name,
                        curriculum_file.getvalue(),
                        "application/pdf",
                    )
                }
                data = {
                    "job_title": job_title,
                    "job_description": job_description,
                }

                try:
                    response = requests.post(
                        N8N_WEBHOOK_URL,
                        files=files,
                        data=data,
                        timeout=120,
                    )
                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                ):
                    st.error(
                        "Nao foi possivel conectar ao n8n. Verifique se o workflow esta ativo."
                    )
                    return

                result = response.json()

                if response.status_code == 200:
                    st.success("Analise concluida com sucesso!")
                    st.caption("Via n8n workflow")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Candidato", result.get("candidate_name", "N/A"))
                    with col2:
                        st.metric("Vaga", result.get("job_title", "N/A"))
                    with col3:
                        st.metric("Status", result.get("status", "N/A"))

                    render_report(result.get("report", ""), result.get("score", 0))

                elif response.status_code == 400:
                    error_msg = result.get("error", "Erro de seguranca")
                    details = result.get("details", [])
                    stage = result.get("stage", "")

                    stage_names = {
                        "validacao": "Validacao de Dados",
                        "regex": "Verificacao de Seguranca",
                        "ia_security": "Analise de IA (vaga)",
                        "api_injection": "Analise de IA (curriculo)",
                    }
                    stage_name = stage_names.get(stage, stage)

                    st.error("Analise bloqueada pelo sistema de seguranca")
                    st.info(f"**Motivo:** {error_msg}")
                    st.caption(f"Etapa: {stage_name}")
                    if details:
                        st.markdown("**Detalhes:**")
                        for d in details:
                            st.write(f"- {d}")

                else:
                    st.error(f"Erro no n8n: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Nao foi possivel conectar ao n8n. Verifique se o backend esta rodando."
                )
            except requests.exceptions.Timeout:
                st.error("A requisicao expirou. Tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e!s}")


def tab_compare():
    """Aba 2: Comparar Candidatos."""
    st.header("Comparar Candidatos")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Vaga")
        job_title = st.text_input("Titulo da Vaga", key="compare_job_title")
        job_description = st.text_area(
            "Descricao da Vaga",
            key="compare_job_desc",
            height=150,
        )

    with col2:
        st.subheader("Curriculos")
        curriculum_files = st.file_uploader(
            "Selecione os curriculos (PDFs)",
            type=["pdf"],
            accept_multiple_files=True,
            key="compare_uploads",
        )

    if curriculum_files:
        st.info(f"{len(curriculum_files)} curriculo(s) selecionado(s)")

    if st.button("Comparar", type="primary", use_container_width=True):
        if not curriculum_files:
            st.error("Por favor, faca upload de pelo menos um curriculo.")
            return

        if not job_title or not job_description:
            st.error("Por favor, preencha o titulo e a descricao da vaga.")
            return

        with st.spinner(
            f"Analisando {len(curriculum_files)} curriculos via n8n... Aguarde."
        ):
            try:
                files = [
                    ("curriculos", (f.name, f.getvalue(), "application/pdf"))
                    for f in curriculum_files
                ]
                data = {
                    "job_title": job_title,
                    "job_description": job_description,
                }

                try:
                    response = requests.post(
                        N8N_BATCH_WEBHOOK_URL,
                        files=files,
                        data=data,
                        timeout=300,
                    )
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Nao foi possivel conectar ao n8n. Verifique se o workflow esta ativo."
                    )
                    return

                if response.status_code == 200:
                    result = response.json()
                    results = result.get("results", [])
                    ranking = result.get("ranking", [])

                    if not results:
                        st.warning(
                            "Nenhum curriculo passou na verificacao de seguranca. "
                            "Todos foram bloqueados por prompt injection."
                        )
                        return

                    st.success("Comparacao concluida com sucesso!")
                    st.caption("Via n8n workflow")

                    st.subheader("Ranking")
                    for i, name in enumerate(ranking, 1):
                        st.write(f"{i}o - {name}")

                    st.subheader("Detalhes")

                    cols = st.columns(min(len(results), 3))
                    for i, r in enumerate(results):
                        with cols[i % 3], st.expander(
                            f"{r.get('candidate_name', 'N/A')} - Score: {r.get('score', 0)}"
                        ):
                            st.metric("Score", f"{r.get('score', 0)}/100")
                            st.markdown(r.get("report", ""))

                elif response.status_code == 400:
                    error_data = response.json()
                    stage = error_data.get("stage", "")
                    stage_labels = {
                        "validacao": "Validacao de Dados",
                        "ia_security": "Analise de IA",
                        "multipart": "Montagem de Requisicao",
                    }
                    stage_name = stage_labels.get(stage, stage)
                    st.error(f"**{stage_name}**")
                    st.error(error_data.get("error", "Erro desconhecido"))
                    details = error_data.get("details", [])
                    for d in details:
                        st.warning(d)
                else:
                    st.error(f"Erro no n8n: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Nao foi possivel conectar ao n8n. Verifique se o backend esta rodando."
                )
            except requests.exceptions.Timeout:
                st.error("A requisicao expirou. Tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e!s}")


def main():
    """Funcao principal do Streamlit."""
    st.title("CurriculoMatch AI")
    st.markdown("Sistema de triagem automatizada de curriculos com IA")

    tab1, tab2 = st.tabs(["Nova Analise", "Comparar"])

    with tab1:
        tab_new_analysis()

    with tab2:
        tab_compare()


if __name__ == "__main__":
    main()
