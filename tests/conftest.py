import sys
from pathlib import Path

# Adicionar o diretorio raiz ao path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
