from fastapi import APIRouter, Query

from app.utils.helpers import object_id_or_400
from app.utils.response import api_success, api_error, build_pagination

from app.schemas.partner_quick_entry import PartnerQuickEntry
from app.schemas.partner_relationship import PartnerRelationshipUpdate
from app.schemas.partner_analysis import PartnerAnalysisUpdate
from app.schemas.partner_financial_estimation import PartnerFinancialEstimationUpdate
from app.schemas.partner_acquisition import PartnerAcquisitionUpdate

from app.models.partner import Partner, Identity, Relationship, Analysis
from app.repositories.partner_repository import PartnerRepository


router = APIRouter(
    prefix="/partners",
    tags=["Partners"]
)


# --------------------------------------------------
# Quick Entry
# --------------------------------------------------

@router.post("/quick-entry")
def quick_entry(payload: PartnerQuickEntry):
    """
    ورود سریع مخاطب (کارت ویزیت / اکسل / لید)
    فقط brand_name اجباری است
    """

    partner = Partner(
        identity=Identity(
            brand_name=payload.brand_name,                 # ✅ تنها الزام
            manager_full_name=payload.manager_full_name,
            business_type=payload.business_type,

            # ⬇️ مهم: هیچ چیز اجباری نیست
            contact_numbers=payload.contact_numbers or [],
            social_links=[],  # quick-entry اصلاً شبکه اجتماعی نمی‌خواهد

            province=payload.province,
            city=payload.city,
            full_address=None,
            location=payload.location,
        ),
        relationship=Relationship(
            notes=payload.notes
        ),
        analysis=Analysis()  # funnel_stage = prospect
    )

    repo = PartnerRepository()
    created = repo.create(partner)

    return api_success(created, "Partner created")

# --------------------------------------------------
# Get Partner
# --------------------------------------------------
@router.get("/{partner_id}")
def get_partner(partner_id: str):
    """
    دریافت پروفایل کامل یک مخاطب / مشتری
    """

    oid = object_id_or_400(partner_id)

    repo = PartnerRepository()
    partner = repo.get_by_id(str(oid))

    if not partner:
        return api_error("Partner not found", 404)

    return api_success(partner)


# --------------------------------------------------
# Generic update helper
# --------------------------------------------------
def update_nested_field(
    partner_id: str,
    payload,
    prefix: str,
    success_message: str
):
    oid = object_id_or_400(partner_id)

    update_data = {
        f"{prefix}.{field}": value
        for field, value in payload.model_dump(exclude_unset=True).items()
    }

    if not update_data:
        return api_error("No data provided for update", 400)

    repo = PartnerRepository()
    updated = repo.update(str(oid), update_data)

    if not updated:
        return api_error("Partner not found", 404)

    return api_success(updated, success_message)


# --------------------------------------------------
# Relationship
# --------------------------------------------------
@router.patch("/{partner_id}/relationship")
def update_relationship(
    partner_id: str,
    payload: PartnerRelationshipUpdate
):
    """
    بروزرسانی وضعیت ارتباط انسانی با مخاطب
    """
    return update_nested_field(
        partner_id,
        payload,
        prefix="relationship",
        success_message="Relationship updated"
    )


# --------------------------------------------------
# Analysis
# --------------------------------------------------
@router.patch("/{partner_id}/analysis")
def update_analysis(
    partner_id: str,
    payload: PartnerAnalysisUpdate
):
    """
    بروزرسانی وضعیت تحلیلی (Upgrade لید / سگمنت‌بندی)
    """
    return update_nested_field(
        partner_id,
        payload,
        prefix="analysis",
        success_message="Analysis updated"
    )


# --------------------------------------------------
# Financial Estimation
# --------------------------------------------------
@router.patch("/{partner_id}/financial-estimation")
def update_financial_estimation(
    partner_id: str,
    payload: PartnerFinancialEstimationUpdate
):
    """
    بروزرسانی اطلاعات مالی تخمینی
    """
    return update_nested_field(
        partner_id,
        payload,
        prefix="financial_estimation",
        success_message="Financial estimation updated"
    )


# --------------------------------------------------
# Acquisition
# --------------------------------------------------
@router.patch("/{partner_id}/acquisition")
def update_acquisition(
    partner_id: str,
    payload: PartnerAcquisitionUpdate
):
    """
    بروزرسانی منبع آشنایی مخاطب
    """
    return update_nested_field(
        partner_id,
        payload,
        prefix="acquisition",
        success_message="Acquisition updated"
    )


# --------------------------------------------------
# List & Search
# --------------------------------------------------
@router.get("")
def list_partners(
    funnel_stage: str | None = Query(None),
    business_type: str | None = Query(None),
    financial_level: str | None = Query(None),
    purchase_readiness: str | None = Query(None),
    potential_level: str | None = Query(None),
    acquisition_source: str | None = Query(None),
    province: str | None = Query(None),
    city: str | None = Query(None),
    map_link: str | None = Query(None),
    tag: str | None = Query(None),
    page: int = 1,
    limit: int = 20,
):
    """
    لیست و جستجوی مخاطبین / مشتریان
    """

    filters = {
        "meta.is_deleted": False
    }

    if funnel_stage:
        filters["analysis.funnel_stage"] = funnel_stage
    if business_type:
        filters["identity.business_type"] = business_type
    if financial_level:
        filters["analysis.financial_level"] = financial_level
    if purchase_readiness:
        filters["analysis.purchase_readiness"] = purchase_readiness
    if potential_level:
        filters["analysis.potential_level"] = potential_level
    if acquisition_source:
        filters["acquisition.source"] = acquisition_source
    if province:
        filters["identity.province"] = province
    if city:
        filters["identity.city"] = city
    if map_link:
        filters["identity.map_link"] = map_link
    if tag:
        filters["analysis.tags"] = tag

    repo = PartnerRepository()
    partners, total = repo.list(filters, page, limit)

    pagination = build_pagination(page, limit, total)

    return api_success(partners, pagination=pagination)


# --------------------------------------------------
# Soft Delete
# --------------------------------------------------
@router.delete("/{partner_id}")
def delete_partner(partner_id: str):
    """
    حذف مخاطب (Soft Delete)
    """

    oid = object_id_or_400(partner_id)

    repo = PartnerRepository()
    success = repo.soft_delete(str(oid))

    if not success:
        return api_error("Partner not found or already deleted", 404)

    return api_success(None, "Partner deleted successfully")


from app.schemas.partner_identity import PartnerIdentityUpdate


@router.patch("/{partner_id}/identity")
def update_identity(partner_id: str, payload: PartnerIdentityUpdate):
    """
    بروزرسانی اطلاعات هویتی پایه مخاطب
    """

    oid = object_id_or_400(partner_id)

    update_data = {}
    for field, value in payload.model_dump(exclude_unset=True).items():
        update_data[f"identity.{field}"] = value

    if not update_data:
        return api_error("No data provided for update")

    repo = PartnerRepository()
    updated = repo.update(str(oid), update_data)

    if not updated:
        return api_error("Partner not found", 404)

    return api_success(updated, "Identity updated")

