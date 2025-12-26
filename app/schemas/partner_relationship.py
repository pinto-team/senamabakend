from pydantic import BaseModel
from typing import Optional, List

from app.models.partner import (
    PartnershipStatus,
    CustomerRelationshipLevel,
    CustomerSatisfaction,
    SocialPlatform,
    CreditStatus,
    PaymentType,
    SensitivityType
)


class PartnerRelationshipUpdate(BaseModel):
    """
    آپدیت وضعیت ارتباط با مخاطب
    """

    partnership_status: Optional[PartnershipStatus] = None
    customer_relationship_level: Optional[CustomerRelationshipLevel] = None
    customer_satisfaction: Optional[CustomerSatisfaction] = None

    credit_status: Optional[CreditStatus] = None
    payment_types: Optional[List[PaymentType]] = None  # ترکیبی
    sensitivity: Optional[SensitivityType] = None

    preferred_channel: Optional[SocialPlatform] = None
    notes: Optional[str] = None
