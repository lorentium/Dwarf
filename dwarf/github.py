import os
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_workflow_filenames(repo_full_name: str) -> list[str]:
    """  
    extrae la lista de nombres de archivos dentro de .github/workflows/ para un repositorio dado.
    Devuelve una lista vacía si el directorio no existe o si ocurre un error.
    """
    url = f"https://api.github.com/repos/{repo_full_name}/contents/.github/workflows"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, headers=headers)
            
            if response.status_code == 200:
                items = response.json()
                if isinstance(items, list):
                    return [item["name"] for item in items if item.get("type") == "file"]
            return []
    except httpx.RequestError:
        return []