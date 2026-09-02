def has_github_agentic_workflows(filenames: list[str]) -> bool:
    """
    Evalúa si dentro de una lista de nombres de archivos existe al menos un par 
    <nombre>.md y <nombre>.lock.yml con el mismo nombre base.
    """
    file_set = set(filenames)
    md_bases = {f[:-3] for f in file_set if f.endswith('.md')}
    
    return any(f"{base}.lock.yml" in file_set for base in md_bases)