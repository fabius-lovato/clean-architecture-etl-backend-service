from pydantic import BaseModel
from fastapi import Body


class BadRequestError(BaseModel):
    field: str    = Body(None, description='Nome da propriedade onde a inconsistência foi detectada.')
    message: str  = Body(...,  description='Descrição resumida do erro ou inconsistência.')
    details: str  = Body(None, description='Informações detalhadas sobre a inconsistência.')
