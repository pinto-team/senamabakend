from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


# -------------------------------------------------
# Enums
# -------------------------------------------------

class BusinessType(str, Enum):
    producer = "producer"
    supplier = "supplier"
    seller = "seller"
    other = "other"


class CreditStatus(str, Enum):
    good = "good"
    normal = "normal"
    bad = "bad"


class PartnershipStatus(str, Enum):
    past = "past"
    present = "present"
    future = "future"


class PotentialLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


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


class PreferredChannel(str, Enum):
    phone = "phone"
    whatsapp = "whatsapp"
    instagram = "instagram"
    telegram = "telegram"
    email = "email"
    in_person = "in_person"
    other = "other"


class FunnelStage(str, Enum):
    prospect = "prospect"
    lead = "lead"
    qualified = "qualified"
    customer = "customer"
    churned = "churned"


class CustomerLevel(str, Enum):
    A = "A"
    B = "B"
    C = "C"


# -------------------------------------------------
# Sub Models
# -------------------------------------------------

class ContactNumber(BaseModel):
    label: Optional[str] = None
    number: str


class SocialLink(BaseModel):
    platform: str
    url: str


class Location(BaseModel):
    latitude: float
    longitude: float


# -------------------------------------------------
# Main Model: BusinessPartner
# -------------------------------------------------

class BusinessPartner(BaseModel):
    id: Optional[str] = None  # Mongo _id

    # اطلاعات پایه
    brand_name: str
    manager_full_name: str

    contact_numbers: List[ContactNumber] = []
    social_links: List[SocialLink] = []

    # ماهیت کسب‌وکار
    business_type: BusinessType
    category: Optional[str] = None
    sub_category: Optional[str] = None
    tags: List[str] = []

    # موقعیت
    address: Optional[str] = None
    location: Optional[Location] = None

    # سابقه مالی
    first_transaction_date: Optional[str] = None
    first_transaction_amount: Optional[float] = None

    last_transaction_date: Optional[str] = None
    last_transaction_amount: Optional[float] = None

    total_transaction_amount: Optional[float] = 0.0
    transaction_count: Optional[int] = 0
    avg_transaction_value: Optional[float] = None
    credit_status: Optional[CreditStatus] = None

    # سابقه همکاری
    purchased_products: List[str] = []
    partnership_status: Optional[PartnershipStatus] = None
    last_interaction: Optional[str] = None

    interest_level: Optional[int] = None  # 1–5
    potential: Optional[PotentialLevel] = None
    current_contract: Optional[str] = None
    purchase_probability: Optional[float] = None  # 0.0 ~ 1.0

    # CRM اضافی
    team_size: Optional[int] = None
    satisfaction: Optional[int] = None  # 1–5
    payment_type: Optional[PaymentType] = None
    sensitivity: Optional[SensitivityType] = None
    preferred_channel: Optional[PreferredChannel] = None
    funnel_stage: Optional[FunnelStage] = None
    how_found: Optional[str] = None

    # نوع مشتری
    customer_type: Optional[str] = None
    customer_level: Optional[CustomerLevel] = None

    # یادداشت‌ها
    notes: Optional[str] = None

    class Config:
        use_enum_values = True
