import datetime
from typing import Optional


class PixBatchEntity():

    def __init__(self, entity = None):
        self.title: str                  = None
        self.description: Optional[str]  = None
        self.timestamp_created: str      = datetime.datetime.utcnow()
        self.timestamp_updated: str      = datetime.datetime.utcnow()
        self.status: str                 = 'pending'
        self.total_items: int            = 0
        self.total_amount: float         = 0.0
        self.total_failures: int         = 0
        self.total_amount_failure: float = 0.0
        self.retries: int                = 0

        if entity:
            self.title                = getattr(entity, 'title', self.title)
            self.description          = getattr(entity, 'description', self.description)
            self.timestamp_created    = getattr(entity, 'timestamp_created', self.timestamp_created)
            self.timestamp_updated    = getattr(entity, 'timestamp_updated', self.timestamp_updated)
            self.status               = getattr(entity, 'status', self.status)
            self.total_items          = getattr(entity, 'total_items', self.total_items)
            self.total_amount         = getattr(entity, 'total_amount', self.total_amount)
            self.total_failures       = getattr(entity, 'total_failures', self.total_failures)
            self.total_amount_failure = getattr(entity, 'total_amount_failure', self.total_amount_failure)
            self.retries              = getattr(entity, 'retries', self.retries)

            key = getattr(entity, 'key')
            if key:
                self.id = getattr(key, 'id') or getattr(key, 'name')


    def is_pending(self) -> bool:
        return self.status == 'pending'
