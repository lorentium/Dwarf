from pydantic import BaseModel, field_validator



class Repository(BaseModel):
    
    """
    Modelo para representar y validar un repositorio de GitHub.
    """
    name: str

    @field_validator("name")
    @classmethod
    def validate_repo_name(cls, value: str) -> str:
        value = value.strip()
        if "/" not in value or len(value.split("/")) != 2:
            raise ValueError(f"Invalid repository name format: '{value}'. Expected 'owner/repo'.")
        return value
    
    