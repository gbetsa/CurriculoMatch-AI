from graph.nodes import validate_inputs, analyze_match
import pytest


def test_validate_inputs_success(mocker, tmp_path):
    # Setup mock files
    pdf_path = tmp_path / "curriculo.pdf"
    pdf_path.touch()
    txt_path = tmp_path / "vaga.txt"
    txt_path.touch()

    state = {"curriculum_path": str(pdf_path), "job_path": str(txt_path)}

    result = validate_inputs(state)
    assert result.get("is_valid") is True
    assert result.get("error_message") is None


def test_validate_inputs_failure(tmp_path):
    # Fails because files don't exist
    state = {
        "curriculum_path": str(tmp_path / "curriculo.pdf"),
        "job_path": str(tmp_path / "vaga.txt"),
    }

    result = validate_inputs(state)
    assert result.get("is_valid") is False
    assert "não encontrado" in result.get("error_message", "").lower()


class FakeResult:
    def __init__(self, content):
        self.content = content


from langchain_core.runnables import RunnableLambda


class FakeResult:
    def __init__(self, content):
        self.content = content


def test_extract_score_regex(mocker):
    # Mocking get_llm with a LangChain Runnable to support the | operator
    mock_llm = RunnableLambda(
        lambda x: FakeResult("# Análise\nScore: 85\nE mais texto aqui.")
    )
    mocker.patch("graph.nodes.get_llm", return_value=mock_llm)

    state = {"extracted_information": {"candidato": {}, "vaga": {}}}

    result = analyze_match(state)
    assert result.get("compatibility_score") == 85
    assert "Análise" in result.get("analysis")
