import pytest

from tools.job_reader import read_job
from tools.pdf_reader import read_curriculum
from tools.report_writer import save_report


def test_pdf_reader_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_curriculum("caminho_inexistente.pdf")


def test_job_reader_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_job("caminho_inexistente.txt")


def test_save_report(tmp_path):
    content = "# Test Report\nSuccess!"
    output_path = tmp_path / "test_report.md"
    success = save_report(content, str(output_path))

    assert success is True
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == content
