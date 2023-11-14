from typing import Optional
import uuid, datetime
from google.cloud import datastore

from app.domain.entities.pix_batch_items_entity import PixBatchItemEntity
from app.infrastructure.database.gcp_datastore.config.connection import GCPDatastoreConnection
from app.services.repositories.contracts.pix_batch_items_repository_contract import PixBatchItemsRepositoryContract


class PixBatchItemsRepository(PixBatchItemsRepositoryContract):
    def __init__(self, connection: datastore.client.Client):
        self.__db_client: datastore.client.Client = connection
        self.__namespace: str = 'payment'
        self.__kind: str = 'PixBatchItems'

    def get_pix_batch_item_by_id(self, pix_batch_item_id: str) -> PixBatchItemEntity | None:
        pix_batch_item_key = self.__db_client.key(self.__kind, pix_batch_item_id, namespace=self.__namespace)
        pix_batch_item = self.__db_client.get(pix_batch_item_key)
        if pix_batch_item:
            return PixBatchItemEntity(pix_batch_item)

        return None

    def insert_pix_batch_item(self, pix_batch_id: int, pix_batch_item_id: PixBatchItemEntity) -> PixBatchItemEntity | None:
        pix_batch_item_key = self.__db_client.key(self.__kind, namespace=self.__namespace)
        pix_batch_item_entity = datastore.Entity(pix_batch_item_key)

        try:
            pix_batch_item_entity["pix_batch_id"] = pix_batch_id
            pix_batch_item_entity["timestamp_created"] = pix_batch_item_id.timestamp_created
            pix_batch_item_entity["timestamp_updated"] = pix_batch_item_id.timestamp_updated
            pix_batch_item_entity["status"] = pix_batch_item_id.status
            pix_batch_item_entity["amount"] = pix_batch_item_id.amount
            pix_batch_item_entity["tx_id"] = pix_batch_item_id.tx_id
            pix_batch_item_entity["pix_key"] = pix_batch_item_id.pix_key
            pix_batch_item_entity["institution"] = pix_batch_item_id.institution
            pix_batch_item_entity["branch"]  = pix_batch_item_id.branch
            pix_batch_item_entity["account_number"] = pix_batch_item_id.account_number
            pix_batch_item_entity["account_type"] = pix_batch_item_id.account_type
            pix_batch_item_entity["holder_name"] = pix_batch_item_id.holder_name
            pix_batch_item_entity["document_number"] = pix_batch_item_id.document_number
            pix_batch_item_entity["retries"] = pix_batch_item_id.retries
            pix_batch_item_entity["error_description"] = pix_batch_item_id.error_description

            self.__db_client.put(pix_batch_item_entity)

            return PixBatchItemEntity(pix_batch_item_entity)
        except:
            return None
