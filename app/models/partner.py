from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


# =================================================
# Enums
# =================================================

class BusinessType(str, Enum):
    furniture_showroom = "furniture_showroom"
    furniture_manufacturer = "furniture_manufacturer"
    furniture_distributor = "furniture_distributor"


class SocialPlatform(str, Enum):
    instagram = "instagram"
    telegram = "telegram"
    whatsapp = "whatsapp"
    website = "website"
    rubika = "rubika"
    bale = "bale"
    eitaa = "eitaa"
    other = "other"


class PartnershipStatus(str, Enum):
    past = "past"
    present = "present"
    future = "future"


class CustomerRelationshipLevel(str, Enum):
    engaged = "engaged"
    normal = "normal"
    indifferent = "indifferent"


class CustomerSatisfaction(str, Enum):
    satisfied = "satisfied"
    neutral = "neutral"
    dissatisfied = "dissatisfied"


class FunnelStage(str, Enum):
    prospect = "prospect"
    lead = "lead"
    qualified = "qualified"
    customer = "customer"
    churned = "churned"


class PotentialLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class PurchaseReadiness(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class CustomerFinancialLevel(str, Enum):
    strong = "strong"
    medium = "medium"
    weak = "weak"


class AcquisitionSource(str, Enum):
    marketing = "marketing"
    self_search = "self_search"
    referral = "referral"
    instagram = "instagram"
    google = "google"
    advertising = "advertising"
    other = "other"


class CreditStatus(str, Enum):
    good = "good"
    normal = "normal"
    bad = "bad"


class PaymentType(str, Enum):
    cash = "cash"
    cheque = "cheque"
    credit = "credit"


class SensitivityType(str, Enum):
    price = "price"
    quality = "quality"
    speed = "speed"
    brand = "brand"
    other = "other"


# =================================================
# Sub Models (FLEXIBLE for both read & update)
# هدف: هیچ چیزی جز brand_name اجباری نباشد
# =================================================

class ContactNumber(BaseModel):
    label: Optional[str] = None
    number: Optional[str] = None


class SocialLink(BaseModel):
    platform: Optional[SocialPlatform] = None
    url: Optional[str] = None


class GeoLocation(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# =================================================
# Identity (Domain/Read Model)
# فقط brand_name اجباری
# =================================================

class Identity(BaseModel):
    brand_name: str

    manager_full_name: Optional[str] = None
    business_type: Optional[BusinessType] = None

    contact_numbers: List[ContactNumber] = Field(default_factory=list)
    social_links: List[SocialLink] = Field(default_factory=list)

    province: Optional[str] = None
    city: Optional[str] = None
    map_link: Optional[str] = None
    full_address: Optional[str] = None

    location: Optional[GeoLocation] = None


# =================================================
# Identity Update DTO
# فقط brand_name اجباری
# =================================================

class PartnerIdentityUpdate(BaseModel):
    """
    Update identity
    Only brand_name is required
    """

    brand_name: str  # ✅ the only required field

    manager_full_name: Optional[str] = None
    business_type: Optional[BusinessType] = None

    contact_numbers: Optional[List[ContactNumber]] = None
    social_links: Optional[List[SocialLink]] = None

    province: Optional[str] = None
    city: Optional[str] = None
    map_link: Optional[str] = None
    full_address: Optional[str] = None

    location: Optional[GeoLocation] = None


# =================================================
# Other Domain Models (همه اختیاری)
# =================================================

class Relationship(BaseModel):
    partnership_status: Optional[PartnershipStatus] = None
    customer_relationship_level: Optional[CustomerRelationshipLevel] = None
    customer_satisfaction: Optional[CustomerSatisfaction] = None

    credit_status: Optional[CreditStatus] = None
    payment_types: List[PaymentType] = Field(default_factory=list)
    sensitivity: Optional[SensitivityType] = None

    preferred_channel: Optional[SocialPlatform] = None
    notes: Optional[str] = None


class FinancialEstimation(BaseModel):
    first_transaction_date: Optional[str] = None
    first_transaction_amount_estimated: Optional[float] = None

    last_transaction_date: Optional[str] = None
    last_transaction_amount_estimated: Optional[float] = None

    total_transaction_amount_estimated: Optional[float] = None
    transaction_count_estimated: Optional[int] = None

    avg_transaction_value_estimated: Optional[float] = None
    estimation_note: Optional[str] = None


class Analysis(BaseModel):
    funnel_stage: Optional[FunnelStage] = FunnelStage.prospect
    potential_level: Optional[PotentialLevel] = None
    financial_level: Optional[CustomerFinancialLevel] = None
    purchase_readiness: Optional[PurchaseReadiness] = None
    tags: Optional[List[str]] = None



class Acquisition(BaseModel):
    source: Optional[AcquisitionSource] = None
    source_note: Optional[str] = None


class Meta(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = "manual"

    is_deleted: bool = False
    deleted_at: Optional[datetime] = None


# =================================================
# Main Domain Model
# فقط brand_name (داخل identity) اجباری
# =================================================

class Partner(BaseModel):
    id: Optional[str] = None

    identity: Identity
    relationship: Relationship = Field(default_factory=Relationship)
    financial_estimation: FinancialEstimation = Field(default_factory=FinancialEstimation)
    analysis: Analysis = Field(default_factory=Analysis)
    acquisition: Acquisition = Field(default_factory=Acquisition)
    meta: Meta = Field(default_factory=Meta)

    class Config:
        use_enum_values = True
