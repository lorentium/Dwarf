import typer
from dwarf.processor import process_csv

app = typer.Typer(help="Dwarf: Herramienta CLI para identificar repositorios con GitHub Agentic Workflows.")

@app.command()
def main(
    input_file: str = typer.Argument(..., help="Ruta al archivo CSV de entrada con los repositorios candidatos."),
    output: str = typer.Option("repositorios_ghaw.csv", "--output", "-o", help="Ruta del archivo CSV de salida.")
):
    """
    Procesa un CSV de entrada y genera un nuevo CSV con los repositorios que usan GH-AW.
    Soporta pausar con Ctrl+C y reanudar automáticamente.
    """
    typer.echo(f"Procesando {input_file}... (Presiona Ctrl+C en cualquier momento para pausar)\n")

    try:
        count, interrupted = process_csv(input_file, output)

        if interrupted:
            typer.echo("Proceso pausado por el usuario.")
            typer.echo(f"Avance guardado en: {output}")
            typer.echo("Ejecuta el mismo comando nuevamente para reanudar desde donde quedaste.")
        else:
            typer.echo(" Proceso completado exitosamente.")
            typer.echo(f"Se encontraron {count} repositorios con GitHub Agentic Workflows.")
            typer.echo(f"Resultado final guardado en: {output}")

    except Exception as e:
        typer.echo(f"Error procesando el archivo: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()