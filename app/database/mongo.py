from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import OperationFailure

MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)
db = client["crm_db"]

partners_collection = db["business_partners"]


def ensure_indexes():
    """
    ایجاد ایندکس‌ها در صورت عدم وجود.
    اگر از قبل ساخته شده باشند، دوباره ساخته نمی‌شوند.
    """

    existing_indexes = {idx["name"] for idx in partners_collection.list_indexes()}

    # ایندکس فول‌تکست
    if "text_search_index" not in existing_indexes:
        try:
            partners_collection.create_index(
                [
                    ("brand_name", TEXT),
                    ("manager_full_name", TEXT),
                    ("tags", TEXT),
                    ("category", TEXT),
                    ("sub_category", TEXT),
                    ("notes", TEXT),
                    ("customer_type", TEXT),
                ],
                name="text_search_index",
                # MongoDB زبان "persian" ندارد؛
                # برای فارسی معمولاً بهتر است از "none" استفاده کنیم.
                default_language="none",
            )
        except OperationFailure as e:
            # اگر به هر دلیلی باز هم خطا داد، لاگ کن و ادامه بده
            print("Failed to create text index:", e)

    # ایندکس‌های ساده روی فیلدهای مهم برای فیلتر کردن

    if "business_type_index" not in existing_indexes:
        partners_collection.create_index(
            [("business_type", ASCENDING)],
            name="business_type_index",
        )

    if "customer_level_index" not in existing_indexes:
        partners_collection.create_index(
            [("customer_level", ASCENDING)],
            name="customer_level_index",
        )

    if "funnel_stage_index" not in existing_indexes:
        partners_collection.create_index(
            [("funnel_stage", ASCENDING)],
            name="funnel_stage_index",
        )

    if "credit_status_index" not in existing_indexes:
        partners_collection.create_index(
            [("credit_status", ASCENDING)],
            name="credit_status_index",
        )

    if "purchase_probability_index" not in existing_indexes:
        partners_collection.create_index(
            [("purchase_probability", ASCENDING)],
            name="purchase_probability_index",
        )

    print("✅ MongoDB indexes ensured.")


# اجرای ایندکس‌ها هنگام import
ensure_indexes()
