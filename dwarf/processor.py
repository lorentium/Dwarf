import os
import json
import pandas as pd
from dwarf.repository import Repository
from dwarf.github import get_workflow_filenames
from dwarf.parser import has_github_agentic_workflows

CHECKPOINT_FILE = ".dwarf_progress.json"

def _load_progress() -> tuple[set, list]:
    """Carga el progreso previo si el archivo de punto de control existe."""
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("processed", [])), data.get("valid_rows", [])
        except Exception:
            pass
    return set(), []

def _save_progress(processed: set, valid_rows: list):
    """Guarda en disco los repositorios ya evaluados y las coincidencias encontradas."""
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump({"processed": list(processed), "valid_rows": valid_rows}, f, indent=2)

def _cleanup_progress():
    """Borra el punto de control cuando el proceso termina al 100%."""
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)

def process_csv(input_path: str, output_path: str) -> tuple[int, bool]:
    """
    Procesa el CSV permitiendo interrupción manual (Ctrl+C) y reanudación.
    Retorna (cantidad_de_coincidencias, fue_interrumpido).
    """
    df = pd.read_csv(input_path)
    processed_repos, valid_rows = _load_progress()
    interrupted = False

    try:
        for index, row in df.iterrows():
            raw_name = str(row.get("name", "")).strip()

            # Omitir repositorios ya analizados en ejecuciones previas
            if raw_name in processed_repos:
                continue

            try:
                repo = Repository(name=raw_name)
                filenames = get_workflow_filenames(repo.name)
                print(f"Archivos en {repo.name}: {filenames}")

                if has_github_agentic_workflows(filenames):
                    valid_rows.append(row.to_dict())
            except Exception:
                pass
            finally:
                # Marcar como procesado independientemente del resultado
                processed_repos.add(raw_name)
                _save_progress(processed_repos, valid_rows)

    except KeyboardInterrupt:
        interrupted = True

    # Guardar los avances en el CSV de salida
    if valid_rows:
        result_df = pd.DataFrame(valid_rows)
    else:
        result_df = pd.DataFrame(columns=df.columns)

    result_df.to_csv(output_path, index=False)

    # Si completado sin interrupciones, se borra el archivo temporal de progreso
    if not interrupted:
        _cleanup_progress()

    return len(result_df), interrupted