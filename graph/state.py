import uuid
from typing import Any, TypedDict

from pydantic import BaseModel, Field


class CurriculumData(BaseModel):
    nome: str = Field(description="Nome completo do candidato")
    email: str = Field(description="Endereço de e-mail do candidato")
    telefone: str = Field(description="Telefone de contato do candidato")
    habilidades: list[str] = Field(
        description="Lista de TODAS as hard skills, competências, softwares e linguagens listadas explicitamente nas seções de 'Habilidades', 'Stacks' ou 'Skills'."
    )
    ferramentas_projetos_experiencias: list[str] = Field(
        default_factory=list,
        description="Lista exaustiva de TODAS as tecnologias, bibliotecas (ex: Vite, Express), ORMs (ex: Sequelize) e ferramentas citadas DENTRO dos textos descritivos das Experiências e Projetos Realizados.",
    )
    experiencias: list[str] = Field(
        description="Lista detalhada de cargos, empresas, atividades e PROJETOS, mantendo as tecnologias e ferramentas citadas no texto original."
    )
    formacao: str = Field(description="Nível acadêmico, graduações ou cursos listados")
    idiomas: list[str] = Field(
        description="Idiomas mencionados e seu respectivo nível de fluência"
    )


class JobData(BaseModel):
    cargo: str = Field(description="Nome ou título da vaga anunciada")
    tecnologias: list[str] = Field(
        description="Linguagens de programação, frameworks e tecnologias exigidas"
    )
    requisitos: list[str] = Field(
        description="Requisitos técnicos e comportamentais obrigatórios"
    )
    diferenciais: list[str] = Field(
        description="Conhecimentos extras que contam como diferencial (Nice-to-have)"
    )


class ExtractedInformation(BaseModel):
    candidato: CurriculumData
    vaga: JobData


class AnalysisRecord(BaseModel):
    """Registro de uma analise anterior, persistida no checkpointer."""

    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate_name: str = ""
    job_title: str = ""
    score: int = 0
    report: str = ""
    created_at: str = ""
    correlation_id: str = ""


class AgentState(TypedDict, total=False):
    # Entradas e Validacoes
    curriculum_path: str
    job_path: str
    is_valid: bool
    error_message: str | None

    # Dados Brutos Extraidos
    curriculum_text: str
    job_description: str

    # Dados Estruturados (Saida da LLM na etapa de Extracao)
    extracted_information: dict[str, Any]

    # Resultados Finais da Analise
    compatibility_score: int
    analysis: str

    # Saida Final
    report: str

    # --- Campos Novos (Projeto Final - Bloco 9) ---
    history: list[dict[str, Any]]
    correlation_id: str
    metadata: dict[str, Any]
