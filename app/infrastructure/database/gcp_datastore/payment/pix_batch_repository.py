import datetime
from typing import Optional
from google.cloud import datastore

from app.domain.entities.pix_batch_entity import PixBatchEntity
from app.infrastructure.database.gcp_datastore.config.connection import GCPDatastoreConnection
from app.services.repositories.contracts.pix_batch_repository_contract import PixBatchRepositoryContract


class PixBatchRepository(PixBatchRepositoryContract):
    def __init__(self, connection: datastore.client.Client):
        self.__db_client: datastore.client.Client = connection
        self.__namespace: str = 'payment'
        self.__kind: str = 'PixBatch'

    def __get_ndb_key(self, id: Optional[str | int] = None) -> datastore.key.Key:
        if id is None:
            return self.__db_client.key(self.__kind, namespace=self.__namespace)

        if isinstance(id, str) and id.isnumeric():
            id = int(id)

        return self.__db_client.key(self.__kind, id, namespace=self.__namespace)

    def get_pix_batch_by_id(self, pix_batch_id: str | int) -> PixBatchEntity | None:
        pix_batch_key = self.__get_ndb_key(pix_batch_id)
        pix_batch = self.__db_client.get(pix_batch_key)

        if pix_batch:
            return PixBatchEntity(pix_batch)

        return None

    def create_new_pix_batch(self, title: str, description: str = None) -> PixBatchEntity | None:
        data = PixBatchEntity()
        data.title = title
        data.description = description

        return self.__insert_pix_batch(data)

    def update_pix_batch_total(self, pix_batch_id: str | int, total_items: int, total_amount: float) -> PixBatchEntity | None:
        pix_batch_key = self.__get_ndb_key(pix_batch_id)
        pix_batch_entity = self.__db_client.get(pix_batch_key)

        if pix_batch_entity:
            try:
                pix_batch_entity["total_items"] = total_items
                pix_batch_entity["total_amount"]  = total_amount
                pix_batch_entity["timestamp_updated"] = datetime.datetime.utcnow()

                self.__db_client.put(pix_batch_entity)
            except:
                return None

        return PixBatchEntity(pix_batch_entity)

    def __insert_pix_batch(self, data: PixBatchEntity) -> PixBatchEntity | None:
        pix_batch_key = self.__get_ndb_key()
        pix_batch_entity = datastore.Entity(pix_batch_key)

        try:
            pix_batch_entity["title"] = data.title
            pix_batch_entity["description"] = data.description
            pix_batch_entity["timestamp_created"] = data.timestamp_created
            pix_batch_entity["timestamp_updated"] = data.timestamp_updated
            pix_batch_entity["status"] = data.status
            pix_batch_entity["total_items"] = data.total_items
            pix_batch_entity["total_amount"]  = data.total_amount
            pix_batch_entity["total_failures"] = data.total_failures
            pix_batch_entity["total_amount_failure"] = data.total_amount_failure
            pix_batch_entity["retries"] = data.retries

            self.__db_client.put(pix_batch_entity)

            return PixBatchEntity(pix_batch_entity)
        except:
            return None
