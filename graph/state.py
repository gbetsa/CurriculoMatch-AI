from typing import Any, Dict, List, Optional, TypedDict
from pydantic import BaseModel, Field


class CurriculumData(BaseModel):
    nome: str = Field(description="Nome completo do candidato")
    email: str = Field(description="Endereço de e-mail do candidato")
    telefone: str = Field(description="Telefone de contato do candidato")
    habilidades: List[str] = Field(
        description="Lista de TODAS as hard skills, competências, softwares e linguagens listadas explicitamente nas seções de 'Habilidades', 'Stacks' ou 'Skills'."
    )
    ferramentas_projetos_experiencias: List[str] = Field(
        default_factory=list,
        description="Lista exaustiva de TODAS as tecnologias, bibliotecas (ex: Vite, Express), ORMs (ex: Sequelize) e ferramentas citadas DENTRO dos textos descritivos das Experiências e Projetos Realizados."
    )
    experiencias: List[str] = Field(
        description="Lista detalhada de cargos, empresas, atividades e PROJETOS, mantendo as tecnologias e ferramentas citadas no texto original."
    )
    formacao: str = Field(description="Nível acadêmico, graduações ou cursos listados")
    idiomas: List[str] = Field(
        description="Idiomas mencionados e seu respectivo nível de fluência"
    )


class JobData(BaseModel):
    cargo: str = Field(description="Nome ou título da vaga anunciada")
    tecnologias: List[str] = Field(
        description="Linguagens de programação, frameworks e tecnologias exigidas"
    )
    requisitos: List[str] = Field(
        description="Requisitos técnicos e comportamentais obrigatórios"
    )
    diferenciais: List[str] = Field(
        description="Conhecimentos extras que contam como diferencial (Nice-to-have)"
    )


class ExtractedInformation(BaseModel):
    candidato: CurriculumData
    vaga: JobData


class AgentState(TypedDict, total=False):
    # Entradas e Validações
    curriculum_path: str
    job_path: str
    is_valid: bool
    error_message: Optional[str]

    # Dados Brutos Extraídos
    curriculum_text: str
    job_description: str

    # Dados Estruturados (Saída da LLM na etapa de Extração)
    extracted_information: Dict[str, Any]

    # Resultados Finais da Análise
    compatibility_score: int
    analysis: str

    # Saída Final
    report: str
