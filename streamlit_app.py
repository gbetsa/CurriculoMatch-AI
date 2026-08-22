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

# URL da API
API_URL = os.getenv("API_URL", "http://localhost:8000")


def check_api_health() -> bool:
    """Verifica se a API esta disponivel."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def render_report(report: str, score: int):
    """Renderiza o relatorio com barra de progresso."""
    # Barra de progresso
    st.progress(score / 100)
    st.metric("Score de Aderencia", f"{score}/100")

    # Relatorio em Markdown
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

        with st.spinner("Analisando curriculo... Aguarde."):
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

                response = requests.post(
                    f"{API_URL}/analyze",
                    files=files,
                    data=data,
                    timeout=120,
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("Analise concluida com sucesso!")

                    # Exibir resultado
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Candidato", result.get("candidate_name", "N/A"))
                    with col2:
                        st.metric("Vaga", result.get("job_title", "N/A"))
                    with col3:
                        st.metric("Status", result.get("status", "N/A"))

                    render_report(result.get("report", ""), result.get("score", 0))

                    # Botao de aprovacao
                    st.markdown("---")
                    st.subheader("Aprovacao")
                    analysis_id = result.get("analysis_id", "")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "Aprovar Analise",
                            type="primary",
                            key="approve_btn",
                            use_container_width=True,
                        ):
                            try:
                                approve_response = requests.post(
                                    f"{API_URL}/approve/{analysis_id}",
                                    json={"approved": True},
                                    timeout=30,
                                )
                                if approve_response.status_code == 200:
                                    st.success("Analise aprovada com sucesso!")
                                else:
                                    st.error(
                                        f"Erro ao aprovar: {approve_response.status_code}"
                                    )
                            except requests.exceptions.ConnectionError:
                                st.error("Nao foi possivel conectar a API.")
                    with col2:
                        if st.button(
                            "Rejeitar Analise",
                            type="secondary",
                            key="reject_btn",
                            use_container_width=True,
                        ):
                            try:
                                approve_response = requests.post(
                                    f"{API_URL}/approve/{analysis_id}",
                                    json={"approved": False},
                                    timeout=30,
                                )
                                if approve_response.status_code == 200:
                                    st.warning("Analise rejeitada.")
                                else:
                                    st.info(
                                        f"Analise rejeitada: {approve_response.status_code}"
                                    )
                            except requests.exceptions.ConnectionError:
                                st.error("Nao foi possivel conectar a API.")

                elif response.status_code == 422:
                    st.error(
                        f"Erro de validacao: {response.json().get('detail', 'Erro desconhecido')}"
                    )
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Nao foi possivel conectar a API. Verifique se o backend esta rodando."
                )
            except requests.exceptions.Timeout:
                st.error("A requisicao expirou. Tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e!s}")


def tab_history():
    """Aba 2: Historico."""
    st.header("Historico de Analises")

    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        candidate_filter = st.text_input(
            "Filtrar por candidato", key="candidate_filter"
        )
    with col2:
        job_filter = st.text_input("Filtrar por vaga", key="job_filter")
    with col3:
        page_size = st.selectbox("Itens por pagina", [5, 10, 20], key="page_size")

    # Paginacao
    if "history_page" not in st.session_state:
        st.session_state.history_page = 1

    page = st.session_state.history_page

    try:
        params = {
            "page": page,
            "limit": page_size,
        }
        if candidate_filter:
            params["candidate_name"] = candidate_filter
        if job_filter:
            params["job_title"] = job_filter

        response = requests.get(f"{API_URL}/history", params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            total = data.get("total", 0)
            pages = data.get("pages", 0)

            if not items:
                st.info("Nenhuma analise encontrada.")
            else:
                # Tabela de historico
                st.dataframe(
                    [
                        {
                            "Data": item.get("created_at", ""),
                            "Candidato": item.get("candidate_name", ""),
                            "Vaga": item.get("job_title", ""),
                            "Score": item.get("score", 0),
                            "Status": "Concluido",
                        }
                        for item in items
                    ],
                    use_container_width=True,
                )

                # Paginacao
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if page > 1 and st.button("Anterior"):
                        st.session_state.history_page -= 1
                        st.rerun()
                with col2:
                    st.write(f"Pagina {page} de {pages} ({total} itens)")
                with col3:
                    if page < pages and st.button("Proximo"):
                        st.session_state.history_page += 1
                        st.rerun()
        else:
            st.error(f"Erro ao carregar historico: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error(
            "Nao foi possivel conectar a API. Verifique se o backend esta rodando."
        )
    except Exception as e:
        st.error(f"Erro inesperado: {e!s}")


def tab_compare():
    """Aba 3: Comparar Candidatos."""
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

        with st.spinner(f"Analisando {len(curriculum_files)} curriculos... Aguarde."):
            try:
                files = [
                    ("curriculos", (f.name, f.getvalue(), "application/pdf"))
                    for f in curriculum_files
                ]
                data = {
                    "job_title": job_title,
                    "job_description": job_description,
                }

                response = requests.post(
                    f"{API_URL}/analyze/batch",
                    files=files,
                    data=data,
                    timeout=300,
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("Comparacao concluida com sucesso!")

                    # Ranking
                    st.subheader("Ranking")
                    ranking = result.get("ranking", [])
                    for i, name in enumerate(ranking, 1):
                        st.write(f"{i}o - {name}")

                    # Resultados detalhados
                    st.subheader("Detalhes")
                    results = result.get("results", [])

                    cols = st.columns(min(len(results), 3))
                    for i, r in enumerate(results):
                        with cols[i % 3], st.expander(
                            f"{r.get('candidate_name', 'N/A')} - Score: {r.get('score', 0)}"
                        ):
                            st.metric("Score", f"{r.get('score', 0)}/100")
                            st.markdown(r.get("report", ""))

                elif response.status_code == 422:
                    st.error(
                        f"Erro de validacao: {response.json().get('detail', 'Erro desconhecido')}"
                    )
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Nao foi possivel conectar a API. Verifique se o backend esta rodando."
                )
            except requests.exceptions.Timeout:
                st.error("A requisicao expirou. Tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e!s}")


def main():
    """Funcao principal do Streamlit."""
    st.title("CurriculoMatch AI")
    st.markdown("Sistema de triagem automatizada de curriculos com IA")

    # Verificar saude da API
    if not check_api_health():
        st.warning(
            "Backend da API nao esta disponivel. Algumas funcionalidades podem nao funcionar."
        )

    # Abas
    tab1, tab2, tab3 = st.tabs(["Nova Analise", "Historico", "Comparar"])

    with tab1:
        tab_new_analysis()

    with tab2:
        tab_history()

    with tab3:
        tab_compare()


if __name__ == "__main__":
    main()
