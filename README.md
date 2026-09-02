# Dwarf
Detection & Workflow Agentic Repository Finder

**Dwarf** es una herramienta de línea de comandos (CLI) desarrollada en Python para automatizar la identificación de repositorios de GitHub que implementan **GitHub Agentic Workflows (GH-AW)**.

## Características Principales

- **Detección Automática:** Identifica pares de archivos de flujo de trabajo (`<nombre>.md` y `<nombre>.lock.yml`) dentro del directorio `.github/workflows/`.
- **Ejecución Reanudable:** Permite pausar el análisis en cualquier momento mediante `Ctrl + C` y continuar desde el último repositorio procesado sin perder el progreso.
- **Validación de Datos:** Valida la estructura de los repositorios (`propietario/repositorio`) mediante esquemas estrictos con Pydantic.
- **Tolerancia a Límites:** Soporta autenticación por token para evitar restricciones de tasa (Rate Limit) de la API de GitHub.

## Requisitos Previos

- Python 3.10 o superior.
- Un token de acceso personal de GitHub (*opcional, pero recomendado*).

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/lorentium/Dwarf.git](https://github.com/lorentium/Dwarf.git)
   cd Dwarf

2. **Crear y activar el entorno virtual:**

    ```bash
    python -m venv .venv
    # En Windows (PowerShell):
    .venv\Scripts\Activate.ps1

    # En Linux / macOS:
    source .venv/bin/activate

3. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt

4. **Copiar variables de entorno:**
    Copia el archivo de ejemplo .env.example a .env y añade tu token de GitHub:
    ```bash
    cp .env.example .env
    ```
    
    Edita .env:
    ```bash
    GITHUB_TOKEN=tu_github_token_aqui

## Uso de la aplicación
Para ejecutar el análisis sobre un archivo CSV con una lista de repositorios:
```bash
python -m dwarf.cli ruta/a/tu_archivo.csv -o salida.csv
```

### Pausar y reanudar la ejecución
- **pausar**: presiona `Ctrl + C` en la terminal. El progreso actual se guardará automáticamente en .dwarf_progress.json y los resultados parciales se volcarán en el CSV de salida.
- **Reanudar**: Vuelve a ejecutar el mismo comando. La aplicación detectará el archivo de progreso y omitirá automáticamente los repositorios previamente analizados.


## Formato de CSV de entrada
El archivo de entrada debe incluir una columna obligatoria llamada ```name``` con el formato ```propietario/repositorio```:

```plaintext
name
microsoft/vscode
langchain-ai/langchain
elastic/elasticsearch
```

## Estructura del proyecto

```plaintext
Dwarf/
├── dwarf/
│   ├── __init__.py
│   ├── cli.py          # Interfaz de línea de comandos (Typer)
│   ├── requirements.py       # Validaciones de modelos de datos (Pydantic)
│   ├── github.py       # Cliente de conexión a la API de GitHub (HTTPX)
│   ├── parser.py       # Lógica pura de detección de GH-AW
│   └── processor.py    # Orquestación de lectura/escritura CSV y control de checkpoints
├── tests/
│   └── test_parser.py  # Pruebas unitarias para la lógica de detección
├── .env.example        # Plantilla de variables de entorno
├── .gitignore          # Exclusión de archivos sensibles y temporales
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación principal
