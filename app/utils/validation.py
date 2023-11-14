"""
    Conjunto de funções de validação comuns amplamente utilizadas na aplicação.

"""
from typing import Any
import re

# TODO: Implementação foi feita de forma muito simplista e merece melhorias


def is_amount_valid(amount: Any) -> bool:
    prop_type = type(amount)
    if prop_type == str:
        try:
            float(amount)
            return True
        except:
            return False
    elif prop_type == int:
        return True
    elif prop_type == float:
        return amount.is_integer()

    return False

def is_pix_identifier_valid(identifer: Any) -> bool:
    return True # TODO: Implementar

def is_txid_valid(txId: Any) -> bool:
    if type(txId) != str:
        return False

    return re.match(r'^[a-zA-Z0-9]{1,35}$', txId)

def is_pix_key_type_valid(pix_type: Any) -> bool:
    if type(pix_type) != str:
        return False

    return pix_type in ['cnpj', 'cpf', 'email', 'phone', 'evp']

def is_pix_key_valid(pix_key_type: str | None, pix_key: Any) -> bool:
    if type(pix_key) != str:
        return False

    if pix_key_type is None:
        pix_key_type = detect_pix_key(pix_key)
        return pix_key_type is not None

    if pix_key_type == 'cnpj':
        return is_cnpj_valid(pix_key)
    if pix_key_type == 'cpf':
        return is_cpf_valid(pix_key)
    if pix_key_type == 'email':
        return is_email_valid(pix_key)
    if pix_key_type == 'phone':
        return is_pix_phone_key_valid(pix_key)
    if pix_key_type == 'evp':
        return is_pix_evp_key_valid(pix_key)

    return False


def is_cpf_valid(cpf: str) -> bool:
    if not cpf:
        return False

    cpf = cpf.replace('.', '').replace('-', '')
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    # TODO: Implementar validação dos dígitos de controle.

    return True

def is_cnpj_valid(cnpj: str) -> bool:
    if not cnpj:
        return False

    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    if len(cnpj) != 14 or not cnpj.isdigit():
        return False

    # TODO: Implementar validação dos dígitos de controle.

    return True

def is_cpf_or_cnpj_valid(document: str) -> bool:
    return is_cnpj_valid(document) or is_cpf_valid(document)

def is_email_valid(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    return re.match(pattern, email) is not None

def is_pix_phone_key_valid(phone: str) -> bool:
    return True # TODO: implementar

def is_pix_evp_key_valid(phone: str) -> bool:
    pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    return re.match(pattern, phone) is not None

def detect_pix_key(pix_key: Any):
    if type(pix_key) != str or not pix_key:
        return None

    if is_cnpj_valid(pix_key):
        return 'cnpj'
    if is_cpf_valid(pix_key):
        return 'cpf'
    if is_email_valid(pix_key):
        return 'email'
    if is_pix_phone_key_valid(pix_key):
        return 'phone'
    if is_pix_evp_key_valid(pix_key):
        return 'evp'

    return None


def is_account_branch_valid(branch: Any) -> bool:
     # TODO: Implementar
    if isinstance(branch, str):
        return True

    if isinstance(branch, int):
        return True

    return False

def is_account_number_valid(acc_number: Any) -> bool:
     # TODO: Implementar
    if isinstance(acc_number, str):
        return True

    if isinstance(acc_number, int):
        return True

    return False

def is_account_type_valid(acc_type: Any) -> bool:
     # TODO: Implementar
    if isinstance(acc_type, str):
        return True

    if isinstance(acc_type, int):
        return True

    return False
