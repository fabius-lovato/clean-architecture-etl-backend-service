from typing import Any, Dict, Optional, List, Sequence
from pydantic import BaseModel
from fastapi import APIRouter, Request, Response, UploadFile, HTTPException, Form, Body
from enum import Enum

class PixBatchFileType(str, Enum):
    CSV  = 'CSV'
    JSON = 'JSON'
    XML  = 'XML'
    YAML = 'YAML'
    YML  = 'YML'

class PixBatchFileConfig(BaseModel):
    file: UploadFile        = Form(...,     description="Arquivo com os pagamentos Pix a serem inseridos no lote.")
    encoding: str           = Form("UTF-8", description="O parâmetro `encoding` define a codificação utilizada pelo arquivo enviado.")
    file_type: str          = Form(None,    description="Tipo e formato do arquivo de lote contendo os pagamentos PIX.")
    ignore_duplicated: bool = Form(True,    description="Opção de tratamento de pagamentos duplicados.")


class PixBatchCSVFileConfig(PixBatchFileConfig):
    delimiter: str           = Form(";",    description="Caracter utilizado como delimitador de colunas no arquivo .CSV.")
    quote_char: str          = Form('"',    description="Caracter que delimita o início e fim de uma string.")
    escape_char: str         = Form(None,   description="Especifica o caractere usado para escapar do caractere delimitador, caso as aspas não sejam usadas.")
    skip_initial_space: bool = Form(False,  description="Quando True, os espaços em branco imediatamente após o delimiter são ignorados.")
    line_terminator: str     = Form("\r\n", description="Tipo de quebra de linha utilizada no arquivo .CSV.")

class PixBatchXMLFileConfig(PixBatchFileConfig):
    pass

class PixBatchJSONFileConfig(PixBatchFileConfig):
    pass

class PixBatchYAMLFileConfig(PixBatchFileConfig):
    pass



class PixBatchFileConfigForAll(PixBatchCSVFileConfig, PixBatchXMLFileConfig, PixBatchJSONFileConfig, PixBatchYAMLFileConfig):

    @classmethod
    def as_form(
        cls,
        file: UploadFile       = Form(),
        encoding: str          = Form("UTF-8"),
        fileType: str          = Form(None),
        ignoreDuplicated: bool = Form(True),
        delimiter: str         = Form(";",  min_length=1, max_length=1),
        quoteChar: str         = Form('"',  min_length=1, max_length=1),
        escapeChar: str        = Form(None, min_length=1, max_length=1),
        skipInitialSpace: bool = Form(False),
        lineTerminator: str    = Form("\r\n")
    ):
        return cls(file=file, encoding=encoding, file_type=fileType, ignore_duplicated=ignoreDuplicated,
                   delimiter=delimiter, quote_char=quoteChar, escape_char=escapeChar, skip_initial_space=skipInitialSpace,
                   line_terminator=lineTerminator)


class PixBatchFileUploadInfo(BaseModel):
    name: str                    = Body(description="Nome do arquivo de lote enviado na requisição.")
    size: int                    = Body(description="Tamanho total do arquivo, em bytes.")
    type: PixBatchFileType       = Body(description="Formato do arquivo.")
    total_lines: int             = Body(description="Quantia total de linhas que o arquivo possui.", alias="TotalLines")

class PixBatchFilePostResponse(BaseModel):
    file: PixBatchFileUploadInfo = Body(description="Informações sobre o arquivo enviado na requisição.")
    total_count: int             = Body(description="Quantidade total de pagamentos pagamentos Pix encontrados no arquivo.", gt=0.01, alias="totalCount")
    total_amount: float          = Body(description="Montante total de todos os pagamentos Pix.",                            gt=0.01, alias="totalAmount")


class PixBatchFileErroItem(BaseModel):
    fileline: int                = Body(description="Número da linha no arquivo onde foi encontrado inconsistências.")
    index: int                   = Body(description="Índice do pagamento Pix dentro do arquivo.")
    field: str                   = Body(description="Nome do campo, coluna ou elemento onde foi encontrado a inconsistência.")
    description: str             = Body(description="Descritivo do erro ou inconsistência encontrada.")

class PixBatchFileErrorResponse(BaseModel):
    file: PixBatchFileUploadInfo       = Body(description="Informações sobre o arquivo enviado na requisição.")
    total_error_count: int             = Body(description="Quantidade total de inconsistências e erros encontrados em todo o arquivo.", gt=0, alias="totalErrorCount")
    errors: List[PixBatchFileErroItem] = Body(description="Primeiros 100 erros encontrados.", )
