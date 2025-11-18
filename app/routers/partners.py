from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.database.mongo import partners_collection
from app.schemas.business_partner import BusinessPartner
from app.utils.helpers import bp_from_mongo, object_id_or_400
from app.utils.response import api_success, api_error, build_pagination

router = APIRouter(
    prefix="/partners",
    tags=["Business Partners"]
)


# ---------------------
# CREATE
# ---------------------

@router.post("", response_model=None)
def create_partner(partner: BusinessPartner):
    data = partner.dict(exclude={"id", "avg_transaction_value"})

    # auto compute avg
    if data.get("transaction_count", 0) > 0:
        data["avg_transaction_value"] = data["total_transaction_amount"] / max(data["transaction_count"], 1)
    else:
        data["avg_transaction_value"] = 0

    result = partners_collection.insert_one(data)
    new_doc = partners_collection.find_one({"_id": result.inserted_id})

    return api_success(bp_from_mongo(new_doc), message="Partner created")



# ---------------------
# LIST + PAGINATION
# ---------------------

@router.get("", response_model=None)
def list_partners(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    business_type: Optional[str] = None,
    customer_level: Optional[str] = None,
    funnel_stage: Optional[str] = None,
    credit_status: Optional[str] = None,
    potential: Optional[str] = None,
    payment_type: Optional[str] = None,
):
    skip = (page - 1) * limit

    # داینامیک query builder
    query = {}

    if business_type:
        query["business_type"] = business_type

    if customer_level:
        query["customer_level"] = customer_level

    if funnel_stage:
        query["funnel_stage"] = funnel_stage

    if credit_status:
        query["credit_status"] = credit_status

    if potential:
        query["potential"] = potential

    if payment_type:
        query["payment_type"] = payment_type

    total = partners_collection.count_documents(query)
    cursor = partners_collection.find(query).skip(skip).limit(limit)
    partners = [bp_from_mongo(d) for d in cursor]
    pagination = build_pagination(page, limit, total)
    return api_success(partners, "List of partners", pagination=pagination)

# ---------------------
# GET ONE
# ---------------------

@router.get("/{partner_id}", response_model=None)
def get_partner(partner_id: str):
    oid = object_id_or_400(partner_id)

    doc = partners_collection.find_one({"_id": oid})
    if not doc:
        return api_error("Partner not found", "404")

    return api_success(bp_from_mongo(doc))


# ---------------------
# UPDATE
# ---------------------

@router.put("/{partner_id}", response_model=None)
def update_partner(partner_id: str, partner: BusinessPartner):

    oid = object_id_or_400(partner_id)
    existing = partners_collection.find_one({"_id": oid})

    if not existing:
        return api_error("Partner not found", "404")

    update_data = partner.model_dump(exclude={"id"}, exclude_unset=True)

    # trim
    for k, v in update_data.items():
        if isinstance(v, str):
            update_data[k] = v.strip()

    partners_collection.update_one({"_id": oid}, {"$set": update_data})

    updated = partners_collection.find_one({"_id": oid})
    return api_success(bp_from_mongo(updated), "Updated")


# ---------------------
# DELETE
# ---------------------

@router.delete("/{partner_id}", response_model=None)
def delete_partner(partner_id: str):
    oid = object_id_or_400(partner_id)
    result = partners_collection.delete_one({"_id": oid})

    if result.deleted_count == 0:
        return api_error("Partner not found", "404")

    return api_success(True, "Deleted")

# ---------------------
# FULL TEXT SEARCH + PAGINATION
# ---------------------

# اگر /search بدون / آمد → ریدایرکت شود به /search/
@router.get("/search", include_in_schema=False)
def redirect_search(
    q: Optional[str] = None,
    business_type: Optional[str] = None,
    funnel_stage: Optional[str] = None,
    customer_level: Optional[str] = None,
    page: int = 1,
    limit: int = 20
):
    from fastapi.responses import RedirectResponse

    params = []
    if q: params.append(f"q={q}")
    if business_type: params.append(f"business_type={business_type}")
    if funnel_stage: params.append(f"funnel_stage={funnel_stage}")
    if customer_level: params.append(f"customer_level={customer_level}")
    params.append(f"page={page}")
    params.append(f"limit={limit}")

    qs = "&".join(params)
    return RedirectResponse(f"/crm-api/partners/search/?{qs}", status_code=307)


@router.get("/search/", response_model=None)
def search_partners(
    q: Optional[str] = None,
    business_type: Optional[str] = None,
    funnel_stage: Optional[str] = None,
    customer_level: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    query = {}

    if q:
        query["$text"] = {"$search": q.strip()}

    if business_type:
        query["business_type"] = business_type

    if funnel_stage:
        query["funnel_stage"] = funnel_stage

    if customer_level:
        query["customer_level"] = customer_level

    skip = (page - 1) * limit
    total = partners_collection.count_documents(query)

    # fulltext score ranking
    if q:
        cursor = partners_collection.find(query, {"score": {"$meta": "textScore"}})
        cursor = cursor.sort([("score", {"$meta": "textScore"})])
    else:
        cursor = partners_collection.find(query)

    cursor = cursor.skip(skip).limit(limit)

    partners = [bp_from_mongo(d) for d in cursor]
    pagination = build_pagination(page, limit, total)

    return api_success(partners, "Search results", pagination=pagination)
