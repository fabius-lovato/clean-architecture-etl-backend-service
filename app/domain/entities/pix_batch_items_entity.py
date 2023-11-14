import datetime
from typing import Optional


class PixBatchItemEntity():

    def __init__(self, entity = None):
        self.timestamp_created: str           = datetime.datetime.utcnow()
        self.timestamp_updated: str           = datetime.datetime.utcnow()
        self.status: str                      = 'pending'
        self.amount: float                    = 0.0
        self.description: Optional[str]       = None
        self.tx_id: Optional[str]             = None
        self.pix_key: Optional[str]           = None
        self.institution: Optional[str]       = None
        self.branch: Optional[str]            = None
        self.account_number: Optional[str]    = None
        self.account_type: Optional[str]      = None
        self.holder_name: Optional[str]       = None
        self.document_number: Optional[str]   = None
        self.identifier: Optional[str]        = None
        self.retries: int                     = 0
        self.error_description: Optional[str] = None

        if entity:
            self.timestamp_created: str           = getattr(entity, 'timestamp_created', self.timestamp_created)
            self.timestamp_updated: str           = getattr(entity, 'timestamp_updated', self.timestamp_updated)
            self.status: str                      = getattr(entity, 'status', self.status)
            self.amount: float                    = getattr(entity, 'amount', self.amount)
            self.description: Optional[str]       = getattr(entity, 'description', self.description)
            self.tx_id: Optional[str]             = getattr(entity, 'tx_id', self.tx_id)
            self.pix_key: Optional[str]           = getattr(entity, 'pix_key', self.pix_key)
            self.institution: Optional[str]       = getattr(entity, 'institution', self.institution)
            self.branch: Optional[str]            = getattr(entity, 'branch', self.branch)
            self.account_number: Optional[str]    = getattr(entity, 'account_number', self.account_number)
            self.account_type: Optional[str]      = getattr(entity, 'account_type', self.account_type)
            self.holder_name: Optional[str]       = getattr(entity, 'holder_name', self.holder_name)
            self.document_number: Optional[str]   = getattr(entity, 'document_number', self.document_number)
            self.identifier: Optional[str]        = getattr(entity, 'identifier', self.identifier)
            self.retries: int                     = getattr(entity, 'retries', self.retries)
            self.error_description: Optional[str] = getattr(entity, 'error_description', self.error_description)

            key = getattr(entity, 'key')
            if key:
                self.id = getattr(key, 'id') or getattr(key, 'name')
