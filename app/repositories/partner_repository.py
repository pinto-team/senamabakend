from datetime import datetime
from typing import Optional, List, Tuple
from bson import ObjectId
from pymongo.collection import Collection

from app.models.partner import Partner
from app.database.mongo import get_partners_collection


class PartnerRepository:
    """
    Repository برای کار با MongoDB
    - فقط دیتابیس
    - بدون منطق بیزینسی
    """

    def __init__(self, collection: Optional[Collection] = None):
        self.collection = collection or get_partners_collection()

    # -------------------------------------------------
    # Create
    # -------------------------------------------------
    def create(self, partner: Partner) -> Partner:
        data = partner.model_dump(exclude={"id"})
        result = self.collection.insert_one(data)
        partner.id = str(result.inserted_id)
        return partner

    # -------------------------------------------------
    # Get by ID
    # -------------------------------------------------
    def get_by_id(self, partner_id: str) -> Optional[Partner]:
        try:
            oid = ObjectId(partner_id)
        except Exception:
            return None

        doc = self.collection.find_one({"_id": oid})
        if not doc:
            return None

        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return Partner(**doc)

    # -------------------------------------------------
    # Update (Partial / Nested)
    # -------------------------------------------------
    def update(self, partner_id: str, data: dict) -> Optional[Partner]:
        try:
            oid = ObjectId(partner_id)
        except Exception:
            return None

        result = self.collection.update_one(
            {"_id": oid},
            {"$set": data}
        )

        if result.matched_count == 0:
            return None

        return self.get_by_id(partner_id)

    # -------------------------------------------------
    # List + Filter + Pagination
    # -------------------------------------------------
    def list(
        self,
        filters: dict,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Partner], int]:
        """
        لیست مخاطبین با فیلتر و صفحه‌بندی
        """

        query = {}

        # فیلترهای داینامیک (nested fields)
        for key, value in filters.items():
            if value is not None:
                query[key] = value

        skip = max(page - 1, 0) * limit

        cursor = (
            self.collection
            .find(query)
            .skip(skip)
            .limit(limit)
            .sort("meta.created_at", -1)
        )

        total = self.collection.count_documents(query)

        partners: List[Partner] = []

        for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            partners.append(Partner(**doc))

        return partners, total

    def soft_delete(self, partner_id: str) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(partner_id), "meta.is_deleted": False},
            {
                "$set": {
                    "meta.is_deleted": True,
                    "meta.deleted_at": datetime.now()
                }
            }
        )

        return result.matched_count == 1