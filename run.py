"""Launcher para CurriculoMatch AI - inicia API e Streamlit simultaneamente.

Uso:
    python run.py              # Inicia tudo
    python run.py --api-only   # Somente API
    python run.py --web-only   # Somente Streamlit
    python run.py --install    # Apenas instala dependencias
"""

import argparse
import signal
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).parent
VENV_DIR = ROOT / ".venv"
REQUIREMENTS = ROOT / "requirements.txt"


def get_python() -> str:
    """Retorna o caminho do Python do venv."""
    if sys.platform == "win32":
        return str(VENV_DIR / "Scripts" / "python.exe")
    return str(VENV_DIR / "bin" / "python")


def get_pip() -> str:
    """Retorna o caminho do pip do venv."""
    if sys.platform == "win32":
        return str(VENV_DIR / "Scripts" / "pip.exe")
    return str(VENV_DIR / "bin" / "pip")


def ensure_venv() -> None:
    """Cria o venv e instala dependencias se necessario."""
    if not VENV_DIR.exists():
        print("[run] Criando ambiente virtual...")
        venv.create(str(VENV_DIR), with_pip=True)
        print(f"[run] Venv criado em {VENV_DIR}")

    pip = get_pip()
    python = get_python()

    # Verificar se requirements esta instalado
    result = subprocess.run(
        [python, "-c", "import streamlit; import fastapi; import langgraph"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print("[run] Instalando dependencias...")
        subprocess.run(
            [pip, "install", "-r", str(REQUIREMENTS), "-q"],
            check=True,
        )
        print("[run] Dependencias instaladas.")


def start_api() -> subprocess.Popen:
    """Inicia a API FastAPI com uvicorn."""
    python = get_python()
    print("[run] API iniciando em http://localhost:8001")
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        )
    return subprocess.Popen(
        [
            python,
            "-m",
            "uvicorn",
            "api.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8001",
        ],
        cwd=str(ROOT),
        **kwargs,
    )


def start_streamlit() -> subprocess.Popen:
    """Inicia o Streamlit."""
    python = get_python()
    print("[run] Streamlit iniciando em http://localhost:8501")
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        )
    return subprocess.Popen(
        [python, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"],
        cwd=str(ROOT),
        **kwargs,
    )


def stop_process(proc: subprocess.Popen, name: str) -> None:
    """Para um processo graceful, com fallback para kill."""
    if proc.poll() is None:
        print(f"[run] Parando {name}...")
        try:
            if sys.platform == "win32":
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=5)
        except (subprocess.TimeoutExpired, OSError):
            proc.kill()
            proc.wait()
        print(f"[run] {name} parado.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="CurriculoMatch AI",
        description="Inicia API e Streamlit simultaneamente.",
    )
    parser.add_argument("--api-only", action="store_true", help="Iniciar somente a API")
    parser.add_argument(
        "--web-only", action="store_true", help="Iniciar somente o Streamlit"
    )
    parser.add_argument(
        "--install", action="store_true", help="Apenas instalar dependencias"
    )
    args = parser.parse_args()

    # Carregar .env
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")

    # Garantir venv + deps
    ensure_venv()

    if args.install:
        print("[run] Dependencias instaladas com sucesso.")
        return

    processes: list[tuple[subprocess.Popen, str]] = []

    def cleanup(signum=None, frame=None):
        print("\n[run] Encerrando...")
        for proc, name in processes:
            stop_process(proc, name)
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        if not args.web_only:
            api_proc = start_api()
            processes.append((api_proc, "API"))

        if not args.api_only:
            st_proc = start_streamlit()
            processes.append((st_proc, "Streamlit"))

        print("\n[run] Servidores rodando. Pressione Ctrl+C para parar.\n")

        # Aguardar (bloqueia ate Ctrl+C ou crash)
        while processes:
            for proc, name in processes[:]:
                if proc.poll() is not None:
                    print(
                        f"[run] {name} encerrou inesperadamente (code={proc.returncode})"
                    )
                    processes.remove((proc, name))

            if not processes:
                break

            _sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


def _sleep(seconds: int) -> None:
    """Fallback para signal.pause no Windows."""
    import time

    time.sleep(seconds)


if __name__ == "__main__":
    main()
