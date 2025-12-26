from pydantic import BaseModel
from typing import Optional, List

from app.models.partner import (
    FunnelStage,
    PotentialLevel,
    CustomerFinancialLevel,
    PurchaseReadiness
)


class PartnerAnalysisUpdate(BaseModel):
    """
    آپدیت داده‌های تحلیلی و مدیریتی
    """

    funnel_stage: Optional[FunnelStage] = None
    potential_level: Optional[PotentialLevel] = None

    financial_level: Optional[CustomerFinancialLevel] = None   # سطح توان مالی
    purchase_readiness: Optional[PurchaseReadiness] = None     # آمادگی خرید (سه‌گزینه‌ای)

    tags: Optional[List[str]] = None
