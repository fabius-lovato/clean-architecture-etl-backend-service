from typing import Any


def is_ispb_valid(ispb: Any) -> bool:
    if type(ispb) == str:
        return True
    
    if type(ispb) == int:
        return True
    
    return False